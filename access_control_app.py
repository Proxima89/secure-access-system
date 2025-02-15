from db_connect import db_connection
import tkinter as tk
from tkinter import messagebox
import subprocess
import mysql.connector
import os
import sys
import time

# Function to run check access script
def run_check_access():
  subprocess.run(["python3", "check_access.py"])

# Helper function to execute a database query
def execute_query(query, params=None):
  try:
    db = db_connection()
    cursor = db.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    db.close()
    return result
  except mysql.connector.Error as err:
    print(f"Error: {err}")
    return None

# Function to get the latest signed-in user
def get_latest_user():
  query = """
    SELECT users.name, attendance.clock_out
    FROM users
    JOIN attendance ON users.id = attendance.user_id
    ORDER BY attendance.clock_in DESC
    LIMIT 1
  """
  result = execute_query(query)
  if result and len(result) > 0:
    return result[0][0], result[0][1]
  else:
    return "User", None

# Function to check access
def check_access():
  run_check_access()
  user_name, clock_out = get_latest_user()
  if clock_out is None or clock_out == "0000-00-00 00:00:00":
    messagebox.showinfo("Access Checked", f"Access has been checked. The Engineer with name {user_name} has entered inside the data center.")
  else:
    messagebox.showinfo("Access Checked", f"The Engineer with name {user_name} logged out of the data center.")

# Function to display signed-in users
def display_signed_in_users():
  query = "SELECT name FROM users"
  result = execute_query(query)
  if result:
    signed_in_window = tk.Toplevel()
    signed_in_window.title("Signed In Users")

    listbox = tk.Listbox(signed_in_window)
    for user in result:
      listbox.insert(tk.END, user[0])
    listbox.pack()

    close_button = tk.Button(signed_in_window, text="Close", command=signed_in_window.destroy)
    close_button.pack()

# Function to log out the user
def logout_user():
  query = """
    SELECT users.id, users.name
    FROM users
    JOIN attendance ON users.id = attendance.user_id
    ORDER BY attendance.clock_in DESC
    LIMIT 1
  """
  result = execute_query(query)
  if result and len(result) > 0:
    user_id, user_name = result[0]
    update_query = """
      UPDATE attendance
      SET clock_out = NOW()
      WHERE user_id = %s AND clock_out IS NULL
    """
    execute_query(update_query, (user_id,))
    messagebox.showinfo("User Logged Out", f"{user_name} has been logged out.")
  else:
    messagebox.showinfo("No User Found", "No user is currently signed in.")

def main():
  # Create the main application window
  root = tk.Tk()
  root.title("Access Control System")

  # Button to run check access
  check_button = tk.Button(root, text="Check Access", command=check_access)
  check_button.pack(pady=10)

  # Button to display signed-in users
  display_button = tk.Button(root, text="Display Signed In Users", command=display_signed_in_users)
  display_button.pack(pady=10)

  # Button to log out user
  logout_button = tk.Button(root, text="Log Out User", command=logout_user)
  logout_button.pack(pady=10)

  # Start the Tkinter event loop
  root.mainloop()

if __name__ == "__main__":
  while True:
    try:
      main()
    except Exception as e:
      print(f"Error: {e}")
      time.sleep(5)  # Wait before restarting the application
      os.execv(sys.executable, [sys.executable] + sys.argv)
