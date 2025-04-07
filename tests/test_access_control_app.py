import pytest
import sys
import os
from unittest.mock import patch

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from access_control_app import execute_query, get_latest_user, check_access, logout_user

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
    mock_cursor.execute.side_effect = Exception("Database error")
    
    result = execute_query("SELECT * FROM test")
    assert result is None

def test_get_latest_user_with_data(mock_db_connection):
    """Test getting latest user when data exists"""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [("John Doe", None)]
    
    name, clock_out = get_latest_user()
    assert name == "John Doe"
    assert clock_out is None

def test_get_latest_user_no_data(mock_db_connection):
    """Test getting latest user when no data exists"""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = []
    
    name, clock_out = get_latest_user()
    assert name == "User"
    assert clock_out is None

def test_check_access(mock_subprocess, mock_tkinter, mock_db_connection):
    """Test check access functionality"""
    # Setup database mock
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [("Test User", None)]  # Mock a user who is signed in
    
    # Setup UI mocks
    mock_messagebox = mock_tkinter["messagebox"]
    
    # Mock the messagebox import
    with patch("access_control_app.messagebox", mock_messagebox), \
         patch("access_control_app.get_latest_user", return_value=("Test User", None)):
        # Run the function
        check_access()
        
        # Verify subprocess was called
        mock_subprocess.assert_called_once_with(["python3", "check_access.py"])
        
        # Verify messagebox was called with correct message
        mock_messagebox.showinfo.assert_called_once_with(
            "Access Checked",
            "Access has been checked. The Engineer with name Test User has entered inside the data center."
        )

def test_logout_user_success(mock_db_connection, mock_tkinter):
    """Test successful user logout"""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, "John Doe")]
    mock_messagebox = mock_tkinter["messagebox"]
    
    # Mock the update query
    mock_cursor.execute.side_effect = [None, None]  # First for select, then for update
    
    with patch("access_control_app.messagebox", mock_messagebox):
        logout_user()
        assert mock_cursor.execute.call_count == 2  # One for select, one for update
        mock_messagebox.showinfo.assert_called_once_with(
            "User Logged Out",
            "John Doe has been logged out."
        )

def test_logout_user_no_user(mock_db_connection, mock_tkinter):
    """Test logout when no user is signed in"""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = []
    mock_messagebox = mock_tkinter["messagebox"]
    
    # Mock the messagebox import
    with patch("access_control_app.messagebox", mock_messagebox):
        logout_user()
        mock_messagebox.showinfo.assert_called_once_with(
            "No User Found",
            "No user is currently signed in."
        ) 