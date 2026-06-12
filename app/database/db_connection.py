import mysql.connector
from contextlib import contextmanager


class GetConnection : 
    def __init__(self):
        self.conn = mysql.connector.connect(
            host= "127.0.0.1",
            user= "root",
            password="oldbook",
            port= "3307"
        )


    def create_database(self):

        self.cursor = self.conn.cursor()
        database = "library_db"
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")

        self.conn.commit()

        self.cursor.close()
        self.conn.close()

    def get_connection(self):
        return  mysql.connector.connect(
            host= "127.0.0.1",
            user= "root",
            password="oldbook",
            port= "3307",
            database="library_db"
        )
    
    def create_table(self):
        self.conn = self.get_connection()
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INT PRIMARY KEY AUTO_INCREMENT , 
                title VARCHAR(50) NOT NULL ,
                author VARCHAR(50) NOT NULL ,
                genre ENUM("Fiction", "Non-Fiction", "Science", "History", "Other"),
                is_available BOOLEAN DEFAULT TRUE ,
                borrowed_by_member_id INT NULL
            )

            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                id INT PRIMARY KEY AUTO_INCREMENT ,
                name VARCHAR(50) NOT NULL , 
                email VARCHAR(100) NOT NULL UNIQUE , 
                is_active BOOLEAN DEFAULT TRUE , 
                total_borrows INT DEFAULT 0 
            )
            """
        )

        self.cursor.close()
        self.conn.close()


    def close(self):
        self.cursor.close()
        self.conn.close()

    def setup(self):
        self.create_database()
        self.create_table()

    @contextmanager #import from contextlib import contextmanager, you don't want to use async
    def get_cursor(self, dictionary=True): #if you want to not receive ditc enter dictionary= False ; example with db.get_cursor(dictionary=False) as cursor :
        conn = self.get_connection() #connection
        cursor = conn.cursor(dictionary=dictionary, buffered=True) #buffered is not obligatory , just in case

        try : 
            yield cursor # as cursor start here ... cursor.execute(..)
            conn.commit() # if you just get and not modify is don't care , if you want to create if commit you can 
        except Exception: 
            conn.rollback() # RETURN BACK IF ERROR AND DON'T COMMIT 
            raise
        finally:
            cursor.close # close cursor ...
            conn.close() #same you understand 
    
