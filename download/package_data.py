import mariadb
from elasticsearch import Elasticsearch


def get_all_record_by_params(host, port, user, password, database, params):
    bad_case_array = []
    conn = mariadb.connect(host=host, port=port, user=user, password=password, database=database)
    cursor = conn.cursor()
    sql = "select case_number,device_id,device_name,video_id,type,accept_type,roi,cause_area," \
          "cause_image_uri,cause_video_uri,address,location,description,artificial," \
          "state,zip_uri,update_time,create_time from tb_bad_case {}".format(params)
    cursor.execute(sql)
    for item in cursor.fetchall():
        bad_case = {
            "case_number": item[0],
            "device_id": item[1],
            "device_name": item[2],
            "video_id": item[3],
            "type": item[4],
            "accept_type": item[5],
            "roi": item[6],
            "cause_area": item[7],
            "cause_image": item[8],
            "cause_video": item[9],
            "address": item[10],
            "location": item[11],
            "description": item[12],
            "artificial": item[13],
            "state": item[14],
            "zip_uri": item[15],
            "update_time": item[16],
            "create_time": item[17]

        }
        bad_case_array.append(bad_case)
    return bad_case_array


def get_alarm_list_by_dsl(host_array, user, password, index_name, dsl):
    alarm_result = []
    es = Elasticsearch(
        host_array,
        # turn on SSL
        use_ssl=True,
        # no verify SSL certificates
        verify_certs=False,
        # don't show warnings about ssl certs verification
        ssl_show_warn=False,
        http_auth=(user, password)
    )
    res = es.search(
        index=index_name,
        body=dsl
    )
    all_doc = res['hits']['hits']
    for doc in all_doc:
        alarm_result.append(doc['_source'])
    return alarm_result
