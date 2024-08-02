"""This module contains the RealEstate class to read resp.json().

Class:
    RealEstate: Extends the ReadDivarJson from read_json module.
Local imports:
    read_json
    tools
"""

# General Exception handling can be updated in the future.
# But it's ok for now for two reasons:
#   1. I know what kind of exceptions we're dealing with and why.
#   2. It's ok to have -404 values(as UNKNOWN) for some data.

import read_json
import tools


class RealEstate(read_json.ReadDivarJson):
    """Extends the ReadDivarJson from read_json module."""

    # -----------------------------------------------------------------
    def manager(self) -> dict:
        """Return final result based on category of response.

        Args:

        Returns:
            dict: Required data from response.json()
        """

        match self.ad_info()["category"]:
            case "apartment-sell":
                return self._apartment()
            case "house-villa-sell":
                return self._villa()
            case "plot-old":
                return self._land()
            case _:
                return {"category": "Unknown!"}

    # -----------------------------------------------------------------
    def _buildings_indexes(self) -> dict:
        row_idx = -404
        f_idx = -404
        for item in self.d_sec:
            try:
                if item["widget_type"] == "GROUP_INFO_ROW":
                    row_idx = self.d_sec.index(item)

                elif item["widget_type"] == "GROUP_FEATURE_ROW":
                    f_idx = self.d_sec.index(item)

            except Exception as e:
                tools.logger.critical(
                    "%s. BUILDING_INDEXES: %s", e, self.token
                )

        return {"row": row_idx, "feature": f_idx}

    # -----------------------------------------------------------------
    def _real_estate_prices(self):
        total_price = -404
        price_per_msquare = -404
        for item in self.d_sec:
            try:
                if item["widget_type"] == "UNEXPANDABLE_ROW":

                    if item["data"]["title"] == "قیمت کل":
                        total_price = item["data"]["value"]

                    elif item["data"]["title"] == "قیمت هر متر":
                        price_per_msquare = item["data"]["value"]

            except Exception as e:
                tools.logger.critical(
                    "%s. REAL_ESTATE_PRICES: %s", e, self.token
                )
        # End of for loop ---------------------------------------------

        try:
            if "مجانی" in total_price or "توافقی" in total_price:
                total_price = -404
            else:
                temp = list(filter(lambda i: i.isdigit(), total_price))
                total_price = int("".join(temp))

        except Exception as e:  # PRICE CAN BE EMPTY
            tools.logger.critical("%s. TOTAL_PRICE: %s", e, self.token)

        try:
            temp = list(filter(lambda i: i.isdigit(), price_per_msquare))
            price_per_msquare = int("".join(temp))

        except Exception as e:  # PRICE CAN BE EMPTY
            tools.logger.critical("%s. PRICE_PER_MSQUARE: %s", e, self.token)

        return {
            "total_price": total_price,
            "price_per_msquare": price_per_msquare,
        }

    # -----------------------------------------------------------------
    def _buildings_main(self):
        row_idx = self._buildings_indexes()["row"]
        msquare = -404
        prod_year = -404
        rooms = -404

        for item in self.d_sec[row_idx]["data"]["items"]:
            try:
                match item["title"]:
                    case "متراژ":
                        msquare = int(item["value"])

                    case "ساخت":
                        temp = list(
                            filter(lambda i: i.isdigit(), item["value"])
                        )
                        prod_year = int("".join(temp))

                    case "اتاق":
                        match item["value"]:
                            case "بدون اتاق":
                                rooms = 0
                            case "بیشتر از ۴":
                                rooms = 5
                            case _:
                                rooms = int(item["value"])
            # End of try

            except Exception as e:
                tools.logger.critical("%s. BUILDINGS_MAIN: %s", e, self.token)
        # End of for loop

        return {
            "msquare": msquare,
            "production_year": prod_year,
            "rooms": rooms,
        }

    # -----------------------------------------------------------------
    def _buildings_features(self):
        f_idx = self._buildings_indexes()["feature"]

        elevator = 0
        parking = 0
        storeroom = 0
        balcony = 0

        try:
            temp = self.d_sec[f_idx]["data"]["items"]
            for item in temp:

                match item["title"]:
                    case "آسانسور":
                        elevator = 1
                    case "پارکینگ":
                        parking = 1
                    case "انباری":
                        storeroom = 1
                    case "بالکن":
                        balcony = 1
                    case "آسانسور ندارد":
                        elevator = 0
                    case "پارکینگ ندارد":
                        parking = 0
                    case "انباری ندارد":
                        storeroom = 0
                    case "بالکن ندارد":
                        balcony = 0
        except Exception as e:
            tools.logger.critical("%s. FEATURES: %s", e, self.token)

        return {
            "elevator": elevator,
            "parking": parking,
            "storeroom": storeroom,
            "balcony": balcony,
        }

    # -----------------------------------------------------------------
    def _apartment(self):
        floor_str = "Unknown"
        floor_number = -404
        total_floors = -404

        for item in self.d_sec:
            if item["widget_type"] == "UNEXPANDABLE_ROW":
                if item["data"]["title"] == "طبقه":
                    floor_str = item["data"]["value"]
                    break
        try:
            temp = floor_str
            temp = temp.replace("زیرهمکف", "-1")
            temp = temp.replace("همکف", "0")
            temp = temp.replace("+", " ")
            temp = temp.replace("بیشتر", " ")
            temp = temp.replace("بالاتر", " ")
            temp = temp.replace("انتخاب نشده", " ")
            if len(temp) > 4:
                temp = temp.split("از")
                floor_number = int(temp[0].strip())
                if temp[1].strip() != "":
                    total_floors = int(temp[1].strip())
                else:
                    total_floors = -404
            else:
                floor_number = int(temp)
                total_floors = -404

        except Exception as e:
            tools.logger.critical("%s. FLOOR_STR: %s", e, self.token)

        result = self.title_description()
        result.update(self.ad_info())
        result.update(
            {"floor_number": floor_number, "total_floors": total_floors}
        )
        result.update(self._real_estate_prices())
        result.update(self._buildings_main())
        result.update(self._buildings_features())
        del result["balcony"]

        return result

    # -----------------------------------------------------------------
    def _villa(self):
        land_msquare = -404

        for item in self.d_sec:
            if item["widget_type"] == "UNEXPANDABLE_ROW":
                if item["data"]["title"] == "متراژ زمین":
                    try:
                        temp = list(
                            filter(
                                lambda i: i.isdigit(), item["data"]["value"]
                            )
                        )
                        land_msquare = int("".join(temp))
                    except Exception as e:
                        tools.logger.critical(
                            "%s. LAND_MSQUARE: %s", e, self.token
                        )
                    break

        result = self.title_description()
        result.update(self.ad_info())
        result.update({"land_msquare": land_msquare})
        result.update(self._real_estate_prices())
        result.update(self._buildings_main())
        result.update(self._buildings_features())
        del result["elevator"]

        return result

    # -----------------------------------------------------------------
    def _land(self):
        land_msquare = -404

        for item in self.d_sec:
            if item["widget_type"] == "UNEXPANDABLE_ROW":
                if item["data"]["title"] == "متراژ":
                    try:
                        temp = list(
                            filter(
                                lambda i: i.isdigit(), item["data"]["value"]
                            )
                        )
                        land_msquare = int("".join(temp))
                    except Exception as e:
                        tools.logger.critical(
                            "%s. LAND_MSQUARE: %s", e, self.token
                        )
                    break

        result = self.title_description()
        result.update(self.ad_info())
        result.update({"land_msquare": land_msquare})
        result.update(self._real_estate_prices())

        return result


# End of class RealEstate ---------------------------------------------
