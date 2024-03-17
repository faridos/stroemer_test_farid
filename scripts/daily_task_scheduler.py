import schedule
import time
import subprocess
import os
import django
import sys

# Add the parent directory of the project to the Python path
# to solve the error: ModuleNotFoundError: No module named stroemer_test_farid
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stroemer_test_farid.settings')
django.setup()


def run_daily_task():
    # Use subprocess to call the Django management command
    log_file = 'daily_task_log.txt'
    with open(log_file, 'a') as f:
        subprocess.run(
            ['docker-compose', 'run', '--rm', 'app', 'python', 'manage.py', 'fetch_posts_comments'],
            stdout=f,
            stderr=subprocess.STDOUT
        )


# Schedule the task to run daily at a specific time
# schedule.every().day.at("02:00").do(run_daily_task)
schedule.every().minute.do(run_daily_task)

# Main loop to run the scheduler
while True:
    schedule.run_pending()
    time.sleep(30)  # Sleep for 60 seconds before checking again
