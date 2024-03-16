import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
import os

# Import functions from your script
from script import (
    connect_to_postgres,
    insert_cdr,
    read_binary_data,
    process_cdr_file,
    get_last_call_start_date,
)


class TestScript(unittest.TestCase):
    def setUp(self):
        # Mocking environment variables
        os.environ['DB_NAME'] = 'test_db'
        os.environ['DB_USER'] = 'test_user'
        os.environ['DB_PASSWORD'] = 'test_password'
        os.environ['DB_HOST'] = 'test_host'
        os.environ['DB_PORT'] = 'test_port'

    def tearDown(self):
        # Clear environment variables after test
        del os.environ['DB_NAME']
        del os.environ['DB_USER']
        del os.environ['DB_PASSWORD']
        del os.environ['DB_HOST']
        del os.environ['DB_PORT']

    def test_connect_to_postgres(self):
        # Test connection to PostgreSQL
        conn = connect_to_postgres()
        self.assertIsNotNone(conn)

    def test_insert_cdr(self):
        # Test inserting CDR data
        conn = MagicMock()
        cursor = MagicMock()
        cdr_data = ('2024-03-14 10:00:00', '123456789', '987654321', 'ANSWERED', 60, b'')
        insert_cdr(conn, cursor, cdr_data)
        cursor.execute.assert_called_once()

    def test_read_binary_data(self):
        # Test reading binary data from a file
        test_file_path = 'test_file.txt'
        with open(test_file_path, 'wb') as f:
            f.write(b'Test binary data')
        binary_data = read_binary_data(test_file_path)
        self.assertEqual(binary_data, b'Test binary data')
        os.remove(test_file_path)

    def test_get_last_call_start_date(self):
        # Test getting the last call start date
        cursor = MagicMock()
        cursor.fetchone.return_value = (datetime.now() - timedelta(days=1),)
        last_call_start_date = get_last_call_start_date(None, cursor)
        self.assertIsInstance(last_call_start_date, datetime)

    def test_process_cdr_file(self):
        # Test processing CDR file
        file_path = 'test.csv'
        with open(file_path, 'w') as f:
            f.write("2024-03-14 10:00:00,123456789,987654321,ANSWERED,60,test_recording.wav")
        # Mock other functions
        connect_to_postgres = MagicMock(return_value=None)
        read_binary_data = MagicMock(return_value=b'')
        insert_cdr = MagicMock()
        get_last_call_start_date = MagicMock(return_value=None)
        process_cdr_file(file_path)
        insert_cdr.assert_called_once()

if __name__ == '__main__':
    unittest.main()
