import os
import time

from config.get_config import get_config
from download.download_single_case import download_single_case
from download.package_data import get_all_record_by_params

# v1
# if __name__ == '__main__':
#     cf = configparser.ConfigParser()
#     cf.read("conf/config.ini")
#     url_prefix = cf.get("core", "url_prefix")
#     # 创建的目录
#     path = "all_record"
#     if not os.path.exists(path):
#         os.mkdir(path)
#     all_bad_case = get_all_record_by_params("10.199.1.210", 3306, "root", "W.R3elungNq", "megcity", "")
#     executor = ThreadPoolExecutor(max_workers=8)
#     all_task = [executor.submit(download_single_case(url_prefix, path, bad_case)) for bad_case in all_bad_case]
#     wait(all_task, return_when=ALL_COMPLETED)


if __name__ == '__main__':
    config_dict = get_config()
    path = "all_record"
    if not os.path.exists(path):
        os.mkdir(path)
    start_time = config_dict.get("start_time")
    end_time = config_dict.get("end_time")
    alarm_type = config_dict.get("type")
    sql_where = " where create_time > '{}' and create_time < '{}' ".format(start_time, end_time)
    if alarm_type:
        type_array = alarm_type.split(",", -1)
        alarm_type_str = ','.join(["'%s'" % item for item in type_array])
        sql_where = sql_where + ' and type in ({})'.format(alarm_type_str)
    all_bad_case = get_all_record_by_params(config_dict.get('mariadb_host'), int(config_dict.get('mariadb_port')),
                                            config_dict.get('mariadb_user'), config_dict.get('mariadb_pwd'),
                                            config_dict.get('mariadb_db'), sql_where)
    for bad_case in all_bad_case:
        s = time.time()
        print("start download {} , now : {}".format(bad_case.get('case_number'),
                                                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        download_single_case(config_dict.get('url_prefix'), path, bad_case)
        e = time.time()
        print("end download {}, cost {} ".format(bad_case.get('case_number'), str(e - s)))
    os.system('pause')
