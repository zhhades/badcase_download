import configparser


def get_config():
    cf = configparser.ConfigParser()
    cf.read("conf/config.ini")
    config = {
        "url_prefix": cf.get("core", "url_prefix"),
        "mariadb_host": cf.get("mariadb", "host"),
        "mariadb_port": cf.get("mariadb", "port"),
        "mariadb_user": cf.get("mariadb", "user"),
        "mariadb_pwd": cf.get("mariadb", "password"),
        "mariadb_db": cf.get("mariadb", "db"),
        "start_time": cf.get("param", "start_time"),
        "end_time": cf.get("param", "end_time"),
        "type": cf.get("param", "type"),
        "url_prefix": cf.get("core", "url_prefix")
    }
    return config
