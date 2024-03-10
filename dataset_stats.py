import os

import pandas as pd

folder_path = 'datasets/output/case0'  # Replace with the path to your folder

def get_median(my_list):
    sorted_list = sorted(my_list)

    # Find the median
    length = len(sorted_list)
    if length % 2 == 1:
        # If the length is odd, get the middle element
        median = sorted_list[length // 2]
    else:
        # If the length is even, get the average of the two middle elements
        middle1 = sorted_list[length // 2 - 1]
        middle2 = sorted_list[length // 2]
        median = (middle1 + middle2) / 2

    return median

def calculate_sum_column_count(folder_path):
    total_columns = 0
    total_rows = 0

    cols_n = []
    num_of_files = 0

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            num_of_files += 1
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path, encoding='utf-8')
            num_rows, num_columns = df.shape
            total_columns += num_columns
            total_rows += num_rows
            cols_n.append(num_columns)

    print(f"Num of datasets: {num_of_files}")
    print(f"Num of avg cols: {total_columns/num_of_files}")
    print(f"Num of median cols: {get_median(cols_n)}")
    print(f"Num of avg rows: {total_rows/num_of_files}")

    return total_columns



calculate_sum_column_count(folder_path)