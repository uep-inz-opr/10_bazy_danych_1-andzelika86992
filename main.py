import csv
import sqlite3

class Report_Generator:
    def __init__(self, connection, escape_string= "(%s)"):
        self.connection= connection
        self.escape_string= escape_string
        self.report_text= None

    def generate_report(self):
        cursor= self.connection.cursor()
        sql= f"Select sum(duration) from polaczenia"
        cursor.execute(sql)
        result= cursor.fetchone()[0]
        self.report_text= result
        

    def get_report(self):
        return self.report_text

if __name__ == "__main__":
    main= input()
    sqlite_con= sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur= sqlite_con.cursor()
    cur.execute('''CREATE TABLE polaczenia (from_subscriber data_type INTEGER, 
                    to_subscriber data_type INTEGER, 
                    datetime data_type timestamp, 
                    duration data_type INTEGER , 
                    celltower data_type INTEGER);''') 


    with open(main, 'r') as fin:
        reader= csv.reader(fin, delimiter= ";")
        next(reader, None)
        rows= [x for x in reader]
        cur.executemany("INSERT INTO polaczenia (from_subscriber, to_subscriber, datetime, duration, celltower) VALUES (?, ?, ?, ?, ?);", rows)
        sqlite_con.commit()

        rg= Report_Generator(sqlite_con, escape_string= "?")
        rg.generate_report()
        print(rg.get_report())