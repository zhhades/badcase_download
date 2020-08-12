## desc
本文档旨在快速使用批量导出bad case
## config
```buildoutcfg
[mariadb]
#必填
host=10.199.1.210
#必填
port=3306
#必填
user=root
#必填
password=W.R3elungNq
#必填
db=megcity
[param]
#必填
start_time=2020-08-02 00:00:00
#必填
end_time=2020-08-12 23:59:59
type=opened_mucktruck,two
[core]
#必填
url_prefix=http://10.199.1.210:8080/v5/resources/data?uri={}&downloadFilename={}
```
