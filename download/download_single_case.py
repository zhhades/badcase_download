import json
import os
import zipfile
from datetime import date, datetime

import requests as req


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def download_file(url, path, case_number, suffix):
    try:
        response = req.get(url)
        data = response.content
        if data:
            file_path = '{}/{}.{}'.format(path, case_number, suffix)
            print('文件为:' + file_path)
            if not os.path.exists(file_path):
                with open(file_path, 'wb')as f:
                    f.write(data)
                    f.close()
                    print('案件 {} 压缩包下载成功:{}'.format(case_number, url))
                return file_path
    except Exception as e:
        print(e)
        print('案件 {} 压缩包下载失败:{}'.format(case_number, url))


def save_alarm_info(path, bad_case):
    case_number = bad_case['case_number']
    with open(path + "\\" + case_number + ".json", 'a') as alarm_file:
        alarm_file.write(json.dumps(bad_case, cls=ComplexEncoder))


def download_single_case(url_prefix, parent_path, bad_case):
    case_number = bad_case['case_number']
    # 创建案件目录
    # path = parent_path + "/" + case_number
    path = parent_path
    if not os.path.exists(path):
        os.mkdir(path)
    # 下载案件压缩包
    download_file(url_prefix.format(bad_case['zip_uri'], case_number + ".tar.gz"), path, case_number, "tar.gz")
    # save_alarm_info(path, bad_case)
    # make_zip(path, parent_path, case_number + ".zip")
    # shutil.rmtree(path)


def make_zip(source_dir, parent_path, output_filename):
    zip_f = zipfile.ZipFile(parent_path + "\\" + output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dir_names, file_names in os.walk(source_dir):
        for file_name in file_names:
            path_file = os.path.join(parent, file_name)
            arc_name = path_file[pre_len:].strip(os.path.sep)
            zip_f.write(path_file, arc_name)
    zip_f.close()

    return output_filename
