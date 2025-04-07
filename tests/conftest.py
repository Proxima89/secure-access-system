import pytest
import mysql.connector
from unittest.mock import MagicMock, patch
import sys
from mock_objects import MockGPIO, MockSMBus, MockSimpleMFRC522

# Below imports are used to replace real hardware-dependent modules with mock versions before the actual code tries to import them.
sys.modules["RPi"] = MagicMock()
sys.modules["RPi.GPIO"] = MockGPIO()
sys.modules["mfrc522"] = MagicMock()
sys.modules["mfrc522.SimpleMFRC522"] = MockSimpleMFRC522
sys.modules["smbus"] = MagicMock()
sys.modules["smbus.SMBus"] = MockSMBus

@pytest.fixture
#Mocks the MySQL database connection
def mock_db_connection():
    """Fixture to mock database connection"""
    with patch("mysql.connector.connect") as mock_connect:
        mock_connection = MagicMock()
        #Mocks the cursor object in order to simulate the execution of a queries
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        #Returns the mocked connection object so test can use it
        yield mock_connection

#Mocks the subprocess calls
@pytest.fixture
def mock_subprocess():
    """Fixture to mock subprocess calls"""
    with patch("subprocess.run") as mock_run:
        #Returns the mocked subprocess object so test can use it
        yield mock_run

#Mocks the tkinter components
@pytest.fixture
def mock_tkinter():
    """Fixture to mock tkinter components"""
    with patch("tkinter.Tk") as mock_tk, \
         patch("tkinter.Toplevel") as mock_toplevel, \
         patch("tkinter.messagebox") as mock_messagebox:
        #Returns the mocked tkinter components so test can use them
        yield {
            "tk": mock_tk,
            "toplevel": mock_toplevel,
            "messagebox": mock_messagebox
        } 