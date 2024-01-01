#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   parametric_data_rule.py
@Time    :   2024/01/01 21:04:02
@Author  :   SimonYuan 
@Version :   1.0
@Site    :   https://tresordie.github.io/
@Desc    :   parametric csv log格式检查, 检查完成后, 输出格式有问题的csv log及细节到csv文件记录, 并将格式有问题的csv log拷贝到指定文件夹下
"""


from csv_operate import *
from collections import Counter
import os
import re
import sys
import shutil


class parametric_data_rule(object):
    """_summary_
        validates if one csv file format legal
    Args:
        object (_type_): _description_
    """

    def __init__(
        self,
        target_validation_folder_path,
        export_file_path,
        error_format_csv_destination_path,
    ):
        # csv files to be validated
        self.target_validation_folder_path = target_validation_folder_path

        self.current_validating_file_fullpath = ""
        self.current_validating_filename = ""
        self.current_validating_file_rows = 0
        self.current_validating_file_columns = 0

        # output result which will be written into output_csv_file
        self.validate_result = ["", ""]

        # export file path & filename
        self.export_file_path = export_file_path

        self.export_file_fullpath = (
            self.export_file_path
            + "parametirc_format_validation_"
            + generate_time_stamp()
            + ".csv"
        )
        self.export_file_header = ["File_Path", "Result", "DRI"]

        creat_csv(self.export_file_fullpath, self.export_file_header)

        # lyft defined standard csv format header
        self.standard_csv_format_header = [
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

        self.standard_csv_format_header_index_dict = {
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

        self.uuid_section_length = [
            8,
            4,
            4,
            4,
            12,
        ]  # E058FB8C-D506-427B-8F1B-D0B03EDB477C

        # generate output folder
        self.error_format_csv_destination_path = error_format_csv_destination_path
        self.mkdir()

    def mkdir(self):
        # print current function name
        # print(sys._getframe().f_code.co_name)
        folder = os.path.exists(self.error_format_csv_destination_path)
        if not folder:
            # print("folder not exist, creating folder!")
            os.makedirs(self.error_format_csv_destination_path)
        # else:
        #     print("folder exist!")

    def get_sn(self):
        tmp_sn = self.self.current_validating_filename.split("_")[2]
        return tmp_sn

    def get_overall_test_result_from_filename(self):
        return self.current_validating_filename.split("_")[1]

    def csv_file_name_check(self):
        """_summary_:
        splitted file name length check

        20230914100738_FAIL_FK2337MCAM3NC0001_
        ['20230914100738', 'FAIL', 'FK2337MCAM3NC0001', '']
        """

        filename = self.current_validating_filename.split(".csv")[0]
        filename_split = filename.split("_")

        if len(filename_split) <= 4:
            self.validate_result[1] += "file name format error\n"

    def csv_head_row_check(self):
        """_summary_
            1. check head row length
            2. check head row content
        Returns:
            _type_: _description_
        """
        head_row_list = pd_read_csv_row(self.current_validating_file_fullpath, 0)

        if len(head_row_list) != len(self.standard_csv_format_header):
            self.validate_result[1] += "head row length mismatch\n"
        else:
            for i in range(len(self.standard_csv_format_header)):
                if head_row_list[i] != self.standard_csv_format_header[i]:
                    # self.validate_result[1] += (
                    #     'head row ' + str(i) + ' content mismatch\n'
                    # )

                    self.validate_result[1] += "head_row[%d] content mismatch\n" % i

    def csv_row_length_check(self, row_index, row_list):
        if len(row_list) != len(self.standard_csv_format_header):
            self.validate_result[1] += "row[%d] length mismatch\n" % row_index

    def csv_row_record_index_check(self, row_index, row_list):
        if row_index != int(row_list[0]):
            self.validate_result[1] += "record_index[%d] number mismatch\n" % row_index

    def csv_row_test_name_check(self, row_index, row_list):
        if not row_list[1]:
            self.validate_result[1] += "row[%d] -- test_name empty\n" % row_index
        else:
            if (
                (" " in row_list[1])
                or ("~" in row_list[1])
                or ("!" in row_list[1])
                or ("@" in row_list[1])
                or ("#" in row_list[1])
                or ("$" in row_list[1])
                or ("%" in row_list[1])
                or ("^" in row_list[1])
                or ("&" in row_list[1])
                or ("*" in row_list[1])
                or ("(" in row_list[1])
                or (")" in row_list[1])
                or ("-" in row_list[1])
                or ("+" in row_list[1])
                or ("=" in row_list[1])
                or ("[" in row_list[1])
                or ("]" in row_list[1])
                or ("{" in row_list[1])
                or ("}" in row_list[1])
                or ("\\" in row_list[1])
                or ("|" in row_list[1])
                or (";" in row_list[1])
                or (":" in row_list[1])
                or ('"' in row_list[1])
                or ("'" in row_list[1])
                or ("," in row_list[1])
                or ("<" in row_list[1])
                or ("." in row_list[1])
                or (">" in row_list[1])
                or ("/" in row_list[1])
                or ("?" in row_list[1])
            ):
                self.validate_result[1] += (
                    "row[%d] -- test_name illegal character\n" % row_index
                )

    def csv_row_lower_limit_check(self, row_index, row_list):
        if not row_list[2]:
            self.validate_result[1] += "row[%d] -- lower_limit empty\n" % row_index

    def csv_row_upper_limit_check(self, row_index, row_list):
        if not row_list[3]:
            self.validate_result[1] += "row[%d] -- upper_limit empty\n" % row_index

    def csv_row_test_value_check(self, row_index, row_list):
        if not row_list[5]:
            self.validate_result[1] += "row[%d] -- test_value empty\n" % row_index

    def csv_row_test_time_check(self, row_index, row_list):
        if not row_list[6]:
            self.validate_result[1] += "row[%d] -- test_time empty\n" % row_index

    def csv_row_pass_fail_status_check(self, row_index, row_list):
        if not row_list[7]:
            self.validate_result[1] += "row[%d] -- pass_fail_status empty\n" % row_index
        else:
            if "PASS" != row_list[7] and "FAIL" != row_list[7]:
                self.validate_result[1] += (
                    "row[%d] -- pass_fail_status with illegal content\n" % row_index
                )

    def csv_row_overall_test_result_check(self, row_index, row_list):
        if not row_list[8]:
            self.validate_result[1] += (
                "row[%d] -- overall_test_result empty\n" % row_index
            )
        else:
            if "PASS" != row_list[8] and "FAIL" != row_list[8]:
                self.validate_result[1] += (
                    'row[%d] -- overall_test_result with illegal content(NOT "PASS" or "FAIL")\n'
                    % row_index
                )

    def csv_row_exit_status_check(self, row_index, row_list):
        if not row_list[9]:
            self.validate_result[1] += "row[%d] -- exit_status empty\n" % row_index
        else:
            if not row_list[9].isdigit():
                self.validate_result[1] += (
                    "row[%d] -- exit_status is NOT digital numbers\n" % row_index
                )
            elif "PASS" == row_list[8] and "0" != row_list[9]:
                self.validate_result[1] += (
                    "row[%d] -- exit_status is NOT 0 when overall_test_result pass\n"
                    % row_index
                )
            elif "FAIL" == row_list[8] and "0" == row_list[9]:
                self.validate_result[1] += (
                    "row[%d] -- exit_status is 0 when overall_test_result fail\n"
                    % row_index
                )

    def csv_row_test_run_uuid_check(self, row_index, row_list):
        if not row_list[10]:
            self.validate_result[1] += "row[%d] -- test_run_uuid empty\n" % row_index
        else:
            uuid_split_list = row_list[10].split("-")
            for i in range(len(uuid_split_list)):
                if not uuid_split_list[i].isalnum():
                    self.validate_result[1] += (
                        "row[%d] -- test_run_uuid section[%d] content is NOT alpha & numbers\n"
                        % (row_index, i)
                    )

                if len(uuid_split_list[i]) != self.uuid_section_length[i]:
                    self.validate_result[1] += (
                        "row[%d] -- test_run_uuid section[%d] with error length(current length is %d, expected: %d)\n"
                        % (
                            row_index,
                            i,
                            len(uuid_split_list[i]),
                            self.uuid_section_length[i],
                        )
                    )

    def csv_row_sn_check(self, row_index, row_list):
        if not row_list[11]:
            self.validate_result[1] += "row[%d] -- sn empty\n" % row_index
        else:
            if not row_list[11].isalnum():
                self.validate_result[
                    1
                ] += "row[%d] -- sn content is NOT alpha & numbers\n" % (row_index)

            if len(row_list[11]) < 15 or len(row_list[11]) > 17:
                self.validate_result[1] += (
                    "row[%d] -- sn length error(current length: %d, expected: 15~17)\n"
                    % (row_index, len(row_list[11]))
                )

    def csv_row_start_time_check(self, row_index, row_list):
        if row_list[12]:
            date_time_split = row_list[12].split(" ")
            if len(date_time_split) != 2:
                self.validate_result[
                    1
                ] += "row[%d] -- start_time(%s) date/time missing\n" % (
                    row_index,
                    row_list[12],
                )
            else:
                date_split = date_time_split[0].split("-")
                if (
                    len(date_split) != 3
                    or len(date_split[0]) != 4
                    or len(date_split[1]) != 2
                    or len(date_split[2]) != 2
                    or not date_split[0].isdigit()
                    or not date_split[1].isdigit()
                    or not date_split[2].isdigit()
                ):
                    self.validate_result[
                        1
                    ] += "row[%d] -- start_time: date(%s) content error\n" % (
                        row_index,
                        date_time_split[0],
                    )

                time_split = date_time_split[1].split(":")
                if (
                    len(time_split) != 3
                    or len(time_split[0]) != 2
                    or len(time_split[1]) != 2
                    or len(time_split[2]) != 2
                    or not time_split[0].isdigit()
                    or not time_split[1].isdigit()
                    or not time_split[2].isdigit()
                ):
                    self.validate_result[
                        1
                    ] += "row[%d] -- start_time: time(%s) content error\n" % (
                        row_index,
                        date_time_split[1],
                    )
        else:
            self.validate_result[1] += "row[%d] -- start_time empty\n" % row_index

    def csv_row_end_time_check(self, row_index, row_list):
        if row_list[13]:
            date_time_split = row_list[13].split(" ")
            if len(date_time_split) != 2:
                self.validate_result[
                    1
                ] += "row[%d] -- end_time(%s) date/time missing\n" % (
                    row_index,
                    row_list[13],
                )
            else:
                date_split = date_time_split[0].split("-")
                if (
                    len(date_split) != 3
                    or len(date_split[0]) != 4
                    or len(date_split[1]) != 2
                    or len(date_split[2]) != 2
                    or not date_split[0].isdigit()
                    or not date_split[1].isdigit()
                    or not date_split[2].isdigit()
                ):
                    self.validate_result[
                        1
                    ] += "row[%d] -- end_time: date(%s) content error\n" % (
                        row_index,
                        date_time_split[0],
                    )

                time_split = date_time_split[1].split(":")
                if (
                    len(time_split) != 3
                    or len(time_split[0]) != 2
                    or len(time_split[1]) != 2
                    or len(time_split[2]) != 2
                    or not time_split[0].isdigit()
                    or not time_split[1].isdigit()
                    or not time_split[2].isdigit()
                ):
                    self.validate_result[
                        1
                    ] += "row[%d] -- end_time: time(%s) content error\n" % (
                        row_index,
                        date_time_split[1],
                    )
        else:
            self.validate_result[1] += "row[%d] -- end_time empty\n" % row_index

    def csv_row_work_order_check(self, row_index, row_list):
        if not row_list[14]:
            self.validate_result[1] += "row[%d] -- work_order empty\n" % row_index
        else:
            if not row_list[14].isalnum():
                self.validate_result[
                    1
                ] += "row[%d] -- work_order(%s) with illegal character\n" % (
                    row_index,
                    row_list[14],
                )
            elif len(row_list[14]) < 8:
                self.validate_result[
                    1
                ] += "row[%d] -- work_order(%s) with error length\n" % (
                    row_index,
                    row_list[14],
                )

    def csv_row_test_station_name_check(self, row_index, row_list):
        if not row_list[15]:
            self.validate_result[1] += (
                "row[%d] -- test_station_name empty\n" % row_index
            )
        else:
            station_name_split = row_list[15].split("_")
            for i in range(len(station_name_split)):
                if not station_name_split[i].isalpha():
                    self.validate_result[1] += (
                        "row[%d] -- test_station_name(%s): [%s] with illegal character\n"
                        % (row_index, row_list[15], station_name_split[i])
                    )

    def csv_row_test_station_id_check(self, row_index, row_list):
        if not row_list[16]:
            self.validate_result[1] += "row[%d] -- test_station_id empty\n" % row_index
        elif not row_list[16].isdigit():
            self.validate_result[1] += (
                "row[%d] -- test_station_id(%s) with illegal content(NOT Digitals)\n"
                % (
                    row_index,
                    row_list[16],
                )
            )

    def csv_rows_content_check(self):
        """_summary_
        check if all rows contents' format
        """
        for i in range(1, self.current_validating_file_rows):
            row_list = pd_read_csv_row(self.current_validating_file_fullpath, i)
            self.csv_row_length_check(i, row_list)

            self.csv_row_record_index_check(i, row_list)
            self.csv_row_test_name_check(i, row_list)
            self.csv_row_lower_limit_check(i, row_list)
            self.csv_row_upper_limit_check(i, row_list)
            self.csv_row_test_value_check(i, row_list)
            self.csv_row_test_time_check(i, row_list)
            self.csv_row_pass_fail_status_check(i, row_list)
            self.csv_row_overall_test_result_check(i, row_list)
            self.csv_row_exit_status_check(i, row_list)
            self.csv_row_test_run_uuid_check(i, row_list)
            self.csv_row_sn_check(i, row_list)
            self.csv_row_start_time_check(i, row_list)
            self.csv_row_end_time_check(i, row_list)
            self.csv_row_work_order_check(i, row_list)
            self.csv_row_test_station_name_check(i, row_list)
            self.csv_row_test_station_id_check(i, row_list)

    def csv_column_pass_fail_status_check(self, column_index, column_list):
        """_summary_
            check if StopOnFail

        Args:
            column_index (string): column index of parametric data
            column_list (string): column list of parametric data
        """
        if "PASS" == self.get_overall_test_result_from_filename():
            for i in range(1, self.current_validating_file_rows):
                if column_list[i] != "PASS":
                    self.validate_result[1] += (
                        "column[%d] -- pass_fail_status: row[%d] NOT match overall_test_result(PASS)\n"
                        % (column_index, i)
                    )
        elif "FAIL" == self.get_overall_test_result_from_filename():
            counter_items_in_column_list = Counter(column_list)

            if counter_items_in_column_list["FAIL"] == 0:
                self.validate_result[1] += (
                    'column[%d] -- pass_fail_status all items "PASS"(overall_result: "FAIL")\n'
                    % (column_index)
                )
            elif counter_items_in_column_list["FAIL"] > 1:
                self.validate_result[1] += (
                    "column[%d] -- pass_fail_status with multi-items fail(NOT StopOnFail)\n"
                    % (column_index)
                )
        else:
            self.validate_result[
                1
            ] += "column[%d] -- pass_fail_status with illegal PASS/FAIL characters\n" % (
                column_index
            )

    def csv_column_overall_test_result_check(self, column_index, column_list):
        column_list_set = list(set(column_list))

        if len(column_list_set) != 1:
            self.validate_result[1] += (
                "column[%d] -- overall_test_result with multiple test result(expected padding with same content)\n"
                % (column_index)
            )
        elif column_list_set[0] != self.get_overall_test_result_from_filename():
            self.validate_result[1] += (
                "column[%d] -- overall_test_result with illegal PASS/FAIL characters\n"
                % (column_index)
            )

    def csv_column_exit_status_check(self, column_index, column_list):
        column_list_set = list(set(column_list))

        if len(column_list_set) != 1:
            self.validate_result[1] += (
                "column[%d] -- exit_status with multiple error code(expected padding with same content)\n"
                % (column_index)
            )
        else:
            if not column_list_set[0].isdigit():
                self.validate_result[
                    1
                ] += "column[%d] -- exit_status DataType error(expected digitals)\n" % (
                    column_index
                )
            else:
                if (
                    "PASS" == self.get_overall_test_result_from_filename()
                    and int(column_list_set[0]) != 0
                ):
                    self.validate_result[1] += (
                        "column[%d] -- exit_status value error(expected error_code: 0)\n"
                        % (column_index)
                    )
                elif (
                    "FAIL" == self.get_overall_test_result_from_filename()
                    and int(column_list_set[0]) == 0
                ):
                    self.validate_result[1] += (
                        "column[%d] -- exit_status value error(expected error_code: NON-ZERO)\n"
                        % (column_index)
                    )

    def csv_column_test_run_uuid_check(self, column_index, column_list):
        column_list_set = list(set(column_list))

        if len(column_list_set) != 1:
            self.validate_result[1] += (
                "column[%d] -- test_run_uuid with multiple value(expected padding with same content)\n"
                % (column_index)
            )

    def csv_column_sn_check(self, column_index, column_list):
        column_list_set = list(set(column_list))

        if len(column_list_set) != 1:
            self.validate_result[1] += (
                "column[%d] -- sn with multiple value(expected padding with same content)\n"
                % (column_index)
            )

    def csv_column_start_time_check(self, column_index, column_list):
        column_list_set = list(set(column_list))

        if len(column_list_set) != 1:
            self.validate_result[1] += (
                "column[%d] -- start_time with multiple value(expected padding with same content)\n"
                % (column_index)
            )

    def csv_column_end_time_check(self, column_index, column_list):
        column_list_set = list(set(column_list))

        if len(column_list_set) != 1:
            self.validate_result[1] += (
                "column[%d] -- end_time with multiple value(expected padding with same content)\n"
                % (column_index)
            )

    def csv_column_work_order_check(self, column_index, column_list):
        column_list_set = list(set(column_list))

        if len(column_list_set) != 1:
            self.validate_result[1] += (
                "column[%d] -- work_order with multiple value(expected padding with same content)\n"
                % (column_index)
            )

    def csv_column_test_station_name_check(self, column_index, column_list):
        column_list_set = list(set(column_list))

        if len(column_list_set) != 1:
            self.validate_result[1] += (
                "column[%d] -- test_station_name with multiple value(expected padding with same content)\n"
                % (column_index)
            )

    def csv_column_test_station_id_check(self, column_index, column_list):
        column_list_set = list(set(column_list))

        if len(column_list_set) != 1:
            self.validate_result[1] += (
                "column[%d] -- test_station_id with multiple value(expected padding with same content)\n"
                % (column_index)
            )

    def csv_columns_content_check(self):
        """_summary_
        check if all columns contents' format
        """
        # pass_fail_status
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["pass_fail_status"],
        )
        self.csv_column_pass_fail_status_check(
            self.standard_csv_format_header_index_dict["pass_fail_status"], column_list
        )

        # overall_test_result
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["overall_test_result"],
        )
        column_list.pop(0)

        self.csv_column_overall_test_result_check(
            self.standard_csv_format_header_index_dict["overall_test_result"],
            column_list,
        )

        # exit_status
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["exit_status"],
        )
        column_list.pop(0)

        self.csv_column_exit_status_check(
            self.standard_csv_format_header_index_dict["exit_status"], column_list
        )

        # test_run_uuid
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["test_run_uuid"],
        )
        column_list.pop(0)

        self.csv_column_test_run_uuid_check(
            self.standard_csv_format_header_index_dict["test_run_uuid"], column_list
        )

        # sn
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["sn"],
        )
        column_list.pop(0)

        self.csv_column_sn_check(
            self.standard_csv_format_header_index_dict["sn"], column_list
        )

        # start_time
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["start_time"],
        )
        column_list.pop(0)

        self.csv_column_start_time_check(
            self.standard_csv_format_header_index_dict["start_time"], column_list
        )

        # end_time
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["end_time"],
        )
        column_list.pop(0)

        self.csv_column_end_time_check(
            self.standard_csv_format_header_index_dict["end_time"], column_list
        )

        # work_order
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["work_order"],
        )
        column_list.pop(0)

        self.csv_column_work_order_check(
            self.standard_csv_format_header_index_dict["work_order"], column_list
        )

        # test_station_name
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["test_station_name"],
        )
        column_list.pop(0)

        self.csv_column_test_station_name_check(
            self.standard_csv_format_header_index_dict["test_station_name"], column_list
        )

        # test_station_id
        column_list = pd_read_csv_column(
            self.current_validating_file_fullpath,
            self.standard_csv_format_header_index_dict["test_station_id"],
        )
        column_list.pop(0)

        self.csv_column_test_station_id_check(
            self.standard_csv_format_header_index_dict["test_station_id"], column_list
        )

    def parametric_format_validation(self):
        file_name_list = os.listdir(self.target_validation_folder_path)

        # ['20231220163854_FAIL_FK2348MFAT3AA0002_monolith_bollard_ft.csv', '20231220163854_FAIL_FK2348MFAT3AA0002_monolith_bollard_ft.txt']
        for fn in file_name_list:
            if re.search(r"\.csv$", fn):
                self.current_validating_filename = fn
                self.validate_result[0] = self.current_validating_filename

                # full_file_path
                self.current_validating_file_fullpath = os.path.join(
                    self.target_validation_folder_path, fn
                )
                print(self.current_validating_file_fullpath)

                self.current_validating_file_rows = get_rows_quantity(
                    self.current_validating_file_fullpath
                )
                self.current_validating_file_columns = get_columns_quantity(
                    self.current_validating_file_fullpath
                )

                self.csv_file_name_check()
                self.csv_head_row_check()

                if self.current_validating_file_rows > 1:
                    self.csv_rows_content_check()
                    self.csv_columns_content_check()

                if self.validate_result[1]:
                    write_row_to_csv(self.validate_result, self.export_file_fullpath)
                    shutil.copy(
                        self.current_validating_file_fullpath,
                        self.error_format_csv_destination_path,
                    )

                print(sys._getframe().f_code.co_name)
                print(self.validate_result)
                print("\n")

                self.current_validating_file_fullpath = ""
                self.current_validating_filename = ""
                self.current_validating_file_rows = 0
                self.current_validating_file_columns = 0
                self.validate_result = ["", ""]


if __name__ == "__main__":
    parametric_data_rule = parametric_data_rule(
        "./monolith_pvt_aws20231227", "./", "./20231228_asw_csv_check"
    )

    parametric_data_rule.parametric_format_validation()
