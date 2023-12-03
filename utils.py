"""
This module defined some useful function for the main process
"""
import os
import shutil
from datetime import datetime

from api_v1.schemas import LoanRequestCreate


def generate_new_log_file_name(log_dir):
    """
    Return new log file name path
    """
    timestamp_format = "%Y-%h-%d-%H:%M:%S"
    current_time = datetime.now()
    timestamp = current_time.strftime(timestamp_format)
    file_name = "loan_request_" + timestamp + ".txt"
    log_file_path = os.path.join(log_dir, file_name)
    return log_file_path


def log_progress(message, log_file):
    """
    Log a message into a file
    """
    timestamp_format = "%Y-%h-%d-%H:%M:%S"
    current_time = datetime.now()
    timestamp = current_time.strftime(timestamp_format)
    with open(log_file, 'a') as f:
        log_msg = f"{timestamp} : {message}  \n"
        print(log_msg)
        f.write(log_msg)


def count_number_of_lines(file_path):
    """
    Returns the number of lines in a file
    """
    with open(file_path) as f:
        lines = f.readlines()
        return len(lines)


def move_file(source_path, destination_path):
    """
    Move a file from source_path to destination_path
    """
    try:
        shutil.move(source_path, destination_path)
        # print(f"File moved from {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error moving the file: {e}")


def parse_loan_request_file(file_path):
    """
        Parse Loan Request file and return the result as an object 
    """
    with open(file_path) as f:
        line = f.readline()
        customer_id = int(line.split(':')[1].strip())

        line = f.readline()
        loan_amount = int(line.split(':')[1].strip())

        line = f.readline()
        loan_duration = int(line.split(':')[1].strip())

        line = f.readline()
        house_id = int(line.split(':')[1].strip())

        #receive_date = str(datetime.now())

        request_details = {
            "customer_id": customer_id,
            "house_id": house_id,
            "amount": loan_amount,
            "duration": loan_duration
            #"created_at": receive_date
        }

        return request_details
