import unittest
from app_old import app, get_tickets # Import your Flask app instance
import sqlite3

class TicketingSystemIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and create a test database."""
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Create a test database or set up a connection to your test database
        # For example, you might use an in-memory SQLite database for testing
        self.db = get_tickets.connect_to_test_database()
        get_tickets.create_tables(self.db)  # Create necessary tables

    def tearDown(self):
        """Clean up after each test."""
        self.db.close()  # Close the database connection

    def test_create_and_retrieve_ticket(self):
        """Test creating a ticket and then retrieving it."""
        # Create a ticket
        data = {
            'createddate': '2020-01-01',
            'description': 'This is a test ticket.',
            'priority': 'high',
            'category': 'software',
            'requestername': 'test_user'
        }
        self.app.post('/create_ticket', data=data, follow_redirects=True)

        # Retrieve the created ticket
        response = self.app.get('/get_tickets')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'List of Tickets', response.data)
        self.assertIn(b'Test Ticket', response.data)  # Check if the ticket title is in the response

    def test_create_and_close_ticket(self):
        """Test creating a ticket and then closing it."""
        # Create a ticket
        data = {
            'createddate': '2020-01-01',
            'description': 'This is a test ticket to close.',
            'priority': 'medium',
            'category': 'software',
            'requestername': 'test_user'
        }
        self.app.post('/submit_ticket', data=data, follow_redirects=True)

        # Close the ticket
        response = self.app.post('/close_ticket/1', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ticket closed successfully', response.data)

if __name__ == '__main__':
    unittest.main()
