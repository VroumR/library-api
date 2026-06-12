import mysql.connector
# from .db_connection import GetConnection


class Book_Database: 
    def __init__(self , db ): #GetConnection):
        self.db = db

        

    def create_book(self, title : str , author : str ,genre : str) -> int :

        with self.db.get_cursor() as cursor : 

            sql = "INSERT INTO books (title, author, genre) VALUES (%s , %s, %s)"
            values = (title,author,genre)

            cursor.execute(sql, values)
            book_id = cursor.lastrowid

            return book_id
    
    def get_all_books(self) -> list[dict]:

        with self.db.get_cursor() as cursor : 
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()


    def get_book_by_id(self, book_id : int ) -> dict | None :
        with self.db.get_cursor() as cursor : 

            cursor.execute("SELECT * FROM books WHERE id = %s", (book_id, ))
            return cursor.fetchone()
    
    def update_book(self, book_id, data : dict) -> bool : 

        with self.db.get_cursor() as cursor : 

            add_data_module = [f"{key} = %s"for key in data.keys()]
            key_str = ", ".join(add_data_module)

            sql = f"UPDATE books SET {key_str} WHERE id = %s "
            values = list(data.values()) + [book_id]

            cursor.execute(sql, values)
            
            succes = cursor.rowcount > 0 

            return succes
    

    def count_total_books(self) -> int : 
        with self.db.get_cursor() as cursor : 

            cursor.execute("SELECT COUNT(*) FROM books ")
            count = cursor.fetchone()
            return count["COUNT(*)"]
    
    def count_available_books(self) -> int : 
        with self.db.get_cursor() as cursor : 

            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = True ")
            count = cursor.fetchone()
            return count["COUNT(*)"]
        
    def count_borrowed_books(self) -> int:
        with self.db.get_cursor() as cursor : 
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = False")
            count = cursor.fetchone()
            return count["COUNT(*)"]
    
    def count_by_genre(self, genre) -> dict : 
        with self.db.get_cursor() as cursor : 
            cursor.execute("SELECT COUNT(genre) FROM books WHERE genre = %s", (genre, ))
            count= cursor.fetchone()
            return {f"Count of {genre}" : count["COUNT(genre)"]}
    
    def count_active_borrows_by_member(self, member_id) -> dict : 
        with self.db.get_cursor() as cursor : 
        
            cursor.execute("SELECT COUNT(borrowed_by_member_id) FROM books " \
            " WHERE borrowed_by_member_id = %s ", (member_id, ))
            count =  cursor.fetchone()
            return {f"Member ID[{member_id}] as book" : count["COUNT(borrowed_by_member_id)"]}
 

    def set_available(self, book_id : int , val : bool , member_id : int ) -> bool : 
        with self.db.get_cursor() as cursor : 

            sql = "UPDATE book SET is_available = %s WHERE id = %s and borrowed_by_member_id = %s"
            values = (val, book_id, member_id)
            cursor.execute(sql, values)

            return cursor.rowcount > 0 