import os
import sys
from pprint import pprint
from typing import Union, Any, Sequence, Dict

import influxdb
import serial
import logging
from datetime import datetime

from influxdb import InfluxDBClient

SERIAL_DEVICE = os.environ.get("PORT", "/dev/ttyS0")

ALARM_NONE = "None"
ALARM_HIGH = "High"
ALARM_LOW = "Low"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def parse_datetime(datestr: str) -> datetime:
    return datetime.strptime(datestr, "%m/%d/%Y %H:%M:%S")


def parse_on_off(st: str) -> bool:
    return st.lower() == "on"


def parse_alarm(alarm_str: str) -> Union[str, None]:
    alarm_str = alarm_str.lower()
    if alarm_str == "none":
        return ALARM_NONE
    elif alarm_str == "high":
        return ALARM_HIGH
    elif alarm_str == "low":
        return ALARM_LOW
    else:
        return None


def parse_yes_no(st: str) -> str:
    return st.lower() == "yes"


def parse_limit(limit_str):
    limit_str = limit_str.lower()
    if limit_str == "off":
        return None
    return str.digits(limit_str)


def parse_channel(fields: Sequence[str]) -> Dict[str, Any]:
    return {
        "SR": float(fields[0]),
        "SEF": float(fields[1]),
        "BISBIT": fields[2],
        "BIS": float(fields[3]),
        "power": float(fields[4]),
        "EMG": float(fields[5]),
        "SQI": float(fields[6]),
        "impedance": int(fields[7]),
        "artefacts": fields[8],
    }


class SerialDecoder(object):
    def __init__(self, port=SERIAL_DEVICE, **options):
        self.ser = serial.Serial(port, **options)
        logger.info(f"Opened port {port}: {self.ser}")

    def poll_lines(self):
        line_raw = self.ser.readline()
        # BIS Also sends a null after \n for some reason:
        self.ser.read(1)
        return SerialDecoder.decode_line(line_raw.decode('latin1'))

    @staticmethod
    def decode_line(line: str):
        raw_fields = line.split('|')
        fields = list(map(str.strip, raw_fields))

        # The first two lines from the BIS are column names that
        # can be safely ignored

        if len(fields) != 36:
            logger.error("Decoded line did not contain 36 fields, skipping")
            return None

        doc = {
            "timestamp": parse_datetime(fields[0]),
            "DSC": fields[1],
            "PIC": fields[2],
            "filters": parse_on_off(fields[3]),
            "alarm": {
                "type": parse_alarm(fields[4]),
                "limit_high": parse_limit(fields[5]),
                "limit_low": parse_limit(fields[6]),
                "silenced": parse_yes_no(fields[7]),
            },
            "channel_1": parse_channel(fields[8:17]),
            "channel_2": parse_channel(fields[17:26]),
            "channel_both": parse_channel(fields[26:35]),
        }

        return doc

    def close(self):
        if self.ser:
            self.ser.close()


if __name__ == "__main__":
    decoder = SerialDecoder()
    client = influxdb.InfluxDBClient(database="bis")
    client.create_database("bis")

    try:
        tag_value = sys.argv[1]
    except IndexError:
        tag_value = "default"


    try:
        while True:
            bis_line = decoder.poll_lines()
            document = {
                "time": datetime.utcnow().isoformat("T") + "Z",
                "measurement": "channel_both",
                "tags": {
                    "subject": tag_value,
                },
                "fields": bis_line["channel_both"],
            }

            pprint(bis_line)
            client.write_points([document])
    except KeyboardInterrupt:
        decoder.close()
