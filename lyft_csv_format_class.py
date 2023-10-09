# !usr/bin/env python
# -*- coding:utf-8 -*-

from csv_operate import *
import os
import re
import shutil


wrong_folder_validation = False

csv_date_folder = "./"

validate_result_output_file = "validate_result_output.csv"

main_bft_csv_path = "pcba10_07"

# main_bft_csv_path = "PCBA/monolith_main_bft/csv"
main_bft_csv_wrong_path = "PCBA/monolith_main_bft/csv/wrong"

main_flash_csv_path = "0912"
main_flash_csv_wrong_path = "PCBA/Monolith_pcba_flash_station/csv/wrong"

triangle_bft_csv_path = "PCBA/Monolith_triangle_pcba_ft/csv"
triangle_bft_csv_wrong_path = "PCBA/Monolith_triangle_pcba_ft/csv/wrong"

leak_ft_csv_path = "FATP/Monolith_leak_ft/csv"
leak_ft_csv_wrong_path = "FATP/Monolith_leak_ft/csv/wrong"

cassette_ft_csv_path = "1009noncharging_cassette"
cassette_ft_csv_wrong_path = "FATP/monolith_cassette_ft/csv/wrong"

receiver_ft_csv_path = "1009recevier"
receiver_ft_csv_wrong_path = "1009recevier"

bollard_ft_csv_path = "1009bollard"
bollard_ft_csv_wrong_path = "FATP/monolith_bollard_ft/csv/wrong"

solar_flat_ft_csv_path = "0904_solar_panel_IQC/csv"
solar_flat_ft_csv_wrong_path = "FATP/monolith_solar_panel_flat_ft/csv/wrong"

solar_left_ft_csv_path = "FATP/monolith_solar_panel_left_ft/csv"
solar_left_ft_csv_wrong_path = "FATP/monolith_solar_panel_left_ft/csv/wrong"

solar_right_ft_csv_path = "FATP/monolith_solar_panel_right_ft/csv"
solar_right_ft_csv_wrong_path = "FATP/monolith_solar_panel_right_ft/csv/wrong"


lyft_csv_format_header = [
    "record_index",
    "test_name",
    "lower_limit",
    "upper_limit",
    "units",
    "test_value",
    "test_time",
    "pass_fail_status",
    "overall_test_result",
    "exit_status",
    "test_run_uuid",
    "sn",
    "start_time",
    "end_time",
    "work_order",
    "test_station_name",
    "test_station_id",
]

# general column headers item's index
lyft_csv_header_index_dict = {
    "record_index": 0,
    "test_name": 1,
    "lower_limit": 2,
    "upper_limit": 3,
    "units": 4,
    "test_value": 5,
    "test_time": 6,
    "pass_fail_status": 7,
    "overall_test_result": 8,
    "exit_status": 9,
    "test_run_uuid": 10,
    "sn": 11,
    "start_time": 12,
    "end_time": 13,
    "work_order": 14,
    "test_station_name": 15,
    "test_station_id": 16,
}

# validate result output file header
validate_result_csv_header = ["File_Path", "Result", "DRI"]


