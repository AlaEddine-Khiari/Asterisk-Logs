import unittest
from unittest.mock import patch, MagicMock
from Script import connect_to_postgres, insert_cdr, process_cdr_file, get_last_call_start_date

class TestScript(unittest.TestCase):
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

        # Mock other dependencies as needed

        # Call the function
        process_cdr_file('/path/to/test.csv')

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

        # Assertions or further test steps

if __name__ == '__main__':
    unittest.main()
