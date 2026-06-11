import mysql.connector
# from .db_connection import GetConnection


class Book_Database: 
    def __init__(self , db ): #GetConnection):
        self.db = db

        self.conn = self.db.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def create_book(self, title : str , author : str ,genre : str) -> int :

        sql = "INSERT INTO books (title, author, genre) VALUES (%s , %s, %s)"
        values = (title,author,genre)

        self.cursor.execute(sql, values)
        book_id = self.cursor.lastrowid
        self.conn.commit()

        return book_id
    
    def get_all_books(self) -> list[dict]:

        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()


    def get_book_by_id(self, book_id : int ) -> dict | None :

        self.cursor.execute("SELECT * FROM books WHERE id = %s", (book_id, ))
        return self.cursor.fetchone()
    
    def update_book(self, book_id, data : dict) -> bool : 

        add_data_module = [f"{key} = %s"for key in data.keys()]
        key_str = ", ".join(add_data_module)

        sql = f"UPDATE books SET {key_str} WHERE id = %s "
        values = list(data.values()) + [book_id]

        self.cursor.execute(sql, values)
        self.conn.commit()

        succes = self.cursor.rowcount > 0 

        return succes
    

    def count_total_books(self) -> int : 

        self.cursor.execute("SELECT COUNT(*) FROM books ")
        count = self.cursor.fetchone()
        return count["COUNT(*)"]
    
    def count_available_books(self) -> int : 

        self.cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = True ")
        count = self.cursor.fetchone()
        return count["COUNT(*)"]
    
    def count_borrowed_books(self) -> int:

        self.cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = False")
        count = self.cursor.fetchone()
        return count["COUNT(*)"]
    
    def count_by_genre(self, genre) -> dict : 

        self.cursor.execute("SELECT COUNT(genre) FROM books WHERE genre = %s", (genre, ))
        count= self.cursor.fetchone()
        return {f"Count of {genre}" : count["COUNT(genre)"]}
    
    def count_active_borrows_by_member(self, member_id) -> dict : 
        
        self.cursor.execute("SELECT COUNT(borrowed_by_member_id) FROM books " \
        " WHERE borrowed_by_member_id = %s ", (member_id, ))
        count =  self.cursor.fetchone()
        return {f"Member ID[{member_id}] as book" : count["COUNT(borrowed_by_member_id)"]}
 

    def set_available(self, book_id : int , val : bool , member_id : int ) -> bool : 

        sql = "INSERT book SET is_available = %s WHERE id = %s and borrowed_by_member_id = %s"
        values = (val, book_id, member_id)
        self.cursor.execute(sql, values)

        self.conn.commit()

        return self.cursor.rowcount > 0 