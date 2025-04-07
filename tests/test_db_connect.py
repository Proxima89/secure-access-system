import pytest
from unittest.mock import patch, MagicMock
from db_connect import db_connection

def test_db_connection_success():
    """Test successful database connection"""
    mock_connection = MagicMock()
    
    with patch("mysql.connector.connect", return_value=mock_connection) as mock_connect, \
         patch("os.getenv") as mock_getenv:
        
        # Setup environment variables
        mock_getenv.side_effect = lambda x: {
            "HOST": "localhost",
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_password",
            "DATABASE": "test_db"
        }.get(x)
        
        connection = db_connection()
        
        # Verify connection was created with correct parameters
        mock_connect.assert_called_once_with(
            host="localhost",
            user="test_user",
            passwd="test_password",
            database="test_db"
        )
        assert connection == mock_connection

def test_db_connection_error():
    """Test database connection error handling"""
    with patch("mysql.connector.connect", side_effect=Exception("Connection error")), \
         patch("os.getenv") as mock_getenv:
        
        # Setup environment variables
        mock_getenv.side_effect = lambda x: {
            "HOST": "localhost",
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_password",
            "DATABASE": "test_db"
        }.get(x)
        
        with pytest.raises(Exception) as exc_info:
            db_connection()
        
        assert str(exc_info.value) == "Connection error" 