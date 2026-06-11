PROJECT LIBRARY

A/ The project is designed as a library management system and aims to be functional, organized, and scalable.

It is divided into two main parts:

1. The book management side, which includes its own classes, methods, and logic.
2. The member management side, which also includes its own classes, methods, and logic.

The project uses SQL for the database layer, Object-Oriented Programming in Python to manage the internal logic, and FastAPI to expose the system through a server/API.

The main idea is to provide a dynamic and secure service, with proper validations, conditions, and handling of edge cases.

------------------------------------------------------------------------------------------------------------------------------------------------

הפרויקט מוגדר כמערכת לניהול ספרייה, והמטרה שלו היא להיות מערכת פונקציונלית, מסודרת וניתנת להרחבה.

המערכת מחולקת לשני חלקים עיקריים:

צד ניהול הספרים, הכולל מחלקות, פונקציות ולוגיקה משלו.
צד ניהול החברים, הכולל גם הוא מחלקות, פונקציות ולוגיקה משלו.

הפרויקט משתמש ב-SQL עבור שכבת מסד הנתונים, בתכנות מונחה עצמים בפייתון לצורך ניהול הלוגיקה הפנימית, וב-FastAPI עבור צד השרת וה-API.

הרעיון המרכזי הוא לספק שירות דינמי ומאובטח, הכולל ולידציות, תנאים, ובדיקות למצבי קצה.



B/ RUN SQL  :

The code work with docker , he create an image with docker and run it : dont't worry isno complicate 

Run the following command to run a MySQL container. 

in terminal : pip install mysql-connector-python

docker pull mysql:latest

docker run --name library-mysql -e MYSQL_ROOT_PASSWORD=oldbook -p 3307:3306 -d mysql:latest

docker exec -it library-mysql mysql -u root -p

ENTER THE PASSWORD : oldbook

use command for show : SHOW DATABASES ;   
... welcome 


C/  FILES ARCHITECTURE : 
library-api/
│
│
├── main.py
├── database/
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
├── logs/
│   └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore

D/ TABLE EXAMPLE : 
BOOKS : 1
"""
CREATE TABLE IF NOT EXISTS books (
    id INT PRIMARY KEY AUTO_INCREMENT , 
    title VARCHAR(50) NOT NULL ,
    author VARCHAR(50) NOT NULL ,
    genre ENUM("Fiction", "Non-Fiction", "Science",  "History",   "Other"),
    is_available DEFAULT TRUE ,
    borrowed_by_member_id DEFAULT NULL
)

"""

MEMBERS : 2 

"""
CREATE TABLE IF NOT EXISTS members (
    id INT PRIMARY KEY AUTO_INCREMENT ,
    name VARCHAR(50) NOT NULL , 
    email UNIQ NOT NULL, 
    is_active DEFAULT TRUE , 
    total_borrows INT DEFAULT 0 
)
"""

4 : RULES OF THE PROCESS : 

חוק
נושא
הכלל
1
יצירת ספר
המשתמש שולח title/author/genre — המערכת מוסיפה is_available=True, borrowed_by=NULL
2
genre
חייב להיות Fiction / Non-Fiction / Science / History / Other — כל ערך אחר מחזיר שגיאה
יש לוודא הן בהוספה (POST) והן בעדכון (PATCH)
3
יצירת חבר
המשתמש שולח name/email — המערכת מוסיפה is_active=True, total_borrows=0
4
email
חייב להיות ייחודי — אם קיים כבר מחזיר שגיאה
5
חבר לא פעיל
אם is_active=False — אי אפשר להשאיל ספר
6
ספר לא זמין
אי אפשר להשאיל ספר שכבר מושאל (is_available=False)
7
מקסימום ספרים
חבר לא יכול להחזיק יותר מ-3 ספרים בו-זמנית
8
החזרת ספר
ניתן להחזיר ספר רק אם הוא מושאל לאותו חבר שמחזיר אותו

6/ ENDPOINTS : 

Method Endpoint / תיאור
POST
/books
יצירת ספר
GET
/books
כל הספרים
GET
/books/{id}
ספר לפי ID
PATCH
/books/{id}
עדכון ספר
PATCH
/books/{id}/borrow/{member_id}
השאלת ספר לחבר
PATCH
/books/{id}/return/{member_id}
החזרת ספר מחבר

Members Method Endpoint
תיאור
POST
/members
יצירת חבר
GET
/members
כל החברים
GET
/members/{id}
חבר לפי ID
PATCH
/members/{id}
עדכון חבר
PATCH
/members/{id}/deactivate
השבתת חבר
PATCH
/members/{id}/activate
הפעלת חבר

Reports Method Endpoint
תיאור
GET
/reports/summary
דוח כללי
GET
/reports/books-by-genre
ספרים לפי ז'אנר
GET
/reports/top-member
החבר הכי פעיל

7/ ORVERFLOW :

CLIENT -> BOOK_ROUTES/MEMBER_ROUTES/REPORT_ROUTES->DB-CONNECTION -> BOOKS_DB/MEMBER_DB -> DATABASE 

example of running : CLIENT (WANT TO EMPRUNT BOOK) / --PUT/ ROUTES (FOR EMPRUNT )  -> BOOK_ROUTES --VERIFY IF IS AVAILAIBLE AND MORE (AVAIBILITY, CONTENT AND MORE ) -> CONNECTION WITH THE DATABASE -> UPDATE HIM -> RETURN THE RESPONSE (IF ALL RIGHT YES AND INFO  IF NO ERROR AND INFO  OR ELSE )

8/INSTRUCTION FOR THE APPLICATION : 

install docker 
install mysql and create images from docker (read PARTIE 2 FOR MORE )
install fastapi in your terminal  "pip install 'fastapi[standard]' "
connect the server with "uvicorn main:app --reload -port 8000"
you can now connect with the localhost:8000 
use localhost:8000/docs for run it and use swagger 