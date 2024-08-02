"""This module contains main functions of scraping Divar project.

Functions:
    tokens: Get tokens for last 25 hours and save them in tokens.csv.
    data: Request for each token in tokens.csv, save required data.
Local imports:
    tools, model, read_json, read_real_estate
"""

import tools
import model
from read_json import extract_tokens_info
import read_real_estate


# ---------------------------------------------------------------------
def tokens(
    city_name: str = "tehran", category: str = "apartment-sell"
) -> None:
    """Get tokens for last 25 hours and save them in tokens.csv.

    Args:
        city_name(str , default="tehran"):  tehran:1, karaj:2, mashhad:3,
            isfahan:4,tabriz:5, shiraz:6, ahvaz:7, qom:8, kermanshah:9
        category(str, default="apartment-sell"):
            "apartment-sell", "house-villa-sell","plot-old"
    Returns:
        None
    """

    tools.logger.info(
        "%s Tokens for %s, %s %s ", "*" * 10, city_name, category, "*" * 10
    )

    with open("tokens.csv", "w", encoding="utf-8"):
        pass

    counter = 0
    now = tools.now
    yesterday = tools.yesterday_ts
    url = tools.get_tokens_url
    req_json = {
        "city_ids": [f"{tools.city_code[city_name]}"],
        "pagination_data": {
            "@type": tools.get_tokens_type,
            "last_post_date": now,
        },
        "search_data": {
            "form_data": {
                "data": {
                    "category": {"str": {"value": category}},
                    "sort": {"str": {"value": "sort_date"}},
                }
            }
        },
    }

    while True:
        print(url, req_json)
        response = tools.try_req_json(url=url, req_json=req_json)
        print(response)
        token_list, last_post_ts, req_json["pagination_data"] = (
            extract_tokens_info(response=response)
        )
        model.write_tokens_csv(
            tokens=token_list,
            category=category,
            city_name=city_name,
        )

        counter += 1
        print(f"Page: {counter}, timestamp: {last_post_ts}")

        if counter == 100 or yesterday > int(last_post_ts):
            break

    # End of while loop

    tools.logger.info(
        "%s Finished. Number of pages: %s, %s ", "*" * 10, counter, "*" * 10
    )


# ---------------------------------------------------------------------
def data() -> None:
    """Request for each token in tokens.csv, save required data."""

    tools.logger.info(
        "%s Getting data for each token in tokens.csv. %s ", "*" * 10, "*" * 10
    )

    with open("tokens.csv", "r", encoding="utf-8", newline="\r\n") as f:
        token_list = f.read().replace("\n", ",").split(",")
    token_list = [token for token in token_list if token not in ("", "\n")]

    counter = 0
    for token in token_list:

        url = tools.get_data_url + str(token)
        response = tools.try_req_json(url=url)

        if not response:
            tools.logger.critical("Skipping %s.", token)
            continue

        data_dict = read_real_estate.RealEstate(response).manager()
        print(data_dict, f"\nToken: {token}, Number: {counter}")
        model.write_data_db(data=data_dict)

        counter += 1
        print(data_dict, f"\nToken: {token}, Number: {counter}")
    # End of for loop (token_list)

    tools.logger.info(
        "%s Finished. %s tokens. %s ", "*" * 10, counter, "*" * 10
    )
