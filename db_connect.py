import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def db_connection():
  connection = mysql.connector.connect(
  host=os.getenv("HOST"),
  user=os.getenv("DB_USER"),
  passwd=os.getenv("DB_PASSWORD"),
  database=os.getenv("DATABASE")
  )

  return connection
