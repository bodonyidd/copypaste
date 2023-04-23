import sqlite3


class DatabaseHandler:

    def __init__(self,path=r"database\data.db") -> None:
        """
        Creates connection with the DB.
        :param path:
        :return: sqlite connection with the DB
        """
        self.connection = None
        try:
            self.connection = sqlite3.connect(path)
            self.initialize_db()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def initialize_db(self):
        try:
            self.connection.execute('CREATE TABLE IF NOT EXISTS COPYDATA (ID INTEGER PRIMARY KEY AUTOINCREMENT,TYPE INTEGER, TEXTDATA TEXT, FILE TEXT)')
            self.connection.commit()
        except sqlite3.OperationalError as o:
            print(f"Create table error. {o}")

    def insert_data(self, textdata,file=None,data_type=0):
        try:
            self.connection.execute(
                rf" INSERT INTO COPYDATA (TYPE,TEXTDATA,FILE) VALUES ('{data_type}','{textdata}', '{file}');")
            self.connection.commit()
            # print("Records created successfully")
        except sqlite3.IntegrityError as e:
            pass
            # print(f"Values are already existing: {e}")

    def list_elements(self, query_elements="*", where=""):
        cursor = self.connection.execute(f"SELECT {query_elements} FROM COPYDATA {where}")
        return cursor.fetchall()

    def delete_item(self, item_id):
        sql = f"DELETE FROM COPYDATA WHERE ID=?"
        cur = self.connection.cursor()
        cur.execute(sql, (item_id,))
        self.connection.commit()
        return True

    @staticmethod
    def close_connection(connection):
        """
        Closes connection with the DB.
        :param connection:
        :return: sqlite connection with the DB
        """
        connection.close()

   


# if __name__ == "__main__":
#     sqlite_handler = DbHandler()
#     conn = sqlite_handler.connect_to_db(path="../database/warehouse_flask.db")
#     sqlite_handler.initialize_db(conn)
#     sqlite_handler.insert_data(connection=conn, lastname="MOCK_DATA_LAST_NAME", firstname="MOCK_DATA_FIRST_NAME",
#                                email="MOCK_DATA_EMAIL")
#     data = sqlite_handler.list_elements(conn)
#     print(data)
