import logging
import math
import os.path
import time
import urllib
from io import BytesIO
from pathlib import Path
from typing import Iterable
from urllib.request import urlopen
from zipfile import ZipFile

import pandas as pd
from django.conf import settings
from django.core.management import BaseCommand

from police_reports.models import Crime

logger = logging.getLogger('django')


class Command(BaseCommand):
    rename_map = {
        'Crime Id': 'crime_id',
        'Original Crime Type Name': 'crime_type',
        'Report Date': 'report_date',
        'Call Date': 'call_date',
        'Offense Date': 'offense_date',
        'Call Time': 'call_time',
        'Call Date Time': 'call_date_time',
        'Disposition': 'disposition',
        'Address': 'address',
        'City': 'city',
        'State': 'state',
        'Agency Id': 'agency_id',
        'Address Type': 'address_type',
        'Common Location': 'common_location'
    }

    @staticmethod
    def _count_lines(filepath: Path) -> int:
        with open(filepath, 'r') as f:
            return len(f.readlines())

    @staticmethod
    def _convert_to_date(
            df: pd.DataFrame,
            fields_to_convert: Iterable[str]
    ) -> pd.DataFrame:
        for field in fields_to_convert:
            df[field] = pd.to_datetime(df[field]).dt.date
        return df

    @staticmethod
    def _convert_to_utc_tz_aware(
            df: pd.DataFrame,
            fields_to_convert: Iterable[str]
    ) -> pd.DataFrame:
        for field in fields_to_convert:
            df[field] = pd.to_datetime(df[field]).dt.tz_localize('UTC')
        return df

    @staticmethod
    def _download_csv_file() -> None:
        url = (
            "https://gist.github.com/tm-minty/"
            "c39f9ab2de1c70ca9d4d559505678234/raw/"
            "8ecaee79b2c2cce88d60815aadeebb5ac209603a/"
            "police-department-calls-for-service.csv.zip"
        )
        http_response = urlopen(url)
        zipfile = ZipFile(BytesIO(http_response.read()))
        zipfile.extractall('.')

    def _check_for_file_existence(self, filepath: Path) -> None:
        if not os.path.exists(filepath):
            print("Downloading csv file...")
            self._download_csv_file()
            print("File downloaded")

    def handle(self, *args, **options):
        start_time = time.perf_counter()
        total_created = 0
        filepath = (
                settings.BASE_DIR / 'police-department-calls-for-service.csv'
        )
        chunk_size = 100_000
        self._check_for_file_existence(filepath)
        message = 'Started loading data from csv file...'
        print(message)
        logger.info(message)

        chunked_df = pd.read_csv(filepath, chunksize=chunk_size)  # to save RAM
        existing_crime_ids = list(
            Crime.objects.only('crime_id').values_list('crime_id', flat=True)
        )

        total_lines = self._count_lines(filepath)
        total_steps = math.ceil(total_lines/chunk_size)
        logger.info(
            f"Rows: {total_lines}, steps: {total_steps},"
            f"chunk size: {chunk_size}"
        )

        for i, chunk in enumerate(chunked_df):
            print(f"{i+1}/{total_steps}")
            to_create = []
            chunk = chunk[~chunk['Crime Id'].isin(existing_crime_ids)]

            chunk = self._convert_to_date(
                chunk, ('Call Date', 'Offense Date', 'Report Date')
            )
            chunk = self._convert_to_utc_tz_aware(
                chunk, ('Call Date Time',)
            )
            chunk = chunk.rename(
                columns=self.rename_map
            ).T.to_dict().values()

            for item in chunk:
                to_create.append(Crime(**item))

            if to_create:
                total_created += len(to_create)
                Crime.objects.bulk_create(to_create, batch_size=chunk_size)
            else:
                print("no new records, skipped")
            logger.info(f"Finished step {i+1}")

        elapsed_time = round(time.perf_counter() - start_time, 2)
        message = (
            f"Finished parsing csv file, "
            f"new records: {total_created}, "
            f"elapsed time: {elapsed_time} sec"
        )
        print(message)
        logger.info(message)
