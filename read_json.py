""" Iterate json files and return required data """

from datetime import date
import tools


class ReadDivarJson:
    """Iterate json files and return required data"""

    def __init__(self, response_json) -> None:

        self.res = response_json
        self.r_sec = response_json["sections"]  # list of dicts(sections)
        idx = {
            item["section_name"]: self.r_sec.index(item) for item in self.r_sec
        }  # Index of sections.

        # Data_section
        self.d_sec = self.r_sec[idx["LIST_DATA"]]["widgets"]
        self.token = self.res["webengage"]["token"]

    # -----------------------------------------------------------------
    def title_description(self) -> dict:
        """Returns title and description of given response"""
        title = (
            (self.res["seo"]["web_info"]["title"])
            .replace('"', "")
            .replace("'", "")
        )
        description = (
            (self.res["seo"]["description"]).replace('"', "").replace("'", "")
        )
        description = description.replace(
            "سایت ثبت آگهی، نیازمندی و خرید و فروش دیوار", ""
        )
        return {"title": title, "description": description}

    # -----------------------------------------------------------------
    def ad_info(self) -> dict:
        """Returns ad_date, city, category and district of given response"""
        city = self.res["webengage"]["city"]
        if city not in ["tabriz", "kermanshah"]:
            if self.res["webengage"]["district"]:
                district = self.res["webengage"]["district"]
            else:
                district = "Unknown"

        else:
            temp = " ".join(self.title_description().values())
            district = ""
            if city == "tabriz":
                for key, value in tools.tabriz_districts.items():
                    if key in temp:
                        district += value + ", "
                if district == "":
                    district = "Unknown"

            else:
                for key, value in tools.kermanshah_districts.items():
                    if key in temp:
                        district += value + ", "
                if district == "":
                    district = "Unknown"

        return {
            "ad_date": date.today(),
            "token": self.token,
            "city": city,
            "category": self.res["webengage"]["category"],
            "district": district,
        }


# End of class ReadDivarJson ------------------------------------------


def extract_tokens_info(response) -> tuple:
    """Extract important information from the response and return them."""
    return (
        response["action_log"]["server_side_info"]["info"]["tokens"],
        response["action_log"]["server_side_info"]["info"][
            "last_post_date_epoch"
        ],
        response["pagination"]["data"],
    )
