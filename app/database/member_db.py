import mysql.connector
from .db_connection import GetConnection




class MemberDatabase: 
    def __init__(self, db : GetConnection): 
        self.db = db

    
    def create_member(self, data : dict) -> int: 
        with self.db.get_cursor() as cursor : 

            values = (data["name"], data["email"])
            cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)",(values ))
            return cursor.lastrowid
    
    def get_all_members(self) -> list[dict]:
        with self.db.get_cursor() as cursor : 

            cursor.execute("SELECT * FROM members ")
            return cursor.fetchall()
    
    def get_member_by_id(self, member_id) -> dict | None :
        with self.db.get_cursor() as cursor : 

            cursor.execute("SELECT * FROM members WHERE id = %s", (member_id, ))
            return cursor.fetchone()

    def update_member_by_id(self , member_id , data : dict) -> bool :
        with self.db.get_cursor() as cursor :  

            add_data_ = [f"{key} = %s" for key in data.keys()]
            str_data_keys = ", ".join(add_data_)

            sql = f"UPDATE members SET {str_data_keys} WHERE id = %s "
            values = list(data.values()) + [member_id]

            cursor.execute(sql , values)
           
            return cursor.rowcount > 0 
    
    def deactivate_members(self, member_id : int) -> None   :
        with self.db.get_cursor() as cursor : 

            cursor.execute("UPDATE members SET is_active = False WHERE id = %s", (member_id,))
           

        
    
    def activate_member(self, member_id : int ) -> None  : 

        with self.db.get_cursor() as cursor : 

            cursor.execute("UPDATE members SET is_active = True WHERE id = %s", (member_id,))
        
    
    def increment_borrow(self, member_id : int ) -> bool :
        with self.db.get_cursor() as cursor : 

            cursor.execute("UPDATE members SET total_borrows = COALESCE(total_borrows , 0) + 1  WHERE  id = %s", (member_id, ))
            return cursor.rowcount > 0 
    
    def count_active_members(self) -> int :
        with self.db.get_cursor() as cursor : 

            cursor.execute("SELECT COUNT(is_active) FROM members WHERE is_active = True") 
            count = cursor.fetchone()
            return count["COUNT(is_active)"]
        
    def get_top_member(self) -> dict : 
        with self.db.get_cursor() as cursor : 

            cursor.execute("SELECT * FROM members " \
            "ORDER BY total_borrows DESC")
            return cursor.fetchone()
    