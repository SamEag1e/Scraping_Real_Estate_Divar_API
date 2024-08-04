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


# Disctricts of Tabriz and Kermanshah ---------------------------------
tabriz_districts = {
    "قره‌آغاج": "ghara-aghaj",
    "خطیب": "khatib",
    "راه‌آهن": "raah-ahan",
    "شهرک‌نور": "shahrak-noor",
    "اندیشه": "andisheh",
    "سهند": "sahand",
    "سهند فاز ۱": "sahand-phase-1",
    "سهند فاز ۲": "sahand-phase-2",
    "سهند فاز ۳": "sahand-phase-3",
    "سهند فاز ۴": "sahand-phase-4",
    "اسکو": "esku",
    "خسروشهر": "khosroshahr",
    "طالقانی": "taaleqani",
    "امیرخیز": "amir-khiz",
    "ملل متحد": "melal-motahed",
    "ارم": "arm",
    "پاسداران": "pasdaran",
    "سرخاب": "sarakhab",
    "منصور": "mansour",
    "مارالان": "maralan",
    "ائل گولی": "eil-goli",
    "زعفرانیه": "zaferanieh",
    "ولیعصر": "vali-e-asr",
    "حکم‌آباد": "hokm-abad",
    "نظام پزشکی": "nezam-pezeshki",
    "استاد جعفری": "ostad-jaafari",
    "ابوذر": "abuzar",
    "بهار": "bahar",
    "کوچه باغ": "kuche-bagh",
    "قدس": "ghods",
    "دکتر قریب": "dr-gharib",
    "رسالت": "resalat",
    "شنب غازان": "shanbe-ghazan",
    "فرهنگ": "farhang",
    "بهشتی": "beheshthi",
    "انقلاب": "enqelab",
    "لاله": "laleh",
    "کوی لاله": "kuye-laleh",
    "رواسان": "ravasan",
    "اخماقیه": "akhmaqiyeh",
    "سردرود": "sardroud",
    "باغ معروف": "bagh-ma’roof",
    "منظریه": "manzariyeh",
    "سفیر امید": "safir-omid",
    "شهرک رازی": "shahrak-razi",
    "سعدی": "saadi",
    "ابوریحان": "abooriyan",
    "ترمینال": "terminal",
    "میدان مسافر": "meydan-mosafir",
    "شاهد": "shahed",
    "دانشگاه پیام نور": "daneshgah-e payam, noor",
    "نصف راه": "nesf-e rah",
    "معراج": "ma’raj",
    "چرنداب": "chernadab",
    "صائب": "sa’eb",
    "پاستور جدید": "pastur-e jadid",
    "پاستور قدیم": "pastur-e ghadim",
    "17 شهریور": "17 shahrivar",
    "بارون آواک": "barun avak",
    "بارناوا": "barnaava",
    "اهراب": "ahraab",
    "باغ فجر": "bagh-e fajr",
    "خیام": "khayyam",
    "خیابان امام": "khiyaban-e emam",
    "آبرسان": "aabersan",
    "فلکه دانشگاه": "felkeh-e daneshgah",
    "خیابان آزادی": "khiyaban-e azaadi",
    "دانشگاه فنی حرفه‌ای": "daneshgah-e fanni-harfeyi",
    "دانشگاه سراسری تبریز": "daneshgah-e sarasari-e tabriz",
    "دانشگاه آزاد": "daneshgah-e aazaad",
    "بلوار نیایش": "bolvar-e niayesh",
    "کسائی": "kassa’i",
    "یادگار امام": "yaadegaar-e emam",
    "زمزم": "zamzam",
    "تجلائی": "tajalla’i",
    "وادی رحمت": "vaadi-ye rahmat",
    "سجادیه": "sajjadiyeh",
    "ساری زمین": "saari zamin",
    "فرهنگیان": "farhangiyaan",
    "میرداماد": "mirdamad",
    "دانش": "danesh",
    "پارک صائب تبریزی": "park-e sa’eb tabrizi",
    "رجائی شهر": "raja’i shahr",
    "الهی پرست": "elahi parast",
    "مخابرات": "mokhabeeraat",
    "دادگستری": "daadgostari",
    "شاه گولی": "shah goli",
    "فردوس": "ferdows",
    "بهارستان": "baharstan",
    "کوی فرشته": "kuye farshad",
    "باغچه بان": "baghcheh baan",
    "فتح آباد": "fath abad",
    "بیمارستان بین‌المللی": "bimarstan-e beynolmelali",
    "شادآباد": "shaadabaad",
    "باغ یعقوب": "bagh-e ya’qub",
    "نعمت آباد": "ne’mat abad",
    "باسمنج": "baasmanj",
    "خاوران": "khaavaraan",
    "مرزداران": "marzdaraan",
    "مصلی": "masjed",
    "شمیم پایداری": "shamim-e paydari",
    "یاغچیان": "yaghchiyan",
    "پرواز": "parvaaz",
    "نارمک": "narmak",
    "باغمیشه": "baghmisheh",
    "رشدیه": "rashdieh",
    "فهمیده": "fahmideh",
    "شهریار": "shahriar",
    "بارنج": "baranj",
    "نصر": "nasr",
    "الهیه": "elahiye",
    "ولی امر": "vali amr",
    "یوسف آباد": "yousef abad",
    "عباسی": "abbasi",
    "سیلاب": "silab",
    "سرباز شهید": "sarbaz shahid",
    "ایده لی": "ideh li",
    "دوه چی": "douh chi",
    "شمس تبریزی": "shams tabrizi",
    "اتحاد": "etehad",
    "کوثر": "kowsar",
    "خلیل آباد": "khalil abad",
    "رضوانشهر": "rezvanshahr",
    "جنت": "jannat",
    "پارک بنفشه": "park-e banafsheh",
    "مجاهد": "mojahed",
    "مفتح": "mofateh",
    "توکلی": "tavakkoli",
    "بازار": "bazaar",
    "شهناز": "shahnaz",
    "مسجد کبود": "masjed kabood",
    "میدان ساعت": "meydan-e saat",
    "تربیت": "tarbiat",
    "گجیل": "gojeel",
    "حافظ": "hafiz",
    "استادیوم تختی": "stadium-e takhti",
    "باغشمال": "bagh-e shomal",
    "والمان": "valaman",
    "نوبر": "nober",
    "ارگ علی شاه": "arg-e ali shah",
    "سه راه امین": "se rah-e amin",
    "محققی": "mahghaghi",
    "چای کنار": "chai kenar",
    "جمشید آباد": "jamshid abad",
    "فرودگاه": "foroudgaah",
    "آذربایجان": "azarbayjan",
    "یکه توکان": "yekkeh tokan",
    "29 بهمن": "29 bahman",
    "راهنمایی": "rahnamayi",
    "گلشهر": "golshahr",
    "دانشسرا": "daneshsara",
    "پل قاری": "pol-e ghaari",
    "مسجد صاحب الامر": "masjed-e sahib al-amr",
    "دارایی": "daaraayi",
    "منجم": "manjam",
    "دانشگاه علامه امینی": "daneshgaah-e allameh amini",
    "پل سنگی": "pol-e sangi",
    "پارک شمس تبریزی": "park-e shams tabrizi",
    "رضانژاد": "rezanjaad",
    "سیدلر": "seyedlar",
    "تپلی باغ": "tapli baagh",
    "کلانتر کوچه": "kolaantar koocheh",
    "گلگشت": "golgasht",
    "بیمارستان شهید مدنی": "bimarstan-e shaheed madani",
    "بیمارستان امام رضا": "bimarstan-e imam reza",
    "فدک": "fodak",
    "پارک ایرانسل": "park-e irancell",
    "دانشکده داندانپزشکی": "daneshkaadeh-e daandanpezeshki",
    "گلنار": "golnaar",
    "گلها": "golha",
    "دانشکده پزشکی": "daneshkaadeh-e pezeshki",
    "بقائیه": "baghaa’iyyeh",
    "گلباد": "golbaad",
    "میخک": "mikhak",
    "اطلس": "atlas",
    "شقایق": "shaqaa’eq",
    "آشتاب": "aashtaab",
    "شهر کتاب": "shahr-e ketab",
    "خاقانی": "khaaghani",
    "ملا زینال": "molla zeinaal",
    "اسماعیل بقال": "esma’il baqaal",
    "پروین اعتصامی": "parvin etesami",
    "بیلانکوه": "bilankoo",
    "ربع رشیدی": "rob’e rashidi",
}

