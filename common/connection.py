from common.recordlog import logs
from conf.operationConfig import OperationConfig
import pymysql

conf = OperationConfig()

class ConnectMysql:
    '''
    连续读取mysql数据库的数据
    '''

    def __init__(self):

        mysql_conf = {
            'host': conf.get_mysql_conf('host'),
            'port': int(conf.get_mysql_conf('port')),
            'user': conf.get_mysql_conf('user'),
            'password': conf.get_mysql_conf('password'),
            'database': conf.get_mysql_conf('sqszyx')
        }

        self.conn = pymysql.connect(**mysql_conf,charset='utf8')
        print(self.conn)


if __name__ == '__main__':
    conn = ConnectMysql()