# csv_format_check
check csv_format meet requirements


2023-06-28

Initial release: drafted script as a basic check for csv log format


2023-06-30
1. there are some issue when using csv lib, now changed to use pandas
2. fix some bugs to compatible all test stations csv log parse
3. add wrong csv format log validate separately


2023-12-26

1. re-write script to check parametric data format
2. the script had been tested with manually error injection, will use in generally
![](https://raw.githubusercontent.com/Tresordie/PicBed/master/csv_format_check_scripts_request.excalidraw.png)


2024-05-08

1. For padding data check, just show error of one row because all padding same


2024-06-02
1. optimized to check one time for all padding items