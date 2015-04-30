#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    Author: Danilo F. Chilene
    Email:      bicofino at gmail dot com
"""

version = 0.1
import argparse
import inspect
import pypyodbc
import json


class Checks(object):

    def Logused(self):
        '''Example: ./pyssql.py --username user --password password --address 1.1.1.1 --port 1433 --database Master Logused'''
        query = "select f.DBName, f.Data_Log, isnull(g.groupname,'LOG') as filegroup, round(sum(Size) * (8192.0/1048576),0)  File_Size, round(sum(SpaceUsed) * (8192.0/1048576),0) MB_Used,  round((sum(Size) * (8192.0/1048576)) - (sum(SpaceUsed) * (8192.0/1048576)),0) MB_Free,  round((((sum(Size) * (8192.0/1048576)) - (sum(SpaceUsed) * (8192.0/1048576)))/ (sum(Size) * (8192.0/1048576)))*100,0) as PCT_Free,  round(((sum(SpaceUsed) * (8192.0/1048576))/ (sum(Size) * (8192.0/1048576)))*100,0) as PCT_Used  from (select db_name() as DBName, groupid, fileproperty(name,'IsLogFile') as Data_Log,  convert(float,size) as Size, convert(float,fileproperty(name,'SpaceUsed')) as SpaceUsed  from sysfiles ) f left join sysfilegroups g on f.groupid = g.groupid  where g.groupname is null group by DBName, Data_Log, g.groupname"
        print self.cur.execute(query).fetchone()[7]

    def Primaryused(self):
        '''Example: ./pyssql.py --username user --password user --address 1.1.1.1 --port 1433 --database Master Primaryused'''
        query = "select f.DBName, f.Data_Log, isnull(g.groupname,'LOG') as filegroup, round(sum(Size) * (8192.0/1048576),0)  File_Size, round(sum(SpaceUsed) * (8192.0/1048576),0) MB_Used,  round((sum(Size) * (8192.0/1048576)) - (sum(SpaceUsed) * (8192.0/1048576)),0) MB_Free,  round((((sum(Size) * (8192.0/1048576)) - (sum(SpaceUsed) * (8192.0/1048576)))/ (sum(Size) * (8192.0/1048576)))*100,0) as PCT_Free,  round(((sum(SpaceUsed) * (8192.0/1048576))/ (sum(Size) * (8192.0/1048576)))*100,0) as PCT_Used  from (select db_name() as DBName, groupid, fileproperty(name,'IsLogFile') as Data_Log,  convert(float,size) as Size, convert(float,fileproperty(name,'SpaceUsed')) as SpaceUsed  from sysfiles ) f left join sysfilegroups g on f.groupid = g.groupid  where g.groupname is not null group by DBName, Data_Log, g.groupname"
        print self.cur.execute(query).fetchone()[7]

    def show_databases(self):
        '''./pyssql.py --username user --password password --address 1.1.1.1 --port 1433 --database master show_databases'''
        query = '''SELECT name FROM sys.databases'''
        res = self.cur.execute(query).fetchall()
        key = ['{#DATABASE}']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        print json.dumps({'data': lst})


class Main(Checks):

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--username')
        parser.add_argument('--password')
        parser.add_argument('--address')
        parser.add_argument('--port')
        parser.add_argument('--database')

        subparsers = parser.add_subparsers()

        for name in dir(self):
            if not name.startswith("_"):
                p = subparsers.add_parser(name)
                method = getattr(self, name)
                argnames = inspect.getargspec(method).args[1:]
                for argname in argnames:
                    p.add_argument(argname)
                p.set_defaults(func=method, argnames=argnames)
        self.args = parser.parse_args()

    def db_connect(self):
        a = self.args
        username = a.username
        password = a.password
        address = a.address
        database = a.database
        port = a.port
        self.db = pypyodbc.connect(
            '''Driver=FreeTDS;Server={0};port={1};uid={2};pwd={3};database={4}'''.format(address,
                                                                                         port, username, password, database))
        self.cur = self.db.cursor()

    def db_close(self):
        self.cur.close()
        self.db.close()

    def __call__(self):
        try:
            a = self.args
            callargs = [getattr(a, name) for name in a.argnames]
            self.db_connect()
            try:
                return self.args.func(*callargs)
            finally:
                self.db_close()
        except Exception, err:
            print err

if __name__ == "__main__":
    main = Main()
    main()
