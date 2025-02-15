import subprocess
import time

def run_check_access():
  try:
    subprocess.run(["python3", "check_access.py"], check=True)
  except subprocess.CalledProcessError as e:
    print("Error running check_access.py:", e)

if __name__ == "__main__":
  while True:
    run_check_access()
    # Add a delay to control how often the scripts run
    time.sleep(1)  # Adjust delay as needed
