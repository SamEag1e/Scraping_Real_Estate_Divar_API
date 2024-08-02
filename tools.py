"""Useful function, tools and constants across project moduls."""

import datetime
import time
import os

from json.decoder import JSONDecodeError
import logging
import requests

from dotenv import load_dotenv

load_dotenv()

# logger used in modules
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filename="log.log",
    encoding="utf-8",
    level=logging.INFO,
)

# Constants used in modules -------------------------------------------

city_code = {
    "tehran": 1,
    "karaj": 2,
    "mashhad": 3,
    "isfahan": 4,
    "tabriz": 5,
    "shiraz": 6,
    "ahvaz": 7,
    "qom": 8,
    "kermanshah": 9,
}

now = datetime.datetime.utcnow().isoformat() + "Z"
yesterday_ts = int((time.time()) * (10**6)) - (3600 * 25 * 10**6)

headers = {
    "Accept": os.getenv("HEADER_ACCEPT"),
    "User-Agent": os.getenv("HEADER_USER_AGENT"),
}
get_tokens_url = os.getenv("GET_TOKENS_URL")
get_tokens_type = os.getenv("GET_TOKENS_TYPE")
get_data_url = os.getenv("GET_DATA_URL")
phone_session_url = os.getenv("PHONE_SESSION_AUTH_URL")
phone_session_confirm_url = os.getenv("PHONE_SESSION_CONFIRM_URL")
get_phone_url = os.getenv("GET_PHONE_URL")

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

# UPDATE LATER-Disctricts of Tabriz and Kermanshah --------------------
tabriz_districts = {
    "باغ فجر": "baghe-fajr",
    "باغفجر": "baghe-fajr",
    "باغ گلستان": "baghe-fajr",
    "باغ قاباغی": "baghe-fajr",
    "خیابان امام": "emam-street",
    "ولی عصر": "vali-asr",
    "ولیعصر": "vali-asr",
    "منصور": "mansour",
    "گلگشت": "golgasht",
    "گل گشت": "golgasht",
    "مفتح": "mofatteh",
    "خطیب": "khatib",
    "راه آهن": "rah-ahan",
    "حافظ": "hafez",
    "باغمیشه": "baghmishe",
    "کوچه باغ": "kouche-bagh",
    "قره آغاج": "ghara-aghaj",
    "نصف راه": "nesfe-rah",
    "ورزش": "varzesh",
    "منظریه": "manzariyeh",
}

kermanshah_districts = {}


# ---------------------------------------------------------------------
def try_req_json(url: str, req_json=False) -> dict:
    """Get response and make it json, return "data" section."""

    res = _try_request(url, req_json=req_json)
    if res["flag"]:
        return {}

    res = _try_json(res["response"], is_token=True if req_json else False)
    if res["flag"]:
        return {}

    return res["data"]


# ---------------------------------------------------------------------
def _try_request(url: str, req_json=False) -> dict:
    flag = response = False
    for err_count in range(1, 6):
        try:
            if req_json:
                response = requests.post(
                    url,
                    json=req_json,
                    headers=headers,
                    timeout=(1, 5),
                )
            else:
                response = requests.get(url, headers=headers, timeout=(1, 5))
            break
        # End of try.
        except requests.exceptions.RequestException:
            logger.critical("Connection/request error, trying %i", err_count)
            time.sleep(1)
            if err_count == 5:
                flag = True
            continue
        # End of except.
    time.sleep(1)
    return {"response": response, "flag": flag}


# ---------------------------------------------------------------------
def _try_json(response, is_token: bool) -> dict:

    flag = data = False
    try:
        data = response.json()
        data["action_log"] if is_token else data["sections"]  # Test

    except (JSONDecodeError, KeyError, TypeError) as e:
        logger.critical("Json error... %s", e)
        flag = True

    return {"flag": flag, "data": data}
