import sqlite3
from datetime import datetime

class dbmanager():
    def __init__(self,db_name="track.db"):
        self.db_name=db_name
        self.initialize_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def initialize_table(self):
        query_products="""
        CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        target_price REAL NOT NULL) """

        query_hist="""
        CREATE TABLE IF NOT EXISTS price_hist(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        price REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
        )"""

        with self._get_connection() as conn:
            cursor=conn.cursor()
            cursor.execute(query_products)
            cursor.execute(query_hist)
            conn.commit()
        print("Database initialized")

    def add_products(self, name, url, target_price):
       
        query = 'INSERT INTO products(name, url, target_price) VALUES (?, ?, ?)'

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (name, url, target_price))
                conn.commit()
                print(f"successfully added {name}") 
        except sqlite3.IntegrityError:
            print(f"Error: The product '{name}' or URL is already being tracked.")
        except Exception as e:
            print(f"error occured: {e}")

    def log_price(self, product_id, price):
        query = "INSERT INTO price_hist (product_id, price) VALUES (?, ?)"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (product_id, price))
            conn.commit()
            print(f"Logged price {price} for product ID {product_id}")        


    def get_price_report(self):
        query = """
        SELECT products.name, price_hist.price, price_hist.timestamp
        FROM products
        JOIN price_hist ON products.id = price_hist.product_id
        ORDER BY price_hist.timestamp DESC
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()    
          
    def get_all_products(self):
        query = "SELECT * FROM products"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()    


if __name__ == "__main__":
    db = dbmanager()
    
    
    db.add_products(
        "Attic Book", 
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", 
        60.00
    )