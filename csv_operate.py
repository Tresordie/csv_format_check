# !usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import datetime
import pandas as pd


def get_rows_quantity(csv_file):
    df = pd.read_csv(csv_file)
    return df.shape[0]


def get_columns_quantity(csv_file):
    df = pd.read_csv(csv_file)
    return df.shape[1]


def creat_csv(csv_file_to_be_created, csv_header):
    # print(csv_file_to_be_created)
    with open(csv_file_to_be_created, "w", encoding="utf8", newline="") as f_bft:
        csv_write = csv.writer(f_bft)
        csv_write.writerow(csv_header)


# method1: 1st row read
def read_csv_head(csv_path):
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        # print(rows[0])
        return rows[0]


# method2: 1st row read
def read_csv_firstROW(path):
    with open(path, "r") as f:
        reader = csv.reader(f)
        fistROW = next(reader)
        print(fistROW)


# read one column data
def read_csv_one_column(csv_path, column_num):
    """
    csv_path:   csv file path
    column_num: specific column need to be read out
    """
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rowList = [rowIndex[column_num] for rowIndex in reader]
        # print(rowList)
        return rowList


# read specific column data
def read_csv_column(csv_path, row_num, column_num):
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        column = [rowIndex[column_num] for rowIndex in reader]
        # print(column[column_num])
        return column[row_num]


# read specific [row, column] data
def read_csv_column_optimized(csv_path, row_num, column_num):
    global test_val
    temp_full_list = []
    temp_data = []
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        temp_full_list = [rowIndex for rowIndex in reader]
        temp_data = temp_full_list[row_num]
        test_val = temp_data[column_num]
        # print(test_val)
        return test_val


# write data to specific .csv file
def write_row_to_csv(row_data, csv_path):
    with open(
        csv_path, "a", encoding="utf8", newline=""
    ) as f:  # newline='': delete empty line
        writer = csv.writer(f)
        writer.writerow(row_data)


# calculate testing cycle time 20230313123924
def calculate_cycle_time(start_time, end_time):
    start_time_split_with_space = start_time.split(" ")
    start_time_split_before_space = start_time_split_with_space[0]
    start_time_split_after_space = start_time_split_with_space[1]

    start_time_year_month_day = start_time_split_before_space.split("-")
    # print(start_time_year_month_day)
    start_time_hour_minute_second = start_time_split_after_space.split(":")
    # print(start_time_hour_minute_second)

    start_time_year = int(start_time_year_month_day[0])
    start_time_month = int(start_time_year_month_day[1])
    start_time_day = int(start_time_year_month_day[2])
    start_time_hour = int(start_time_hour_minute_second[0])
    start_time_minute = int(start_time_hour_minute_second[1])
    start_time_second = int(start_time_hour_minute_second[2])

    end_time_split_with_space = end_time.split(" ")
    end_time_split_before_space = end_time_split_with_space[0]
    end_time_split_after_space = end_time_split_with_space[1]

    end_time_year_month_day = end_time_split_before_space.split("-")
    end_time_hour_minute_second = end_time_split_after_space.split(":")
    end_time_year = int(end_time_year_month_day[0])
    end_time_month = int(end_time_year_month_day[1])
    end_time_day = int(end_time_year_month_day[2])
    end_time_hour = int(end_time_hour_minute_second[0])
    end_time_minute = int(end_time_hour_minute_second[1])
    end_time_second = int(end_time_hour_minute_second[2])

    t_start = datetime.datetime(
        start_time_year,
        start_time_month,
        start_time_day,
        start_time_hour,
        start_time_minute,
        start_time_second,
    )
    t_start_total_sec = (t_start - datetime.datetime(1970, 1, 1)).total_seconds()

    t_end = datetime.datetime(
        end_time_year,
        end_time_month,
        end_time_day,
        end_time_hour,
        end_time_minute,
        end_time_second,
    )
    t_end_total_sec = (t_end - datetime.datetime(1970, 1, 1)).total_seconds()

    # print(t_end_total_sec - t_start_total_sec)

    return t_end_total_sec - t_start_total_sec


def get_repeat_element_index_list(src_list, str_repeat):
    count = src_list.count(str_repeat)
    index_list = []
    index = -1

    for i in range(0, count):
        index = src_list.index(str_repeat, index + 1)
        index_list.append(index)

    print(index_list)


def sort_csv(file_name, sort_name, ascending_seq, inplace_state, export_file_name):
    csv_df = pd.read_csv(file_name)
    csv_df.sort_values(
        sort_name, axis=0, ascending=[ascending_seq], inplace=inplace_state
    )
    csv_df.to_csv(export_file_name, index=False)
