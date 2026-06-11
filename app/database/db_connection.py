import mysql.connector

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


    def setup(self):
        self.create_database()
        self.create_table()


    
