import pandas as pd
from datetime import datetime
import re


class CSVValidator:
    REQUIRED_COLUMNS = {
        "trip_id",
        "client_id",
        "driver_id",
        "trip_date",
        "status"
    }

    VALID_STATUS = {"done", "not_respond"}

    # YYYY-MM-DD HH:MM:SS.mmm
    DATE_PATTERN = re.compile(
        r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$"
    )

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None

    def load(self):
        self.df = pd.read_csv(self.csv_path, sep=";", quotechar='"', header=0, dtype=str, na_values=["", " ", "NULL", "null"])
        if self.df.empty:
            raise ValueError("CSV file is empty")

    def validate_columns(self):
        missing = self.REQUIRED_COLUMNS - set(self.df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    def validate_nulls_and_blanks(self):
        if self.df.isnull().any().any():
            raise ValueError("Null values detected in CSV")

        blanks = self.df.applymap(
            lambda x: isinstance(x, str) and x.strip() == ""
        )

        if blanks.any().any():
            raise ValueError("Blank (empty string) values detected in CSV")


    def validate_duplicates(self):
        if self.df["trip_id"].duplicated().any():
            raise ValueError("Duplicate trip_id values found")

        if self.df.duplicated().any():
            raise ValueError("Duplicate rows found")

    def validate_status(self):
        if not self.df["status"].isin(self.VALID_STATUS).all():
            raise ValueError("Invalid status values found")

    def validate_trip_date_format(self):
        invalid_dates = self.df[
            ~self.df["trip_date"].astype(str).str.match(self.DATE_PATTERN)
        ]

        if not invalid_dates.empty:
            raise ValueError(
                "trip_date must match format YYYY-MM-DD HH:MM:SS.mmm"
            )
    def show_example_rows(self):
        print(self.df.head(3))

    def validate_trip_date_logic(self):
        parsed_dates = pd.to_datetime(
            self.df["trip_date"], format="%Y-%m-%d %H:%M:%S.%f"
        )

        if (parsed_dates > datetime.now()).any():
            raise ValueError("trip_date contains future dates")

    def run_all(self):
        self.load()
        self.validate_columns()
        self.validate_nulls_and_blanks()
        self.validate_duplicates()
        self.validate_status()
        self.validate_trip_date_format()
        self.validate_trip_date_logic()
        self.show_example_rows()
