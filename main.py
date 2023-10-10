"""main correction TP3"""
"""execute each exercise or correction for TP1"""
import requests
import sys

from pathlib import Path

from common.credentials import get_ripe_atlas_credentials
from common.file_utils import dump_json, load_json, insert_json
from common.default import TP3_DATASET_PATH, TP3_RESULTS_PATH
from common.logger_config import logger


def ping(
    target: dict,
    vps: list,
    output_file_path: Path,
) -> int:
    """perform a traceroute from one vp in UA towards one server in RU"""
    logger.info("###############################################")
    logger.info("#  PING                                       #")
    logger.info("###############################################")

    ripe_credentials = get_ripe_atlas_credentials()

    if not ripe_credentials:
        raise RuntimeError(
            "set .env file at the root dir of the project with correct credentials"
        )

    response = requests.post(
        f"https://atlas.ripe.net/api/v2/measurements/?key={ripe_credentials['secret_key']}",
        json={
            "definitions": [
                {
                    "target": target,
                    "af": 4,
                    "packets": 3,
                    "size": 48,
                    "tags": ["netmethrtest12345"],
                    "description": f"Dioptra Geolocation of {target}",
                    "resolve_on_probe": False,
                    "skip_dns_check": True,
                    "include_probe_id": False,
                    "type": "ping",
                }
            ],
            "probes": [{"value": vp, "type": "probes", "requested": 1} for vp in vps],
            "is_oneoff": True,
            "bill_to": ripe_credentials["username"],
        },
    ).json()

    try:
        measurement = {
            "measurement_id": response["measurements"][0],
        }
    except KeyError:
        logger.error("Ping measurement failed.")
        return None

    logger.info(f"measurement uuid (for retrieval): {response['measurements']}")

    insert_json(measurement, output_file_path)

    return measurement["measurement_id"]


def detect_anycast(ip_addresses_list: list, vps: list) -> list:
    """detect anycast addresses from a list of IP addresses"""

    anycast_addresses = []

    for ip_address in ip_addresses_list:
        ping_results = []

        for vp in vps:
            measurement_id = ping(ip_address, vps=[vp], output_file_path=Path())
            if measurement_id is not None:
                ping_results.append(measurement_id)

        # Analyze the ping results
        if len(set(ping_results)) > 1:
            anycast_addresses.append(ip_address)



if __name__ == "__main__":
    ip_addresses_list = [
        {"address_v4": "142.250.201.4"}, # USA, France
        {"address_v4": "157.240.202.35"}, # USA, France
        {"address_v4": "104.16.124.96"}, # USA, Canada
        {"address_v4": "142.250.188.228"}, # USA
    ]

    vps = ["142.250.188.228", "104.16.124.96", "157.240.202.35", "142.250.201.4"]

    anycast_addresses = detect_anycast(ip_addresses_list, vps)

    print(anycast_addresses)


    # Here goes your code for anycast detection, enjoy!
