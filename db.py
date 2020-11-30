
import sqlite3


def db_conn():
    # Open existing or create new databse
    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    # Create table 'Users' in database
    cur.execute("""CREATE TABLE Users 
        (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
         username TEXT, 
         password TEXT,
         account_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
         )""")
    # Create table 'Pages' in database
    cur.execute("""CREATE TABLE Pages
        (page_id INTEGER PRIMARY KEY AUTOINCREMENT, 
         page TEXT NOT NULL,
         user_id INTEGER,
         page_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
         FOREIGN KEY (user_id) REFERENCES Users(user_id)
         )""")

    # Create table 'Distillations' in database
    cur.execute("""CREATE TABLE Distillations
        (distillation_id INTEGER PRIMARY KEY AUTOINCREMENT, 
         distillation TEXT NOT NULL,
         page_id INTEGER,
         distillation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
         FOREIGN KEY (page_id) REFERENCES Pages(page_id)
         )""")

    conn.commit()
    cur.close()
    conn.close()


def insert_user(username, password):

    # Open existing or create new databse

    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    # Insert variables into database
    try:
        sqlite_insert_with_param = """INSERT INTO Users (username, password) 
        VALUES (?,?);"""

        data_tuple = (username, password)
        cur.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        print("Python variables inserted successfully into Users table.")

        cur.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variables into Users table.")
    finally:
        if conn:
            conn.close()


def insert_word(word, explanation, user_id):
    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()
    try:

        sqlite_insert_with_param = """INSERT INTO word_explanation (word, explanation, user_id) 
        VALUES (?,?,?);"""

        data_tuple = (word, explanation, user_id)
        cur.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        print("Python variables inserted sucessfully into Users table.")

        cur.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variables into Pages table.")
    finally:
        if conn:
            conn.close()
            print("The connection is not closed")


# Function checks if the account is present

def check_user(password):
    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    try:
        user_id = cur.execute('SELECT user_id FROM Users WHERE password=?', password)
        try:
            output = user_id.fetchone()[0]
        except TypeError:
            output = 0
            print(output)
    except sqlite3.Error as error:
        print("Database Error.", error)

    finally:
        if conn:
            conn.close()
            print("Connection closed.")

    return output



