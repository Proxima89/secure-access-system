from db_connect import db_connection
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector

def execute_query(query, params=None):
  try:
    db = db_connection()
    cursor = db.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result
  except mysql.connector.Error as err:
    print(f"Error: {err}")
    return None

def main():
  reader = SimpleMFRC522()

  try:
    while True:
      id, text = reader.read()
      query = "SELECT id FROM users WHERE rfid_uid=%s"
      result = execute_query(query, (str(id),))

      if result and len(result) >= 1:
        overwrite = input("Overwrite (Y/N)? ")
        if overwrite[0].lower() == "y":
          time.sleep(1)
          sql_insert = "UPDATE users SET name = %s WHERE rfid_uid=%s"
        else:
          continue
      else:
        sql_insert = "INSERT INTO users (name, rfid_uid) VALUES (%s, %s)"

      new_name = input("Name: ")
      execute_query(sql_insert, (new_name, id))
      time.sleep(2)
  finally:
    GPIO.cleanup()

if __name__ == "__main__":
  main()
