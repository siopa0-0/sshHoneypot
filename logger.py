import datetime
import config

log_file = config.LOG_FILE

def get_formatted_time():
    return datetime.datetime.now().strftime("%c")

def log_event(message):
    timestamp = get_formatted_time()
    with open(log_file, 'a') as log:
        log.write(f"[{timestamp}] {message}\n")
