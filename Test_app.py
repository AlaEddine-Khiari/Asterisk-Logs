import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from app import connect_to_postgres, insert_cdr, process_cdr_file

class TestScript(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a temporary CSV file
        self.temp_csv_file = os.path.join(self.temp_dir.name, 'test.csv')
        with open(self.temp_csv_file, 'w') as file:
            file.write("""2024-03-15 10:00:00,200,39100200,ANSWERED,3,7,test1,SIP/100009
2024-03-15 10:05:00,100,200,ANSWERED,12,15,test2,SIP/100009
2024-03-15 10:06:00,100,300,BUSY,0,3,test3,
2024-03-15 10:07:00,100,300,ANSWERED,7,7,test3,
""")

    def tearDown(self):
        # Delete the temporary directory and its contents
        self.temp_dir.cleanup()

    @patch('app.psycopg2.connect')
    def test_connect_to_postgres(self, mock_connect):
        # Mock the connection object
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Call the function
        conn = connect_to_postgres()

        # Assertions
        self.assertIsNotNone(conn)
        mock_connect.assert_called_once()

    @patch('app.connect_to_postgres')
    def test_process_cdr_file(self, mock_connect):
        # Mock the cursor object
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [None]  # Simulate no existing records
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Call the function
        process_cdr_file(self.temp_csv_file)

if __name__ == '__main__':
    unittest.main()
