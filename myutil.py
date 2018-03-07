import subprocess
import sqlite3
import pandas as pd

def myrun(cmd):
    """
    run command using subprocess module
    """
    try:
        subprocess.run(cmd.split(), check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        return False
    return True

class DbController:
    def __init__(self, dbFilepath):

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        self.dbFilepath = dbFilepath
        self.con = sqlite3.connect(self.dbFilepath)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()
        self.table_lst=self.__tables()

    def __del__(self):
        self.con.close()

    def execute(self, query, arg=None):
        try:
            if arg is None:
                self.cur.execute(query)
            else:
                self.cur.execute(query, arg)
            self.con.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
            print(e)
            return False
        return True
    
    def __tables(self):
        """
        get list of table names, like .tables
        """
        
        query = "SELECT name FROM sqlite_master where type='table'"
        success = self.execute(query)
        if success:
            table_lst=[dct["name"] for dct in self.cur.fetchall()]
            return table_lst
        else:
            return None
        
    def __columns(self, table):
        """
        get list of column names for the table
        """
        
        assert table in self.table_lst
        query = "PRAGMA table_info({})".format(table)
        success = self.execute(query)
        if success:
            column_lst=[dct["name"] for dct in mdc.cur.fetchall()]
            return column_lst
        else:
            return None

    def clear_row(self, table):
        """
        clear all rows
        """
        
        query = 'DELETE FROM "{}"'.format(table)
        success = self.execute(query)
        return success
    
    def count_row(self, table):
        """
        given table name, return number of rows
        """
        
        assert table in self.table_lst
        query = 'SELECT COUNT(*) AS count FROM "{}"'.format(table)
        success = self.execute(query)
        if success:
            return self.cur.fetchone()["count"]
        else:
            return None

