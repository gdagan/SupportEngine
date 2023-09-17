import unittest
import flask
import os
import pytest
import tempfile
import pytest
from app import *

# get tickets 
def test_get_tickets():
    tickets = get_tickets()
    assert len(tickets) == 37
    
    # Assuming the first ticket is a dictionary, you can access its keys and values
    first_ticket = tickets[0]
    
    assert first_ticket['id'] == 1
    assert first_ticket['createddate'] == '2023-09-015'  # Assuming this is a string
    assert first_ticket['description'] == 'my laptop not working anymore'  # Assuming this is a string
    assert first_ticket['priority'] == 'high'  # Assuming this is a string
    assert first_ticket['category'] == 'software'  # Assuming this is a string

     
# create ticket
def test_create_ticket():
    ticket = create_ticket('2023-09-015', 'my laptop not working anymore', 'high', 'software', 'test_user')
    assert ticket['id'] == 1
    assert ticket['createddate'] == '2023-09-016'
    assert ticket['description'] == 'my laptop not working anymore'
    assert ticket['priority'] == 'high'
    assert ticket['category'] == 'software'
    assert ticket['requestername'] == 'test_user'

        


    

if __name__ == '__main__':
    unittest.main()

   