class lyft_csv_format_validate(object):
    def __init__(self, csv_files_folder_path):
        # csv files search path
        self.search_path = csv_files_folder_path

        # csv format header required by lyft
        self.csv_format_header = lyft_csv_format_header

        # csv header of output result csv file
        self.output_result_csv_header = validate_result_csv_header

        # csv file path of output result
        self.output_result_file_path = (
            csv_date_folder + "_" + validate_result_output_file
        )

        # current csv file been scanned
        self.current_validating_file = ""

        # temporary to record current file errors
        self.current_validating_file_result = ""

        # list to temporarily record current file errors & will be as one row written into output_result_csv
        self.current_validating_file_list = []

        # for multiple same errors, only record one error at a time
        self.current_validating_file_no_repeat_error_counter = 0

        self.header_index_dict = lyft_csv_header_index_dict

        # one csv file total error counter
        self.current_csv_format_err_counter = 0

        self.length_uuid_section = [
            8,
            4,
            4,
            4,
            12,
        ]  # E058FB8C-D506-427B-8F1B-D0B03EDB477C

        if not wrong_folder_validation:
            self.category_correct_csv_format_folder = os.path.join(
                self.search_path, "correct"
            )
            self.mkdir(self.category_correct_csv_format_folder)
            self.category_wrong_csv_format_folder = os.path.join(
                self.search_path, "wrong"
            )
            self.mkdir(self.category_wrong_csv_format_folder)

        # create file to record validate result
        self.create_csv_output_validate_result()

    def mkdir(self, path):
        # print(sys._getframe().f_code.co_name)
        folder = os.path.exists(path)
        if not folder:
            # print("folder not exist, creating folder!")
            os.makedirs(path)
        # else:
        #     print("folder exist!")

    def create_csv_output_validate_result(self):
        creat_csv(self.output_result_file_path, self.output_result_csv_header)

    def write_output_result_to_csv(self):
        self.current_validating_file_list.append(self.current_validating_file)
        self.current_validating_file_list.append(self.current_validating_file_result)
        write_row_to_csv(
            self.current_validating_file_list, self.output_result_file_path
        )

    def clear_current_validating_file_error_counters(self):
        self.current_validating_file_no_repeat_error_counter = 0

    def clear_current_validating_file_list(self):
        self.current_validating_file_list = []

    def clear_current_validating_file_name(self):
        self.current_validating_file = ""

    def clear_current_validating_file_result(self):
        self.current_validating_file_result = ""

    def clear_current_file_total_error_counters(self):
        self.current_csv_format_err_counter = 0

    def file_name_check(self, file_name):
        # check if any txt files
        if file_name:
            temp_tuple = os.path.splitext(file_name)
            # print(temp_tuple)
            if temp_tuple[1] == ".txt":
                self.current_csv_format_err_counter += 1
                self.current_validating_file_result += "Error - txt file exist!\n"
                # print(self.current_validating_file_result)
            elif temp_tuple[1] == ".csv":
                file_name_split = file_name.split("_")
                # print(file_name_split)
                if len(file_name_split) <= 4 or (file_name_split[3] == ".csv"):
                    self.current_csv_format_err_counter += 1
                    self.current_validating_file_result += (
                        "Error - file name incorrect!\n"
                    )
                    # print(self.current_validating_file_result)

    def csv_format_header_check(self, csv_file):
        """
        check if csv file header same as Lyft pre-defined
        """
        # print(sys._getframe().f_code.co_name)
        # use ret_code to mark different csv log format(some csv log without test_run_uuid)
        ret_code = 0

        csv_header_read = read_csv_one_row(csv_file, 0)
        if len(csv_header_read) != len(self.csv_format_header):
            print(
                "csv_file: %s, len(csv_header_read): %d"
                % (csv_file, len(csv_header_read))
            )
            self.current_csv_format_err_counter += 1
            self.current_validating_file_result += "Error - csv_header len mismatch!\n"
            ret_code = 1
        else:
            for i in range(0, len(self.csv_format_header)):
                if csv_header_read[i] != self.csv_format_header[i]:
                    self.current_csv_format_err_counter += 1
                    self.current_validating_file_no_repeat_error_counter += 1
                    if self.current_validating_file_no_repeat_error_counter == 1:
                        self.current_validating_file_result += (
                            "Error - csv_header name incorrect!\n"
                        )
                    ret_code = 2
        self.clear_current_validating_file_error_counters()
        return ret_code

    def record_index_check(self, csv_file):
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        record_index_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["record_index"]
        )

        # check if empty
        for i in range(row_cnt):
            if i == 0:
                if record_index_column_list[i] != 1:
                    self.current_csv_format_err_counter += 1
                    self.current_validating_file_result += (
                        "Error - record_index[1] not equal 1!\n"
                    )

            if record_index_column_list[i] == "" or pd.isna(
                record_index_column_list[i]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - record_index cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and (int(record_index_column_list[i]) + 1) != (
                int(record_index_column_list[i + 1])
            ):
                # print("Error - record_index[%d] not increased by 1" % i)
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - record_index not increased by 1!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def test_name_check(self, csv_file):
        """
        check if test_name valid
        1. not empty
        2. no illegal character in test_name(e.g., @#!~%^&*_+/)
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        test_name_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["test_name"]
        )

        # test_name empty?
        for i in range(row_cnt):
            if "" == test_name_column_list[i] or pd.isna(test_name_column_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_name cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            # any illegal character?
            if (
                (" " in test_name_column_list[i])
                or ("~" in test_name_column_list[i])
                or ("!" in test_name_column_list[i])
                or ("@" in test_name_column_list[i])
                or ("#" in test_name_column_list[i])
                or ("$" in test_name_column_list[i])
                or ("%" in test_name_column_list[i])
                or ("^" in test_name_column_list[i])
                or ("&" in test_name_column_list[i])
                or ("*" in test_name_column_list[i])
                or ("(" in test_name_column_list[i])
                or (")" in test_name_column_list[i])
                or ("?" in test_name_column_list[i])
                or ("-" in test_name_column_list[i])
                or ("+" in test_name_column_list[i])
                or ("=" in test_name_column_list[i])
                or (";" in test_name_column_list[i])
                or (":" in test_name_column_list[i])
                or ("[" in test_name_column_list[i])
                or ("]" in test_name_column_list[i])
                or ('"' in test_name_column_list[i])
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_name with illegal character!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def lower_limit_check(self, csv_file):
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        lower_limit_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["lower_limit"]
        )

        for i in range(1, row_cnt):
            if "" == lower_limit_column_list[i] or pd.isna(lower_limit_column_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - low_limit cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def upper_limit_check(self, csv_file):
        """
        upper_limit check
        1. only check not empty, must have criteria (PASS/Fail or value)
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        upper_limit_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["upper_limit"]
        )

        for i in range(1, row_cnt):
            if "" == upper_limit_column_list[i] or pd.isna(upper_limit_column_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - upper_limit cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def test_value_check(self, csv_file):
        """
        test_value check
        1. only check not empty, must have criteria (PASS/Fail or value)
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        test_value_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["test_value"]
        )

        for i in range(row_cnt):
            if "" == test_value_column_list[i] or pd.isna(test_value_column_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_value cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def test_time_check(self, csv_file):
        """
        test_time check
        1. only check not empty, must have criteria (PASS/Fail or value)
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        test_time_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["test_time"]
        )

        for i in range(1, row_cnt):
            if "" == test_time_column_list[i] or pd.isna(test_time_column_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_time cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def pass_fail_status_check(self, csv_file):
        """
        pass_fail_status_check
        1. not empty
        2. only can be 'PASS'/'FAIL'
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        pass_fail_status_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["pass_fail_status"]
        )

        for i in range(row_cnt):
            if "" == pass_fail_status_column_list[i] or pd.isna(
                pass_fail_status_column_list[i]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - pass_fail_status cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if (
                "PASS" != pass_fail_status_column_list[i]
                and "FAIL" != pass_fail_status_column_list[i]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - pass_fail_status with illegal content!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def overall_result_check(self, csv_file):
        """
        overall_result_check
        1. not empty
        2. all row with same content
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        overall_result_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["overall_test_result"]
        )

        for i in range(row_cnt):
            if "" == overall_result_column_list[i] or pd.isna(
                overall_result_column_list[i]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - overall_test_result cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if (
                "PASS" != overall_result_column_list[i]
                and "FAIL" != overall_result_column_list[i]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - overall_test_result with illegal content!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and (
                overall_result_column_list[i] != overall_result_column_list[i + 1]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += "Error - overall_test_result with different content in columns!\n"
        self.clear_current_validating_file_error_counters()

    def exit_status_check(self, csv_file):
        """
        exit_status_check
        1. if overall result fail, it should not be zero; pass with exit_status zero
        2. not empty
        3. all exit_status(error_code) should be same
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        overall_result_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["overall_test_result"]
        )

        exit_status_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["exit_status"]
        )

        for i in range(row_cnt):
            overall_result_column_content = overall_result_column_list[i]

            # pandas convert '0' to int64
            exit_status_column_content = exit_status_column_list[i]

            if "" == exit_status_column_list[i] or pd.isna(exit_status_column_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - exit_status cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and (
                exit_status_column_list[i] != exit_status_column_list[i + 1]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - exit_status with different content in columns!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if (overall_result_column_content == "PASS") and (
                exit_status_column_content != 0
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += "Error - exit_status - overall_result 'PASS' but error code not 0!\n"
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if (overall_result_column_content == "FAIL") and (
                exit_status_column_content == 0
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += "Error - exit_status - overall_result 'FAIL' but error code is 0!\n"
        self.clear_current_validating_file_error_counters()

    def test_run_uuid_check(self, csv_file):
        """
        test_run_uuid_check
        1. uuid section length -> 8-4-4-4-12(e.g., E058FB8C-D506-427B-8F1B-D0B03EDB477C)
        2. not empty
        3. all uuid should be same
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)

        test_run_uuid_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["test_run_uuid"]
        )

        # compatible with csv log without test_run_uuid
        # test_run_uuid_column_header = read_csv_cell(
        #     csv_file, 0, self.header_index_dict["test_run_uuid"]
        # )

        # if (
        #     test_run_uuid_column_header
        #     == lyft_csv_format_header[lyft_csv_header_index_dict['test_run_uuid']]
        # ):
        for i in range(row_cnt):
            if "" == test_run_uuid_column_list[i] or pd.isna(
                test_run_uuid_column_list[i]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_run_uuid cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and test_run_uuid_column_list[
                i
            ] != test_run_uuid_column_list[i + 1]:
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_run_uuid with different content in columns!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            test_run_uuid_column_content = test_run_uuid_column_list[i]

            if "" != test_run_uuid_column_list[i] and not pd.isna(
                test_run_uuid_column_list[i]
            ):
                test_run_uuid_column_content_split_list = (
                    test_run_uuid_column_content.split("-")
                )
                for k in range(len(self.length_uuid_section)):
                    if (
                        len(test_run_uuid_column_content_split_list[k])
                        != self.length_uuid_section[k]
                    ):
                        self.current_csv_format_err_counter += 1
                        self.current_validating_file_no_repeat_error_counter += 1
                        if self.current_validating_file_no_repeat_error_counter == 1:
                            self.current_validating_file_result += "Error - test_run_uuid_section - test_run_uuid_section length incorrect!\n"
        self.clear_current_validating_file_error_counters()

    def sn_check(self, csv_file):
        """
        test_run_uuid_check
        1. SN length -> 17: Foxlink SN /16: Solar panel SN
        2. not empty
        3. all SN should be same in the column
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)

        sn_column_list = pd_read_csv_column(csv_file, self.header_index_dict["sn"])

        # compatible with csv log without test_run_uuid
        # sn_column_header = read_csv_cell(csv_file, 0, self.header_index_dict["sn"])
        # if sn_column_header == lyft_csv_format_header[lyft_csv_header_index_dict['sn']]:
        for i in range(row_cnt):
            if "" == sn_column_list[i] or pd.isna(sn_column_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - serial number cell empty!"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and (sn_column_list[i] != sn_column_list[i + 1]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - serial number with different content in columns!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if (
                "FK" not in str(sn_column_list[i])
                and "DEDK" not in str(sn_column_list[i])
                and "fk" not in str(sn_column_list[i])
                and "dedk" not in str(sn_column_list[i])
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - serial number format incorrect!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if len(str(sn_column_list[i])) < 15 or len(str(sn_column_list[i])) > 17:
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - serial number length incorrect!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def date_time_format_valid_check(self, date_time):
        ret_code = 0
        # print(sys._getframe().f_code.co_name)
        if date_time != "" and not pd.isna(date_time):
            date_time_split = date_time.split(" ")
            if len(date_time_split) != 2:
                ret_code = 1
            else:
                date_split = date_time_split[0].split("-")
                if (
                    len(date_split) != 3
                    or len(date_split[0]) != 4
                    or len(date_split[1]) != 2
                    or len(date_split[2]) != 2
                ):
                    ret_code = 2
                else:
                    time_split = date_time_split[1].split(":")
                    if (
                        len(time_split) != 3
                        or len(time_split[0]) != 2
                        or len(time_split[1]) != 2
                        or len(time_split[2]) != 2
                    ):
                        ret_code = 3

        return ret_code

    def start_time_check(self, csv_file):
        """
        start_time_check
        1. date & time exist?
        2. date & time format correct?
        3. all date & time should be same in the column
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        start_time_list = pd_read_csv_column(
            csv_file, self.header_index_dict["start_time"]
        )

        for i in range(row_cnt):
            if "" == start_time_list[i] or pd.isna(start_time_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - start_time cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and (start_time_list[i] != start_time_list[i + 1]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - start_time with different content in columns!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            start_time_column_content = start_time_list[i]
            start_date_time_check_result = self.date_time_format_valid_check(
                start_time_column_content
            )

            if start_date_time_check_result == 1:
                self.current_csv_format_err_counter += 1
                self.current_validating_file_result += (
                    "Error - start_time format error(space_split & length)!\n"
                )
                break
            elif start_date_time_check_result == 2:
                self.current_csv_format_err_counter += 1
                self.current_validating_file_result += (
                    "Error - start_time format error(dash_split & length)!\n"
                )
                break
            elif start_date_time_check_result == 3:
                self.current_csv_format_err_counter += 1
                self.current_validating_file_result += (
                    "Error - start_time format error(colon_split & length)!\n"
                )
                break
        self.clear_current_validating_file_error_counters()

    def end_time_check(self, csv_file):
        """
        end_time_check
        1. date & time exist?
        2. date & time format correct?
        3. all date & time should be same in the column
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        end_time_list = pd_read_csv_column(csv_file, self.header_index_dict["end_time"])

        for i in range(row_cnt):
            if "" == end_time_list[i] or pd.isna(end_time_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - end_time cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and (end_time_list[i] != end_time_list[i + 1]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - end_time with different content in columns!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            end_time_column_content = end_time_list[i]
            end_date_time_check_result = self.date_time_format_valid_check(
                end_time_column_content
            )

            if end_date_time_check_result == 1:
                self.current_csv_format_err_counter += 1
                self.current_validating_file_result += (
                    "Error - end_time format error(space_split & length)!\n"
                )
                break
            elif end_date_time_check_result == 2:
                self.current_csv_format_err_counter += 1
                self.current_validating_file_result += (
                    "Error - end_time format error(dash_split & length)!\n"
                )
                break
            elif end_date_time_check_result == 3:
                self.current_csv_format_err_counter += 1
                self.current_validating_file_result += (
                    "Error - end_time format error(colon_split & length)!\n"
                )
                break
        self.clear_current_validating_file_error_counters()

    def work_order_check(self, csv_file):
        """
        work_order_check
        1. not empty
        2. length > 5
        3. all work_order should be same in the column
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        wo_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["work_order"]
        )

        for i in range(row_cnt):
            if "" == wo_column_list[i] or pd.isna(wo_column_list[i]):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - work_order cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and wo_column_list[i] != wo_column_list[i + 1]:
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - work_order with different content in columns!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if (
                str(wo_column_list[i]) != "8888"
                and str(wo_column_list[i]) != "9999"
                and str(wo_column_list[i]) != "YYYY"
                and len(str(wo_column_list[i])) < 7
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - work_order length incorrect!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def test_station_name_check(self, csv_file):
        """
        test_station_name_check
        1. not empty
        2. all test_station_name should be same in the column
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        test_station_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["test_station_name"]
        )

        for i in range(row_cnt):
            if "" == test_station_column_list[i] or pd.isna(
                test_station_column_list[i]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_station_name cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and (
                test_station_column_list[i] != test_station_column_list[i + 1]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_station_name with different content in columns!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def test_station_id_check(self, csv_file):
        """
        test_station_id_check
        1. not empty
        2. all test_station_id should be same in the column
        """
        # print(sys._getframe().f_code.co_name)
        row_cnt = get_rows_quantity(csv_file)
        test_station_id_column_list = pd_read_csv_column(
            csv_file, self.header_index_dict["test_station_id"]
        )

        for i in range(row_cnt):
            if "" == test_station_id_column_list[i] or pd.isna(
                test_station_id_column_list[i]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_station_id cell empty!\n"
                    )
        self.clear_current_validating_file_error_counters()

        for i in range(row_cnt):
            if ((i + 1) < row_cnt) and (
                test_station_id_column_list[i] != test_station_id_column_list[i + 1]
            ):
                self.current_csv_format_err_counter += 1
                self.current_validating_file_no_repeat_error_counter += 1
                if self.current_validating_file_no_repeat_error_counter == 1:
                    self.current_validating_file_result += (
                        "Error - test_station_id with different content in columns!\n"
                    )
        self.clear_current_validating_file_error_counters()

    def search_csv_log_check_format(self):
        # print(sys._getframe().f_code.co_name)
        file_name_list = os.listdir(self.search_path)
        for fn in file_name_list:
            if re.search(r"\.csv$", fn):
                if fn != validate_result_output_file:
                    full_file_name = os.path.join(self.search_path, fn)

                    # file name recorded into output path
                    self.current_validating_file = fn

                    # file path recorded into output path
                    # self.current_validating_file = full_file_name

                    print(full_file_name)

                    self.file_name_check(full_file_name)

                    row_cnt = get_rows_quantity(full_file_name)
                    if row_cnt > 0:
                        if self.csv_format_header_check(full_file_name):
                            if not wrong_folder_validation:
                                if self.current_csv_format_err_counter > 0:
                                    self.write_output_result_to_csv()
                                    shutil.copy(
                                        full_file_name,
                                        self.category_wrong_csv_format_folder,
                                    )
                                elif self.current_csv_format_err_counter == 0:
                                    shutil.copy(
                                        full_file_name,
                                        self.category_correct_csv_format_folder,
                                    )

                            self.clear_current_file_total_error_counters()
                            self.clear_current_validating_file_list()
                            self.clear_current_validating_file_name()
                            self.clear_current_validating_file_result()
                            continue  # there are some csv log withou test_run_uuid
                        else:
                            self.record_index_check(full_file_name)
                            self.test_name_check(full_file_name)
                            self.lower_limit_check(full_file_name)
                            self.upper_limit_check(full_file_name)
                            self.test_value_check(full_file_name)
                            self.test_time_check(full_file_name)
                            self.pass_fail_status_check(full_file_name)
                            self.overall_result_check(full_file_name)
                            self.exit_status_check(full_file_name)
                            self.test_run_uuid_check(full_file_name)
                            self.sn_check(full_file_name)
                            self.start_time_check(full_file_name)
                            self.end_time_check(full_file_name)
                            self.work_order_check(full_file_name)
                            self.test_station_name_check(full_file_name)
                            self.test_station_id_check(full_file_name)
                    else:
                        # print("Error - row content empty")
                        self.current_csv_format_err_counter += 1
                        self.current_validating_file_result += (
                            "Error - row content empty!\n"
                        )

                    if not wrong_folder_validation:
                        if self.current_csv_format_err_counter > 0:
                            self.write_output_result_to_csv()
                            shutil.copy(
                                full_file_name, self.category_wrong_csv_format_folder
                            )
                        elif self.current_csv_format_err_counter == 0:
                            shutil.copy(
                                full_file_name, self.category_correct_csv_format_folder
                            )

                    self.clear_current_file_total_error_counters()
                    self.clear_current_validating_file_list()
                    self.clear_current_validating_file_name()
                    self.clear_current_validating_file_result()


if __name__ == "__main__":
    if not wrong_folder_validation:
        # PCBA - main_bft
        # monolith_main_bft_csv_validate = lyft_csv_format_validate(
        #     # csv_date_folder
        #     csv_date_folder
        #     + main_bft_csv_path
        # )
        # monolith_main_bft_csv_validate.search_csv_log_check_format()

        # # PCBA - main_flash
        # monolith_main_flash_csv_validate = lyft_csv_format_validate(
        #     csv_date_folder + main_flash_csv_path
        # )
        # monolith_main_flash_csv_validate.search_csv_log_check_format()

        # # PCBA - triangle
        # monolith_triangle_csv_validate = lyft_csv_format_validate(
        #     csv_date_folder + triangle_bft_csv_path
        # )
        # monolith_triangle_csv_validate.search_csv_log_check_format()

        # # cassette - leak
        # monolith_cassette_leak_csv_validate = lyft_csv_format_validate(
        #     csv_date_folder + leak_ft_csv_path
        # )
        # monolith_cassette_leak_csv_validate.search_csv_log_check_format()

        # cassette - ft
        monolith_cassette_ft_csv_validate = lyft_csv_format_validate(
            csv_date_folder + cassette_ft_csv_path
        )
        monolith_cassette_ft_csv_validate.search_csv_log_check_format()

        # receiver - ft
        # monolith_receiver_ft_csv_validate = lyft_csv_format_validate(
        #     csv_date_folder + receiver_ft_csv_path
        # )
        # monolith_receiver_ft_csv_validate.search_csv_log_check_format()

        # bollard - ft
        # monolith_bollard_ft_csv_validate = lyft_csv_format_validate(
        #     csv_date_folder + bollard_ft_csv_path
        # )
        # monolith_bollard_ft_csv_validate.search_csv_log_check_format()

        # solar flat - ft
        # monolith_solar_flat_ft_csv_validate = lyft_csv_format_validate(
        #     csv_date_folder + solar_flat_ft_csv_path
        # )
        # monolith_solar_flat_ft_csv_validate.search_csv_log_check_format()

        # # solar left - ft
        # monolith_solar_left_ft_csv_validate = lyft_csv_format_validate(
        #     csv_date_folder + solar_left_ft_csv_path
        # )
        # monolith_solar_left_ft_csv_validate.search_csv_log_check_format()

        # # solar right - ft
        # monolith_solar_right_ft_csv_validate = lyft_csv_format_validate(
        #     csv_date_folder + solar_right_ft_csv_path
        # )
        # monolith_solar_right_ft_csv_validate.search_csv_log_check_format()
    else:
        ########## wrong format double check ########
        # PCBA - main_bft
        monolith_main_bft_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + main_bft_csv_wrong_path
        )
        monolith_main_bft_csv_wrong_validate.search_csv_log_check_format()

        # PCBA - main_flash
        monolith_main_flash_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + main_flash_csv_wrong_path
        )
        monolith_main_flash_csv_wrong_validate.search_csv_log_check_format()

        # PCBA - triangle
        monolith_triangle_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + triangle_bft_csv_wrong_path
        )
        monolith_triangle_csv_wrong_validate.search_csv_log_check_format()

        # cassette - leak
        monolith_cassette_leak_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + leak_ft_csv_wrong_path
        )
        monolith_cassette_leak_csv_wrong_validate.search_csv_log_check_format()

        # cassette - ft
        monolith_cassette_ft_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + cassette_ft_csv_wrong_path
        )
        monolith_cassette_ft_csv_wrong_validate.search_csv_log_check_format()

        # receiver - ft
        monolith_receiver_ft_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + receiver_ft_csv_wrong_path
        )
        monolith_receiver_ft_csv_wrong_validate.search_csv_log_check_format()

        # bollard - ft
        monolith_bollard_ft_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + bollard_ft_csv_wrong_path
        )
        monolith_bollard_ft_csv_wrong_validate.search_csv_log_check_format()

        # solar flat - ft
        monolith_solar_flat_ft_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + solar_flat_ft_csv_wrong_path
        )
        monolith_solar_flat_ft_csv_wrong_validate.search_csv_log_check_format()

        # solar left - ft
        monolith_solar_left_ft_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + solar_left_ft_csv_wrong_path
        )
        monolith_solar_left_ft_csv_wrong_validate.search_csv_log_check_format()

        # solar right - ft
        monolith_solar_right_ft_csv_wrong_validate = lyft_csv_format_validate(
            csv_date_folder + solar_right_ft_csv_wrong_path
        )
        monolith_solar_right_ft_csv_wrong_validate.search_csv_log_check_format()
