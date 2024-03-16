import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from Script import connect_to_postgres, insert_cdr, process_cdr_file, get_last_call_start_date

class TestScript(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a temporary CSV file
        self.temp_csv_file = os.path.join(self.temp_dir.name, 'test.csv')
        with open(self.temp_csv_file, 'w') as file:
            file.write("""2024-03-15 10:00:00,1234567890,0987654321,completed,60,test1
2024-03-15 10:05:00,0987654321,1234567890,completed,45,test2
""")

        # Create two mock recording files
        self.recording1_path = os.path.join(self.temp_dir.name, 'recording1.wav')
        self.recording2_path = os.path.join(self.temp_dir.name, 'recording2.wav')
        with open(self.recording1_path, 'wb') as file:
            file.write(b'Mock recording 1 data')
        with open(self.recording2_path, 'wb') as file:
            file.write(b'Mock recording 2 data')

    def tearDown(self):
        # Delete the temporary directory and its contents
        self.temp_dir.cleanup()

    @patch('Script.psycopg2.connect')
    def test_connect_to_postgres(self, mock_connect):
        # Mock the connection object
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Call the function
        conn = connect_to_postgres()

        # Assertions
        self.assertIsNotNone(conn)
        mock_connect.assert_called_once()

    @patch('Script.connect_to_postgres')
    def test_process_cdr_file(self, mock_connect):
        # Mock the cursor object
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [None]  # Simulate no existing records
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Call the function
        process_cdr_file(self.temp_csv_file)

        # Assertions or further test steps

    @patch('Script.connect_to_postgres')
    def test_get_last_call_start_date(self, mock_connect):
        # Mock the cursor object
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ['2024-01-01 00:00:00']  # Simulate an existing record
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Call the function
        last_call_start_date = get_last_call_start_date(mock_conn, mock_cursor)

if __name__ == '__main__':
    unittest.main()
