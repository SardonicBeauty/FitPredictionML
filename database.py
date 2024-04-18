import mysql.connector
from mysql.connector import Error
import random

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='test',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def fetch_random_entries(connection, table_name, num_entries):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY RAND() LIMIT {num_entries}")
        entries = cursor.fetchall()
        return entries
    except Error as e:
        print(f"Error fetching entries: {e}")
        return []

def create_table(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
        print(f"Table '{table_name}' created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_sample_data(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {table_name} (name) VALUES ('John'), ('Alice'), ('Bob'), ('Emily'), ('David')")
        connection.commit()
        print("Sample data inserted successfully")
    except Error as e:
        print(f"Error inserting sample data: {e}")

def main():
    connection = connect_to_database()
    if connection:
        table_name = 'your_table_name'  # Replace 'your_table_name' with the actual table name
        create_table(connection, table_name)
        insert_sample_data(connection, table_name)
        
        num_entries = 5
        random_entries = fetch_random_entries(connection, table_name, num_entries)
        if random_entries:
            print("Random Entries:")
            for entry in random_entries:
                print(entry)
        else:
            print("No entries found.")
        connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()