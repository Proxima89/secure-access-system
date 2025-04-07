import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os
import mysql.connector
from tests.mock_objects import MockGPIO, MockSMBus, MockSimpleMFRC522

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock gpiozero before importing check_access
with patch("gpiozero.Buzzer") as mock_buzzer:
    mock_buzzer.return_value = MagicMock()
    from check_access import execute_query, lcd_init, lcd_string, main
    from access_control_app import check_access

@pytest.fixture
def mock_hardware():
    """Fixture to mock all hardware components"""
    with patch("smbus.SMBus", return_value=MockSMBus(1)), \
         patch("RPi.GPIO.setmode") as mock_gpio_setmode, \
         patch("RPi.GPIO.setup") as mock_gpio_setup, \
         patch("RPi.GPIO.output") as mock_gpio_output, \
         patch("mfrc522.SimpleMFRC522", return_value=MockSimpleMFRC522()) as mock_reader:
        
        # Setup mock objects
        mock_bus = MockSMBus(1)
        
        yield {
            "bus": mock_bus,
            "reader": mock_reader.return_value,
            "gpio_setmode": mock_gpio_setmode,
            "gpio_setup": mock_gpio_setup,
            "gpio_output": mock_gpio_output
        }

def test_execute_query_success(mock_db_connection):
    """Test successful database query execution"""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [("test_user", "2024-03-07 10:00:00")]
    
    result = execute_query("SELECT * FROM users WHERE id = %s", (1,))
    assert result == [("test_user", "2024-03-07 10:00:00")]
    mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE id = %s", (1,))

def test_execute_query_error(mock_db_connection):
    """Test database query execution with error"""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.execute.side_effect = mysql.connector.Error("Database error")
    
    result = execute_query("SELECT * FROM users")
    assert result is None

def test_lcd_init(mock_hardware):
    """Test LCD initialization"""
    # Mock the bus variable
    with patch("check_access.bus", mock_hardware["bus"]):
        lcd_init()
        # Verify that the correct initialization commands were sent
        assert mock_hardware["bus"].write_byte.call_count >= 5  # At least 5 initialization commands

def test_lcd_string(mock_hardware):
    """Test sending string to LCD"""
    # Mock the bus variable
    with patch("check_access.bus", mock_hardware["bus"]):
        test_message = "Hello World"
        lcd_string(test_message)
        # Verify that write_byte was called for each character
        assert mock_hardware["bus"].write_byte.call_count >= len(test_message)

@pytest.mark.skip(reason="Hardware-dependent test that requires mocking")
def test_main_successful_sign_in(mock_hardware, mock_db_connection):
    """Test successful sign in flow"""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.side_effect = [
        [(1, "Test User")],  # First query for user lookup
        []  # Second query for existing attendance
    ]
    
    mock_reader = mock_hardware["reader"]
    mock_reader.read.return_value = (12345, "Test User")
    
    # Mock datetime to return a consistent timestamp
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 3, 7, 10, 0, 0)
        
        # Run main in a separate thread to avoid infinite loop
        with pytest.raises(SystemExit):
            main()
    
    # Verify database operations
    assert mock_cursor.execute.call_count >= 2  # At least user lookup and attendance insert
    
    # Verify hardware interactions
    mock_hardware["buzzer"].on.assert_called_once()
    mock_hardware["buzzer"].off.assert_called_once()
    assert mock_hardware["gpio_output"].call_count >= 2  # At least on and off for relay

def test_check_access(mock_subprocess, mock_tkinter, mock_db_connection):
    """Test check access functionality"""
    # Setup database mock
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [("Test User", None)]  # Mock a user who is signed in
    
    # Setup UI mocks
    mock_messagebox = mock_tkinter["messagebox"]
    
    # Mock the messagebox import
    with patch("access_control_app.messagebox", mock_messagebox):
        check_access()
        mock_subprocess.assert_called_once_with(["python3", "check_access.py"])
        assert mock_messagebox.showinfo.call_count == 1 