from flask import Flask
import csv
import psycopg2
import os
import time
from datetime import datetime, timedelta

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
            INSERT INTO cdr_log (timestamp, source, destination, status, duration, call_recording)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, cdr_data)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print("Error inserting CDR data:", e)

# Function to read CSV file and insert data into PostgreSQL
def process_cdr_file(file_path):
    conn = connect_to_postgres()
    if conn is not None:
        cursor = conn.cursor()
        last_one = None
        last_call_start_date = None
        with open(file_path, 'r') as csvfile:
            cdr_reader = csv.reader(csvfile)
            for row in cdr_reader:
                # Assuming the structure of CSV file: timestamp, source, destination, status, billsec, duration, recording_file_name
                timestamp, source, destination, status, billsec, duration, recording_file_name = row
                # Construct the full file path
                recording_file_path = os.path.join('/ext/recordings', recording_file_name+'wav')
                # Check if billsec is equal to duration
                if int(billsec) == int(duration):
                    status = "NO ANSWER"
                    call_recording_data = None
                    duration = "00:00"  # Set duration to 00:00 if billsec equals duration
                else:
                    # Convert duration to minutes and seconds format
                    duration = str(timedelta(seconds=int(duration)))
                    call_recording_data = read_binary_data(recording_file_path)
                # Check if call_start date is after the last recorded call_start date
                last_call_start_date = get_last_call_start_date(conn, cursor)
                call_start_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                if (last_call_start_date is None or call_start_date > last_call_start_date) and (recording_file_name != last_one):    
                    # Insert Data Into Data Base
                    cdr_data = (timestamp, source, destination, status, duration, call_recording_data)
                    insert_cdr(conn, cursor, cdr_data)
                    last_one = recording_file_name
                # Delete the call recording file
                os.remove(recording_file_path)
        conn.close()

# Function to get the last recorded call_start date from PostgreSQL
def get_last_call_start_date(conn, cursor):
    cursor.execute("SELECT MAX(timestamp) FROM cdr_log")
    last_call_start_date = cursor.fetchone()[0]
    return last_call_start_date

# Function to read binary data from a file
def read_binary_data(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Run the script in a loop
@app.route('/apply', methods=['GET'])
def apply_changes():
    file_path = "/ext/Simple.csv"
    try:
        process_cdr_file(file_path)
        return 'Successfully Updated'
    except Exception as e:
        return f'An error occurred while Updating: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)