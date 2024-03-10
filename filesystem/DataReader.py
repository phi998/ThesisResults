import os
import re

import pandas as pd


class DataReader:

    def __init__(self, datasets_folder):
        self.__datasets_folder = datasets_folder

    def exists_dataset(self, dataset_name, case_name):
        print(os.path.join(self.__datasets_folder, "output", case_name, f'{dataset_name}.csv'))
        return os.path.exists(os.path.join(self.__datasets_folder, "output", case_name, f'{dataset_name}.csv')) and os.path.exists(os.path.join(self.__datasets_folder, "expected", case_name, f'{dataset_name}.csv'))

    def read_dataset(self, dataset_group, dataset_name):
        df = pd.read_csv(os.path.join(self.__datasets_folder, dataset_group, f'{dataset_name}.csv'), header=None)

        return df

    def read_expected(self, dataset_name, case_name):
        df = pd.read_csv(os.path.join(self.__datasets_folder, "expected", case_name, f'{dataset_name}.csv'))
        df = df.rename(columns=lambda x: re.sub(r'\.\d+$', '', x))

        return df

    def read_output(self, dataset_name, case_name, ignore_renaming=False):
        df = pd.read_csv(os.path.join(self.__datasets_folder, "output", case_name, f'{dataset_name}.csv'))

        if not ignore_renaming:
            df = df.rename(columns=lambda x: re.sub(r'\.\d+$', '', x))

        return df
