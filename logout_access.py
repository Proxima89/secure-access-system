import mysql.connector
from db_connect import db_connection

def logout_user():
  """
  Log out the user by updating the clock_out time in the attendance table.
  """
  try:
    # Simulate card tap and get user_id (replace with actual card reading logic)
    user_id = get_user_id_from_card()

    db = db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE attendance SET clock_out = NOW() WHERE user_id = %s AND clock_out IS NULL", (user_id,))
    db.commit()
  except mysql.connector.Error as err:
    print(f"Error: {err}")
  finally:
    cursor.close()
    db.close()

def get_user_id_from_card():
  """
  Simulate card reading logic to get the user_id.
  Replace this function with actual card reading logic.
  """
  return 1  # Example user_id

def main():
  """
  Main function to log out the user.
  """
  logout_user()

if __name__ == "__main__":
  main()
