from base import Base
from sqlalchemy import create_engine
from pathlib import Path
from dotenv import load_dotenv
from os import getenv
import pandas as pd
import psycopg2
import os

folder_dir = os.path.join(Path(__file__).parents[0], 'data')

load_dotenv()
class PGSQL:
    __user = 'qxqdekzb'
    __password = 'PhAQn8YHzjFbSBOz9oRdohA5XXF1pYLB'
    __server = getenv("SERVER")
    __pg_con = psycopg2.connect(
        dbname=__user,
        user=__user,
        password=__password,
        host=__server
        )
    cur = __pg_con.cursor()
    #only used for the quick dump of the csvs's
    SQL_URL='postgresql://qxqdekzb:PhAQn8YHzjFbSBOz9oRdohA5XXF1pYLB@batyr.db.elephantsql.com/qxqdekzb'

    def toSQL(self,csvpath,table):
        print(self.SQL_URL)
        #########build_temp_table to upsert from
        try:
            self.df = pd.read_csv(csvpath)
            print(self.df.head())
            engine = create_engine(self.SQL_URL)
            self.df.to_sql(table, con=engine, if_exists='replace', index=False)
        except psycopg2.ProgrammingError as msg:
                print(f'Command Skipped: {msg}')



if __name__ == '__main__':
    p = PGSQL()
   
    p.toSQL(f'{folder_dir}\monsters.csv','monsters')
    p.cur.close()
    p.toSQL(f'{folder_dir}\monster_actions.csv','monster_actions')
    p.cur.close()
    p.toSQL(f'{folder_dir}\monster_resists.csv','monster_resists')
    p.cur.close()
    p.toSQL(f'{folder_dir}\monster_characteristics.csv','monster_characteristics')
    p.cur.close()
 
    '''
    def create_tables(self, sql_filepath: str):
        start = self.create_file(sql_filepath)
        tables = start.split(';')
        for table in tables:
            try:
                print(table)
                self.cur.execute(table)
                self.__pg_con.commit()
            except psycopg2.ProgrammingError as msg:
                print(f'Command Skipped: {msg}')
                '''