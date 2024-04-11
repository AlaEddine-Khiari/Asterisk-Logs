from flask import Flask
import csv
import psycopg2
import os
import time
from datetime import timedelta

app = Flask(__name__)

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
        raise e
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
        raise e

# Function to read CSV file and insert data into PostgreSQL
def process_cdr_file(file_path):
    conn = connect_to_postgres()
    if conn is not None:
        cursor = conn.cursor()
        last_one = None
        with open(file_path, 'r+') as csvfile:
            cdr_reader = csv.reader(csvfile)
            for row in cdr_reader:
                if not row:  # Check if the row is empty or 
                    continue  # Skip
                # Assuming the structure of CSV file: timestamp, source, destination, status, billsec, duration, recording_file_name, aux: for Knowing The person Who answer For Incoming
                timestamp, source, destination, status, billsec, duration, recording_file_name, aux = row
                # Construct the full file path
                recording_file_path = os.path.join('/ext/recordings', recording_file_name+'.wav')
                # Convert billsec to minutes and seconds format
                x = billsec
                billsec = str(timedelta(seconds=int(billsec)))
                
                # Check if billsec is equal to 0 so the destination is unvailable
                if (int(x) == 0 and status == "ANSWERED" and recording_file_name != last_one):
                    status = "UNVAILABLE"
                    call_recording_data = None
                    cdr_data = (timestamp, source, destination, status, billsec, call_recording_data)
                    insert_cdr(conn, cursor, cdr_data)
                    last_one = recording_file_name
                
                elif len(source.split('<')[1].split('>')[0]) > 3 :
                    last_one = recording_file_name
                    if (not aux):
                        os.remove(recording_file_path)
                    elif (status == "ANSWERED"):
                        call_recording_data = read_binary_data(recording_file_path) 
                        destination = aux.split("/")[1][:3]                         
                        cdr_data = (timestamp, source, destination, status, billsec, call_recording_data)
                        insert_cdr(conn, cursor, cdr_data)
                        os.remove(recording_file_path)
                                    
                    elif (os.path.exists(recording_file_path)) and (status != "ANSWERED"):
                        call_recording_data = None
                        status = "NO ANSWER"
                        destination = "No One"
                        cdr_data = (timestamp, source, destination, status, billsec, call_recording_data)
                        insert_cdr(conn, cursor, cdr_data)
                        os.remove(recording_file_path)
                        
                elif (recording_file_name != last_one):                   
                    if status == "BUSY" or status == "NO ANSWER":
                        call_recording_data = None
                        os.remove(recording_file_path)
                    elif x == duration and status == "ANSWERED":
                        call_recording_data = None
                        status = "BUSY"
                    else:
                        call_recording_data = read_binary_data(recording_file_path)
                        os.remove(recording_file_path)
                    # Insert Data Into Data Base
                    cdr_data = (timestamp, source, destination, status, billsec, call_recording_data)
                    insert_cdr(conn, cursor, cdr_data)
                    last_one = recording_file_name
                else:
                        continue
            # Clear the CSV file by rewriting it without processed rows
            csvfile.seek(0)
            csvfile.truncate()
            csvfile.close()
        
        conn.close()

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
