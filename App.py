import sqlite3
import Record
import sys
import random
import string
import time

class App:
    def __init__(self, database:str):
        self.database = database
        self.connection = sqlite3.connect("data_base.db")
        self.cursor = self.connection.cursor()

    def __createTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS employees(name, bithsday, sex)")

    def __makeRecord(self):
        record = sys.argv[2::]
        rec = Record(record)
        rec.push(self.cursor)

    def __dropTable(self):
        self.cursor.execute("DROP TABLE employees")

    def __generateContent(self):
        letters = string.ascii_lowercase
        records = []
        N = 1000000
        for i in range(N):
            name = ""
            for j in range(3):
                length = random.randint(4,6)
                name += ''.join(random.choice(letters) for k in range(length)).capitalize() + " "
            if len(name) < 16: #for tabulation
                name += "   "
            number = random.randint(1930,2009)
            date = str(number)  +  "-" + str( number%12+1).zfill(2) + "-" + str(number%30+1).zfill(2)
            sex = ""
            if number % 2 == 0:
                sex = "Female"
            else:
                sex = "Male"
            
            records.append((name, date, sex))
            #print(records[i],i)
        return records
   
    def __showRecords(self):
        return self.cursor.execute("""
                       SELECT DISTINCT name, bithsday, sex ,
                       cast (date('now','start of year') as integer) - cast (date(bithsday,'start of year') as integer) + case when strftime('%m-%d',date('now')) < strftime('%m-%d',bithsday) then -1 else 0 end
                       FROM employees
                       ORDER BY name ASC
                       """).fetchall()

    def __showSelectedRecords(self):
        return self.cursor.execute("""
                       SELECT DISTINCT name, bithsday, sex,
                       cast (date('now','start of year') as integer) - cast (date(bithsday,'start of year') as integer) + case when strftime('%m-%d',date('now')) < strftime('%m-%d',bithsday) then -1 else 0 end
                       FROM employees where sex = 'Male' AND name LIKE 'F%'
                       ORDER BY name ASC
                       """).fetchall()

    def commandHandler(self, num_operation):
        if num_operation==1:
            self.__createTable()
            self.connection.commit()
        elif num_operation==2:
            self.__makeRecord()
            self.connection.commit()
        elif num_operation==3:
            print(self.__showRecords())
        elif num_operation==4:
            records = self.__generateContent()
            Record.pushListOfRecords(self.cursor, records)
            self.connection.commit()
        elif num_operation == 5:
            time_b = time.time()
            res = self.__showSelectedRecords()
            time_nd = time.time()
            print(f"Timing: {time_nd-time_b}")
            print("Name\t\tBirthsday\t\tSex\t\tAge")
            for line in res:
                print(f"{line[0]}\t{line[1]}\t{line[2]}\t{line[3]}")
            #print(*res, sep="\n")
        elif num_operation==0:
            self.__dropTable()
            self.connection.commit()