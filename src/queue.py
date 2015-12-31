import MySQLdb, sys

class Queue:
    def __init__(self, h, u, password, database, table):
        # Set up the database connection
        #             self.db = MySQLdb.connect(host="localhost",
                         # user="forefathersbot",
                         # passwd="password",
                         # db="forefathersbot")
        try:
            self.db = MySQLdb.connect(host=h,user=u,passwd=password,db=database)
            self.cur = self.db.cursor()
            self.table = table;
        except:
            print "Failed to connect to database, exiting"
            sys.exit(1)
    
    def query(self,query):
        self.cur.execute(query)
        self.db.commit()

    def add(self, idNum, url, commentType):
        query = "INSERT INTO queue SET ID=\'"+ str(db.escape_string(idNum)) + "\', URL=\'" 
        query += url + "\', type=\'" + commentType + "\';"
        self.query(query)

    def remove(self, idNum):
        query = "DELETE FROM queue WHERE ID=\'"+ str(db.escape_string(idNum))+ "\';"
        self.query(query)

    def get(self):
        query="SELECT * FROM " + self.table + ";" 
        self.cur.execute(query)
        return self.cur.fetchall()

    def close(self):
        db.commit()
        
