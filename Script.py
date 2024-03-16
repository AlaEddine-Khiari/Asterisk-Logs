import csv
import psycopg2
import os
from datetime import datetime

# Function to connect to PostgreSQL
def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        return None

# Function to insert CDR data into PostgreSQL
def insert_cdr(conn, cursor, cdr_data):
    try:
        cursor.execute("""
            INSERT INTO your_table_name (timestamp, source, destination, status, duration, call_recording)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, cdr_data)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print("Error inserting CDR data:", e)

# Function to read binary data from a file
def read_binary_data(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Function to read CSV file and insert data into PostgreSQL
def process_cdr_file(file_path):
    conn = connect_to_postgres()
    if conn is not None:
        cursor = conn.cursor()
        last_one = None  
        with open(file_path, 'r') as csvfile:
            cdr_reader = csv.reader(csvfile)
            for row in cdr_reader:
                # Assuming the structure of CSV file: timestamp, source, destination, status, duration, recording_file_name
                timestamp, source, destination, status, duration, recording_file_name = row
                # Construct the full file path
                recording_file_path = os.path.join('/app/asterisk/recordings', recording_file_name)
                # Read binary data from the file
                call_recording_data = read_binary_data(recording_file_path)
                cdr_data = (timestamp, source, destination, status, duration, call_recording_data)
                # Check if call_start date is after the last recorded call_start date
                last_call_start_date = get_last_call_start_date(conn, cursor)
                call_start_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                if (last_call_start_date is None or call_start_date > last_call_start_date) and (recording_file_name != last_one):
                    insert_cdr(conn, cursor, cdr_data)
                    last_one = recording_file_name
        conn.close()

# Function to get the last recorded call_start date from PostgreSQL
def get_last_call_start_date(conn, cursor):
    cursor.execute("SELECT MAX(timestamp) FROM cdr_log")
    last_call_start_date = cursor.fetchone()[0]
    return last_call_start_date

# Run the script
if __name__ == "__main__":
    file_path = "/app/Simple.csv"
    process_cdr_file(file_path)
