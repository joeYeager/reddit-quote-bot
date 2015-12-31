import MySQLdb, sys

class Queue:
    def __init__(self, logger):
        self.logger = logger

    def connect(self, h, u, password, database, table):
        try:
            self.db = MySQLdb.connect(host=h,user=u,passwd=password,db=database)
            self.cur = self.db.cursor()
            self.table = table;
        except:
            self.logger.fail("Failed to connect to database, exiting");
            sys.exit(1)

    def query(self,query):
        self.cur.execute(query)
        self.db.commit()

    def add(self, idNum, url):
        query = "INSERT INTO queue SET ID=\'"+ str(idNum) + "\', URL=\'" + str(url) + "\';"
        self.query(query)

    def remove(self, idNum):
        query = "DELETE FROM queue WHERE ID=\'"+ str(idNum)+ "\';"
        self.query(query)

    def get(self):
        query = "SELECT * FROM " + self.table + ";" 
        self.cur.execute(query)
        return self.cur.fetchall()

    def close(self):
        self.db.commit()
        self.db.close()
