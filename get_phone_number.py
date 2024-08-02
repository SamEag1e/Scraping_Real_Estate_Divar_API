"""This module gets the phone number of each ad"""

# This is not joined to other parts of the project.
# I didn't need to have phone numbers in this particular project.
# But it's possible to get and save phone numbers too.
# Just need to make an authorized session in main.py or get_divar
# and make request for each token in get_divar.data()
# and then add the field to data_dict.

import requests

import tools


def phone_number(token: str) -> str:
    """Create an authorized session and return phone _extract_token"""

    headers = tools.headers
    session = requests.Session()

    phone = input("Phone Number: ")
    response = session.post(
        url=tools.phone_session_url,
        json={"phone": phone},
        headers=headers,
    )

    code = input("Code: ")
    response = session.post(
        url=tools.phone_session_confirm_url,
        json={"phone": phone, "code": code},
        headers=headers,
    )

    headers.update({"Authorization": "Basic " + response.json()["token"]})

    return _extract_phone(token=token, req_session=session, headers=headers)


def _extract_phone(token: str, req_session, headers):
    try:
        url = tools.get_phone_url + str(token)
        response = req_session.get(url, headers=headers).json()
        for item in response["widget_list"]:
            if (
                item["widget_type"] == "UNEXPANDABLE_ROW"
                and item["data"]["title"] == "شمارهٔ موبایل"
            ):
                return item["data"]["action"]["payload"]["phone_number"]
    except Exception as e:
        print(e)
    return "Unknown"


if __name__ == "__main__":
    # Test
    pass
