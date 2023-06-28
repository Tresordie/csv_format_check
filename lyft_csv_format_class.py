# !usr/bin/env python
# -*- coding:utf-8 -*-

from csv_operate import *
import os
import re
import shutil

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


class lyft_csv_format_validate(object):
    def __init__(self, csv_files_folder_path):
        self.search_path = csv_files_folder_path
        self.csv_header = lyft_csv_format_header
        self.header_index_dict = lyft_csv_header_index_dict
        self.current_csv_format_err_counter = 0
        self.length_uuid_section = [
            8,
            4,
            4,
            4,
            12,
        ]  # E058FB8C-D506-427B-8F1B-D0B03EDB477C
        self.category_correct_csv_format_folder = os.path.join(os.getcwd(), "correct")
        self.mkdir(self.category_correct_csv_format_folder)
        self.category_wrong_csv_format_folder = os.path.join(os.getcwd(), "wrong")
        self.mkdir(self.category_wrong_csv_format_folder)

    def mkdir(self, path):
        folder = os.path.exists(path)
        if not folder:
            # print("folder not exist, creating folder!")
            os.makedirs(path)
        else:
            print("folder exist!")

    def csv_header_check(self, csv_file):
        """
        check if csv file header same as Lyft pre-defined
        """
        csv_header_read = read_csv_head(csv_file)

        if len(csv_header_read) != len(self.csv_header):
            print("Error - csv_header length mismatch!")
            self.current_csv_format_err_counter += 1

        for i in range(0, len(self.csv_header)):
            if csv_header_read[i] != self.csv_header[i]:
                print("Error - csv_header[%d]: %s" % (i, csv_header_read[i]))
                self.current_csv_format_err_counter += 1

    def record_index_check(self, csv_file):
        """
        check if record_index valid
        1. not empty
        2. increased by 1
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            record_index_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["record_index"]
            )

            record_index_column_content = record_index_column_list[1]
            if record_index_column_content != "1":
                print("Error - record_index[1] not equal 1")
                self.current_csv_format_err_counter += 1

            for i in range(1, row_cnt + 1):
                # record_index content is empty?
                if "" == record_index_column_list[i]:
                    print(
                        "Error - record_index[%d] empty: %s"
                        % (i, record_index_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1
                # record_index increased by 1?
                elif ((i + 1) < (row_cnt + 1)) and (
                    "" != record_index_column_list[i + 1]
                ):
                    if (int(record_index_column_list[i]) + 1) != int(
                        record_index_column_list[i + 1]
                    ):
                        print("Error - record_index[%d] not increased by 1" % (i + 1))
                        self.current_csv_format_err_counter += 1

    def test_name_check(self, csv_file):
        """
        check if test_name valid
        1. not empty
        2. no illegal character in test_name(e.g., @#!~%^&*_+/)
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            test_name_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["test_name"]
            )
            for i in range(1, row_cnt + 1):
                # test_name empty?
                if "" == test_name_column_list[i]:
                    print("Error - test_name[%d] empty" % i)
                    self.current_csv_format_err_counter += 1

                # any illegal character?
                elif (
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
                    print(
                        "Error - illegal character in test_name[%d]: %s"
                        % (i, test_name_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1

    def lower_limit_check(self, csv_file):
        """
        lower_limit check
        1. only check not empty, must have criteria (PASS/Fail or value)
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            lower_limit_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["lower_limit"]
            )

            for i in range(1, row_cnt + 1):
                if "" == lower_limit_column_list[i]:
                    print("Error - low_limit[%d] cell empty" % i)
                    self.current_csv_format_err_counter += 1

    def upper_limit_check(self, csv_file):
        """
        upper_limit check
        1. only check not empty, must have criteria (PASS/Fail or value)
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            upper_limit_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["upper_limit"]
            )

            for i in range(1, row_cnt + 1):
                if "" == upper_limit_column_list[i]:
                    print("Error - upper_limit[%d] cell empty" % i)
                    self.current_csv_format_err_counter += 1

    def test_value_check(self, csv_file):
        """
        test_value check
        1. only check not empty, must have criteria (PASS/Fail or value)
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            test_value_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["test_value"]
            )
            for i in range(1, row_cnt + 1):
                if "" == test_value_column_list[i]:
                    print("Error - test_value[%d] cell empty" % i)
                    self.current_csv_format_err_counter += 1

    def test_time_check(self, csv_file):
        """
        test_time check
        1. only check not empty, must have criteria (PASS/Fail or value)
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            test_time_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["test_time"]
            )
            for i in range(1, row_cnt + 1):
                if "" == test_time_column_list[i]:
                    print("Error - test_time[%d] cell empty" % i)
                    self.current_csv_format_err_counter += 1

    def pass_fail_status_check(self, csv_file):
        """
        pass_fail_status_check
        1. not empty
        2. only can be 'PASS'/'FAIL'
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            pass_fail_status_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["pass_fail_status"]
            )
            for i in range(1, row_cnt + 1):
                if "" == pass_fail_status_column_list[i]:
                    print("Error - pass_fail_status[%d] cell empty" % i)
                    self.current_csv_format_err_counter += 1
                elif (
                    "PASS" != pass_fail_status_column_list[i]
                    and "FAIL" != pass_fail_status_column_list[i]
                ):
                    print(
                        "Error - pass_fail_status[%d]: %s - content illegal"
                        % (i, pass_fail_status_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1

    def overall_result_check(self, csv_file):
        """
        overall_result_check
        1. not empty
        2. all row with same content
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            overall_result_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["overall_test_result"]
            )

            for i in range(1, row_cnt + 1):
                if "" == overall_result_column_list[i]:
                    print("Error - overall_test_result[%d]: empty" % i)
                    self.current_csv_format_err_counter += 1
                elif (
                    "PASS" != overall_result_column_list[i]
                    and "FAIL" != overall_result_column_list[i]
                ):
                    print(
                        "Error - overall_test_result[%d]: %s - content illegal"
                        % (i, overall_result_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1
                else:
                    if (i < row_cnt) and overall_result_column_list[
                        i
                    ] != overall_result_column_list[i + 1]:
                        print(
                            "Error - overall_test_result[%d]: %s - content different in column"
                            % (i, overall_result_column_list[i])
                        )
                        self.current_csv_format_err_counter += 1

    def exit_status_check(self, csv_file):
        """
        exit_status_check
        1. if overall result fail, it should not be zero; pass with exit_status zero
        2. not empty
        3. all exit_status(error_code) should be same
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            overall_result_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["overall_test_result"]
            )

            exit_status_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["exit_status"]
            )

            for i in range(1, row_cnt + 1):
                overall_result_column_content = overall_result_column_list[i]
                exit_status_column_content = exit_status_column_list[i]

                if "" == exit_status_column_list[i]:
                    print(
                        "Error - exit_status[%d]: %s - content empty"
                        % (i, exit_status_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1
                elif (i < row_cnt) and exit_status_column_list[
                    i
                ] != exit_status_column_list[i + 1]:
                    print(
                        "Error - exit_status[%d]: %s - content different in column"
                        % (i, exit_status_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1

                if (
                    overall_result_column_content == "PASS"
                    and exit_status_column_content != "0"
                ):
                    print(
                        "Error - exit_status[1]: %s - overall_result 'PASS' but error code not 0"
                        % exit_status_column_content
                    )
                    self.current_csv_format_err_counter += 1
                elif (
                    overall_result_column_content == "FAIL"
                    and exit_status_column_content == "0"
                ):
                    print(
                        "Error - exit_status[1]: %s - overall_result 'FAIL' but error code is 0"
                        % exit_status_column_content
                    )
                    self.current_csv_format_err_counter += 1

    def test_run_uuid_check(self, csv_file):
        """
        test_run_uuid_check
        1. uuid section length -> 8-4-4-4-12(e.g., E058FB8C-D506-427B-8F1B-D0B03EDB477C)
        2. not empty
        3. all uuid should be same
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            test_run_uuid_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["test_run_uuid"]
            )

            for i in range(1, row_cnt + 1):
                test_run_uuid_column_content = test_run_uuid_column_list[i]
                test_run_uuid_column_content_split_list = (
                    test_run_uuid_column_content.split("-")
                )

                if "" == test_run_uuid_column_list[i]:
                    print(
                        "Error - test_run_uuid[%d]: %s - content empty"
                        % (i, test_run_uuid_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1
                elif (i < row_cnt) and test_run_uuid_column_list[
                    i
                ] != test_run_uuid_column_list[i + 1]:
                    print(
                        "Error - test_run_uuid[%d]: %s - content different in column"
                        % (i, test_run_uuid_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1

                for k in range(len(self.length_uuid_section)):
                    if (
                        len(test_run_uuid_column_content_split_list[k])
                        != self.length_uuid_section[k]
                    ):
                        print(
                            "Error - test_run_uuid_section[%d] length: %d vs %d - test_run_uuid_section length incorrect"
                            % (
                                k,
                                len(test_run_uuid_column_content_split_list[k]),
                                self.length_uuid_section[k],
                            )
                        )
                        self.current_csv_format_err_counter += 1

    def sn_check(self, csv_file):
        """
        test_run_uuid_check
        1. SN length -> 17: Foxlink SN /16: Solar panel SN
        2. not empty
        3. all SN should be same in the column
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            sn_column_list = read_csv_one_column(csv_file, self.header_index_dict["sn"])
            sn_column_content = sn_column_list[1]

            for i in range(1, row_cnt + 1):
                if "" == sn_column_list[i]:
                    print("Error - sn[%d]: %s - sn empty" % (i, sn_column_list[i]))
                    self.current_csv_format_err_counter += 1
                elif (i < row_cnt) and sn_column_list[i] != sn_column_list[i + 1]:
                    print(
                        "Error - sn[%d]: %s - sn different in column"
                        % (i, sn_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1
                if len(sn_column_list[i]) < 15:
                    print(
                        "Error - sn[%d]: %s - sn length incorrect"
                        % (i, sn_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1

    def date_time_format_valid_check(self, date_time):
        ret_code = 0
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
        row_cnt = get_rows_quantity(csv_file)

        if row_cnt > 0:
            start_time_list = read_csv_one_column(
                csv_file, self.header_index_dict["start_time"]
            )

            for i in range(1, row_cnt + 1):
                if "" == start_time_list[i]:
                    print("Error: start_time[%d] date_time empty" % i)
                    self.current_csv_format_err_counter += 1
                elif (i < row_cnt) and start_time_list[i] != start_time_list[i + 1]:
                    print(
                        "Error: start_time[%d]: %s date_time different in column"
                        % (i, start_time_column_content)
                    )
                    self.current_csv_format_err_counter += 1

                start_time_column_content = start_time_list[i]

                start_date_time_check_result = self.date_time_format_valid_check(
                    start_time_column_content
                )
                if start_date_time_check_result == 1:
                    print(
                        "Error: start_time[%d]: %s format error(space_split & length)"
                        % (i, start_time_column_content)
                    )
                    self.current_csv_format_err_counter += 1
                elif start_date_time_check_result == 2:
                    print(
                        "Error: start_time[%d]: %s format error(dash_split & length)"
                        % (i, start_time_column_content)
                    )
                    self.current_csv_format_err_counter += 1
                elif start_date_time_check_result == 3:
                    print(
                        "Error: start_time[%d]: %s format error(colon_split & length)"
                        % (i, start_time_column_content)
                    )
                    self.current_csv_format_err_counter += 1

    def end_time_check(self, csv_file):
        """
        end_time_check
        1. date & time exist?
        2. date & time format correct?
        3. all date & time should be same in the column
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            end_time_list = read_csv_one_column(
                csv_file, self.header_index_dict["end_time"]
            )

            for i in range(1, row_cnt + 1):
                if "" == end_time_list[i]:
                    print("Error: end_time[%d] date_time empty" % i)
                    self.current_csv_format_err_counter += 1
                elif (i < row_cnt) and end_time_list[i] != end_time_list[i + 1]:
                    print(
                        "Error: end_time[%d]: %s date_time different in column"
                        % (i, end_time_list[i])
                    )
                    self.current_csv_format_err_counter += 1

                end_time_column_content = end_time_list[i]
                end_date_time_check_result = self.date_time_format_valid_check(
                    end_time_column_content
                )

                if end_date_time_check_result == 1:
                    print(
                        "Error: end_time[%d]: %s format error(space_split & length)"
                        % (i, end_time_column_content)
                    )
                    self.current_csv_format_err_counter += 1
                elif end_date_time_check_result == 2:
                    print(
                        "Error: end_time[%d]: %s format error(dash_split & length)"
                        % (i, end_time_column_content)
                    )
                    self.current_csv_format_err_counter += 1
                elif end_date_time_check_result == 3:
                    print(
                        "Error: end_time[%d]: %s format error(colon_split & length)"
                        % (i, end_time_column_content)
                    )
                    self.current_csv_format_err_counter += 1

    def work_order_check(self, csv_file):
        """
        work_order_check
        1. not empty
        2. length > 5
        3. all work_order should be same in the column
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            wo_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["work_order"]
            )

            for i in range(1, row_cnt + 1):
                if "" == wo_column_list[i]:
                    print("Error: work_order[%d] empty" % i)
                    self.current_csv_format_err_counter += 1
                elif (i < row_cnt) and wo_column_list[i] != wo_column_list[i + 1]:
                    print(
                        "Error: work_order[%d]: %s content different"
                        % (i, wo_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1

                if len(wo_column_list[i]) < 10:
                    # if i == row_cnt:
                    print(
                        "Error: work_order[%d]: %s length incorrect"
                        % (i, wo_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1

    def test_station_name_check(self, csv_file):
        """
        test_station_name_check
        1. not empty
        2. all test_station_name should be same in the column
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            test_station_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["test_station_name"]
            )

            for i in range(1, row_cnt + 1):
                if "" == test_station_column_list[i]:
                    print("Error: test_station_name[%d] empty" % i)
                    self.current_csv_format_err_counter += 1
                elif (i < row_cnt) and test_station_column_list[
                    i
                ] != test_station_column_list[i + 1]:
                    print(
                        "Error: test_station_name[%d]: %s content different"
                        % (i, test_station_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1

    def test_station_id_check(self, csv_file):
        """
        test_station_id_check
        1. not empty
        2. all test_station_id should be same in the column
        """
        row_cnt = get_rows_quantity(csv_file)
        if row_cnt > 0:
            test_station_id_column_list = read_csv_one_column(
                csv_file, self.header_index_dict["test_station_id"]
            )

            for i in range(1, row_cnt + 1):
                if "" == test_station_id_column_list[i]:
                    print("Error: test_station_id[%d] empty" % i)
                    self.current_csv_format_err_counter += 1
                elif (i < row_cnt) and test_station_id_column_list[
                    i
                ] != test_station_id_column_list[i + 1]:
                    print(
                        "Error: test_station_id[%d]: %s content different"
                        % (i, test_station_id_column_list[i])
                    )
                    self.current_csv_format_err_counter += 1

    def search_csv_log_check_format(self):
        file_name_list = os.listdir(self.search_path)
        for fn in file_name_list:
            if re.search(r"\.csv$", fn):
                full_file_name = os.path.join(self.search_path, fn)
                print(full_file_name)

                self.csv_header_check(full_file_name)
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

                if self.current_csv_format_err_counter > 0:
                    shutil.copy(full_file_name, self.category_wrong_csv_format_folder)
                elif self.current_csv_format_err_counter == 0:
                    shutil.copy(full_file_name, self.category_correct_csv_format_folder)
                self.current_csv_format_err_counter = 0


if __name__ == "__main__":
    monolith_csv_validate = lyft_csv_format_validate("./monolith_charging_main_bft/CSV")
    monolith_csv_validate.search_csv_log_check_format()