kermanshah_districts = {
    "پارک شیرین": "park-e shirin",
    "22 بهمن": "22 bahman",
    "شهرک سجادیه": "shahrak-e sajjadiyeh",
    "شهرک بسیج": "shahrak-e basij",
    "کهریز": "kahriz",
    "بریموند": "berimond",
    "کیانشهر": "kianshahr",
    "مرادآباد": "moradabad",
    "گلستان": "golestan",
    "شهرک دادگستری": "shahrak-e daadgostari",
    "دیزل آباد": "dizel abad",
    "دولت آباد": "doulat abad",
    "صدرا": "sadra",
    "پردیس": "pardis",
    "بلوار فرهیختگان": "bolvar-e farhikhtegan",
    "صادقیه": "saadeghiyeh",
    "سراب قنبر": "sarab-e qanbar",
    "چشمه سعدی": "cheshmeh sa’di",
    "چاوشان": "chaavoshan",
    "چشمه سعید": "cheshmeh sa’id",
    "درگه غلامعلی": "dargah-e gholamali",
    "ملودی": "meloodi",
    "باغ ماهان": "bagh-e maahan",
    "باغ مهر ویلا": "bagh-e mehr villa",
    "تهران دشت": "tehran dasht",
    "کهنز": "kahanz",
    "گلها": "golha",
    "الهیه": "elahiye",
    "دره دراز": "darreh daraz",
    "شهرک کشاورزی": "shahrak-e keshavarzi",
    "ولایت فاز ۲": "valayat phase 2",
    "شهرک جام جم": "shahrak-e jaam jam",
    "سهرابی": "sohrabi",
    "باغ گلاره": "bagh-e golareh",
    "پارک سعدی": "park-e sa’di",
    "بلوار شاهد": "bolvar-e shaheed",
    "شهرک نجفی": "shahrak-e najafi",
    "سی متری": "si metri",
    "بلور گل سرخ": "bolur-e gol-e sorkh",
    "گلناز": "golnaz",
    "شریعتی": "shariati",
    "مطهری": "motahhari",
    "جعفر آباد": "ja’far abad",
    "شهرک بعثت": "shahrak-e besat",
    "سراب نیلوفر": "sarab-e niloofar",
    "دانشجو": "daneshjoo",
    "کاشانی": "kaashani",
    "دلگشا": "delgushaa",
    "کسری": "kasri",
    "خلیج فارس": "khalij-e fars",
    "دانشگاه آزاد": "daneshgaah-e aazaad",
    "منطقه ۴": "mantaghe 4",
    "منطقه ۵": "mantaghe 5",
    "منطقه ۳": "mantaghe 3",
    "منطقه ۱": "mantaghe 1",
    "منطقه ۲": "mantaghe 2",
    "منطقه ۶": "mantaghe 6",
    "منطقه ۷": "mantaghe 7",
    "خیابان پردیس": "khiyaaban-e pardis",
    "بلوار شقایق": "bolvar-e shaqaa’eq",
    "برج تندیس": "borj-e tondis",
    "بام پردیس": "baam-e pardis",
    "پایتخت کرمانشاه": "paayetakht-e kermanshah",
    "تئاتر شهر": "te’aatr-e shahr",
    "آزادگان": "aazaadegaan",
    "مدرس": "modares",
    "حداد عادل": "haddaad aadel",
    "اربابی": "arbaabi",
    "اعظمی": "a’zami",
    "فلاحی": "fallaahi",
    "بلوار کارگر": "bolvar-e kaargar",
    "آزادی": "aazaadi",
    "سلیمی": "saleemi",
    "شهید امجدیان": "shaheed amjadiyaan",
    "موحد": "mohe’d",
    "گل میخک": "gol mikhak",
    "جلیلی": "jalili",
    "نواب سفری": "navaab safari",
    "باغ نی": "baagh-e ni",
    "بلوار ارشاد": "bolvar-e arshaad",
    "بلوار امامی": "bolvar-e emaami",
    "خیابان صفا": "khiyaaban-e safaa",
    "سنگر": "sangar",
    "بلوار گلریزان": "bolvar-e golrizan",
    "شرکت نفت": "sherkat-e naft",
    "پارک شاهد": "park-e shaheed",
    "گاوبنده": "gaavbandeh",
    "بیمارستان رازی": "bimarstan-e raazi",
    "شهرک باهنر": "shahrak-e baahonar",
    "عمارت ماندگار": "emarat-e mandegaar",
    "کرناچی": "karnaachi",
    "مهر و ماه": "mehr va maah",
    "نوکان": "nokaan",
    "ظفر": "zafar",
    "مسکن": "maskan",
    "طاق بهارستان": "taagh-e bahaaristaan",
    "باغ ابریشم": "baagh-e abrisham",
    "تکاور": "takavvar",
    "سیاهبید سفلی": "siyahbid-e sofla",
    "فرودگاه": "foroudgaah",
    "نصر": "nasr",
    "فرهنگیان": "farhangiyaan",
    "کارمندان": "kaarmendaan",
    "تعاون": "taavon",
    "هوانیرو": "havaaniru",
    "جهاد": "jahad",
    "وحدت": "vahdat",
    "معلم": "mo’allem",
    "میلاد": "milad",
}
