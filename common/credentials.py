"""get all credentials (Clickhouse and RIPE)"""
import os

from common.logger_config import logger
from dotenv import load_dotenv


def get_ripe_atlas_credentials() -> dict:
    """return ripe credentials from env var or dotenv file"""
    load_dotenv()

    try:
        return {
            "username": os.environ["RIPE_USERNAME"],
            "secret_key": os.environ["RIPE_SECRET_KEY"],
        }

    except KeyError as e:
        logger.error(
            f"Missing credentials for interacting with IRIS API (set: RIPE_USERNAME | RIPE_SECRET_KEY): {e}"
        )
