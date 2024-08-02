"""This module handles dynamic read/write processes for get_divar.

Class:
    Model: An object to read/write dynamically from/to database.
Functions:
    write_tokens_csv: Write tokens to tokens.csv if they're not
        already in database.
    write_data_db: Write data to database if they're appropriate
        for future uses.
Third party import:
    mysql.connector
"""

from datetime import date, timedelta

import mysql.connector

import tools


class Model:
    """A mini ORM for Divar project"""

    # -----------------------------------------------------------------
    def __init__(
        self,
        user=tools.db_username,
        pw=tools.db_password,
        host="localhost",
        database="real_estate",
    ) -> None:
        """Initialize the model.

        Args:
            user: Username for connecting to db. (default=DEFINE IN ENV)
            pw: Password for connecting to db. (default=DEFINE IN ENV)
            host: Host for connecting to db. (default="localhost")
        Return:
            None
        """

        self.user = user
        self.pw = pw
        self.host = host
        self.data_base = database
        self.connection = None
        self.cursor = None

    # -----------------------------------------------------------------
    def _open(self) -> None:
        connection = mysql.connector.connect(
            user=self.user,
            password=self.pw,
            host=self.host,
            database=self.data_base,
        )

        self.connection = connection
        self.cursor = connection.cursor()

    # -----------------------------------------------------------------
    def _close(self) -> None:

        self.cursor.close()
        self.connection.close()

    # -----------------------------------------------------------------
    def insert(self, table, **kwargs) -> None:
        """Inserts to database with given info and returns last_row_id.

        Args:
            table (str): Name of the table which data will be
                written to.
            kwargs: The "column: values" which will be added to the table.
        Returns:
            int: The last_row_id
        """

        columns = kwargs.keys()
        values = kwargs.values()
        query = f"INSERT INTO `{str(table)}` "
        query += (
            "(" + ", ".join(["`%s`"] * len(columns)) % tuple(columns) + ")"
        )
        query += (
            " VALUES ("
            + ", ".join(['"%s"'] * len(values)) % tuple(values)
            + ");"
        )

        self._open()
        self.cursor.execute(query)
        self.connection.commit()
        self._close()

    # -----------------------------------------------------------------
    def duplicate_check(self, table, city, token):
        """Checks if the row exists in last 10 days"""

        today = date.today()
        ten_d_ago = str(today - timedelta(days=10))
        today = str(today)
        query = f"SELECT * FROM `{table}` WHERE "
        query += f'(`city` = "{city}") '
        query += f'AND (`token` = "{token}") '
        query += f'AND (`ad_date` BETWEEN "{ten_d_ago}" AND "{today}")'

        self._open()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self._close()

        return result


# End of class Model --------------------------------------------------

_db = Model()


# ---------------------------------------------------------------------
def write_tokens_csv(tokens: list, category: str, city_name: str) -> None:
    """Write tokens to tokens.csv if they're not already in database."""

    duplicates = [
        token
        for token in tokens
        if _db.duplicate_check(
            table=_table_name(category), city=city_name, token=token
        )
    ]
    if duplicates:
        tools.logger.info("Skipping duplicates %s\n ", duplicates)
    unique_tokens = [token for token in tokens if token not in duplicates]

    if not unique_tokens:
        tools.logger.info("All duplicate from a timestamp. Skipping...")

    else:
        with open("tokens.csv", "a", encoding="utf-8", newline="\n") as file:
            for token_ in unique_tokens:
                file.writelines([token_ + ","])
                if token_ == tokens[-1]:
                    file.write("\n")


# ---------------------------------------------------------------------
def write_data_db(data: dict) -> None:
    """Write data to database if they're appropriate for future uses."""

    if -404 in (data.get("price_per_msquare"), data.get("total_price")):
        # Skip ads without price.
        tools.logger.info("Skipping due to no price....")
        return None
    table = _table_name(data["category"])
    del data["category"]
    _db.insert(table=table, **data)
    return None


# ---------------------------------------------------------------------
def _table_name(category: str) -> str:
    return {
        "apartment-sell": "main_apartment",
        "house-villa-sell": "main_villa",
        "plot-old": "main_land",
    }.get(category)
