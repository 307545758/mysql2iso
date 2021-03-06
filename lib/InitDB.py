# -*- encoding: utf-8 -*-
'''
@author: Great God
'''

import pymysql,sys
import traceback
sys.path.append("..")
from .Loging import Logging
from contextlib import closing

class InitMyDB(object):
    def __init__(self,mysql_host=None,mysql_port=None,mysql_user=None,mysql_password=None,unix_socket=None,
                 auto_commit=None,ssl=None,type=None):
        self.ssl = ssl
        self.auto_commit = auto_commit
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_port = mysql_port
        self.socket_dir = unix_socket
        self.mysql_host = mysql_host

    def Init(self):

        try:
            connection = pymysql.connect(host=self.mysql_host,
                                              user=self.mysql_user,
                                              password=self.mysql_password, port=self.mysql_port,
                                              db='',
                                              charset='utf8mb4',
                                              autocommit=self.auto_commit,
                                              ssl=self.ssl,
                                              unix_socket=self.socket_dir,max_allowed_packet=536870912,
                                              cursorclass=pymysql.cursors.DictCursor)
            return connection
        except:
            Logging(msg='host: {}  port: {} '.format(self.mysql_host,self.mysql_port),level='error')
            Logging(msg=traceback.format_exc(),level='error')
            return None

    def ExecuteSQL(self,sql_list = None):
        connection = self.Init()
        with closing(connection.cursor()) as cur:
            try:
                for sql in sql_list[::-1]:
                    Logging(msg='Rollback statement: {}'.format(sql),level='info')
                    cur.execute(sql)
            except pymysql.Error:
                return False
                Logging(msg=traceback.format_exc(),level='error')
                connection.rollback()
            connection.commit()
        connection.close()
        return True
