import datetime
class Record:
    def __init__(self, data):
        self.name = data[0]
        self.birthsday = data[1]
        self.sex = data[2]

    def __repr__(self) -> str:
        return f'Sex:{self.sex}'
    
    def toList(self):
        return [self.name, self.birthsday, self.sex]

    def push(self, cursor):
        cursor.execute("""
                       INSERT  INTO employees 
                        VALUES (?,?,?)
                       """,(self.name, self.birthsday, self.sex))      
        
    def getAge(self):
        dt_birth = datetime.datetime.strptime(self.birthsday,"%y-%m-%d")
        dt_today = datetime.datetime.today()
        year = dt_today.year- dt_birth.year
        condition  = ((dt_today.month < dt_birth.month) or (dt_today.month == dt_birth.month)and(dt_today.day < dt_birth.day))
        if(condition):
            year -= 1
        return(year)

    @staticmethod
    def pushListOfRecords(cursor, listOfRecords):
        response = """INSERT INTO employees VALUES"""     
        for record in listOfRecords:
            response += f""" (\"{record[0]}\", \"{record[1]}\", \"{record[2]}\"), """
        cursor.execute(response[:-2])
        