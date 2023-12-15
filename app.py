"""

Apply the application logic (check the file app_logic.txt)

"""


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


import requests
import json

from utils import log_progress, parse_loan_request_file, count_number_of_lines, generate_new_log_file_name, move_file

import os

from datetime import datetime

from env import URL, NEW_LOAN_REQUEST_DIR, LOG_DIR, ASSESSMENT_LOAN_REQUEST_DIR, SCORE_TRESHOLD, ACCEPTED_LOAN_REQUEST_DIR, REFUSED_LOAN_REQUEST_DIR, MIN_LOAN_AMOUNT, MAX_LOAN_AMOUNT, MIN_LOAN_DURATION, MAX_LOAN_DURATION


class LoanFileHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        # self.watch_dir = loan_request_dir
        # self.assessment_dir = assessment_dir

    def on_created(self, event):
        if event.is_directory:
            return
        new_loan_request_file = event.src_path
        file_name = new_loan_request_file.split('/')[-1]
        # print(file_name)
        log_file = generate_new_log_file_name(LOG_DIR)
        log_progress("New loan request received. File name: " +
                     new_loan_request_file, log_file)

        # 1- Read and parse the content of the file

        log_progress(new_loan_request_file + " parse started.", log_file)
        count_lines = count_number_of_lines(new_loan_request_file)
        if count_lines != 4:
            log_progress(
                f"Loan request rejected: the file {file_name} don't complain to the format. It contains {count_lines} lines.", log_file)
            move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
            print(
                f"The loan request in {file_name} is rejected because it don't complain to the format. Please check it and try again. It is moved to {REFUSED_LOAN_REQUEST_DIR} directory")
        else:
            new_loan_request = parse_loan_request_file(new_loan_request_file)
            # print(new_loan_request)
            move_file(new_loan_request_file, ASSESSMENT_LOAN_REQUEST_DIR)
            log_progress(new_loan_request_file +
                         " parse completed.", log_file)

            new_loan_request_file = os.path.join(
                ASSESSMENT_LOAN_REQUEST_DIR, file_name)

            # 2- Pre-assessment

            log_progress("Pre-assessment phase started.", log_file)
            # check if customer exist
            log_progress("Check if customer exist started.", log_file)
            url = f"{URL}/customers/{new_loan_request['customer_id']}"
            # print(url)
            response = requests.get(url)
            if response.status_code == 404:
                log_progress(
                    f"Loan request rejected: Customer {new_loan_request['customer_id']} don't exist.", log_file)
                print(
                    f"Customer {new_loan_request['customer_id']} don't exist.")
                move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
            else:
                log_progress("Check if house exist started.", log_file)
                url = f"{URL}/houses/{new_loan_request['house_id']}"
                # print(url)
                response = requests.get(url)
                if response.status_code == 404:
                    log_progress(
                        f"Loan request rejected: House {new_loan_request['house_id']} don't exist.", log_file)
                    print(
                        f"House {new_loan_request['house_id']} don't exist.")
                else:
                    log_progress("Pre-assessment phase completed.", log_file)

                    # 3- Loan request creation
                    log_progress("Loan request creation started.", log_file)
                    url = f"{URL}/loanrequests/"
                    response = requests.post(url,
                                             data=json.dumps(new_loan_request))
                    if response.status_code != 200:
                        log_progress(
                            f"Loan request creation  failed. Error code: {response.status_code}. The loan request is rejected")
                        print("System error. Try again later. Thank you.")
                        move_file(new_loan_request_file,
                                  REFUSED_LOAN_REQUEST_DIR)
                    else:
                        log_progress(
                            "Loan request creation completed.", log_file)
                        loan_request = response.json()
                        print(loan_request)
                        # 4- Business Rule Check
                        log_progress(
                            "Loan request creation completed. Business rule check started", log_file)

                        # check amount
                        if new_loan_request['amount'] < MIN_LOAN_AMOUNT or new_loan_request["amount"] > MAX_LOAN_AMOUNT:
                            log_progress(
                                f"Loan amount {new_loan_request['amount']} don't complain with business rule. The loan request is rejected", log_file)
                            print(
                                f"Loan requestion rejected. MIN authorized amount: {MIN_LOAN_AMOUNT}  and MAX authorized amount: {MAX_LOAN_AMOUNT}")

                            # update loan request status
                            loan_request['status'] = "rejected"
                            url = f"{URL}/loanrequests/{loan_request['id']}/"
                            response = requests.put(url,
                                                    data=json.dumps(loan_request))
                            move_file(new_loan_request_file,
                                      REFUSED_LOAN_REQUEST_DIR)

                        # check duration
                        elif new_loan_request['duration'] < MIN_LOAN_DURATION or new_loan_request["duration"] > MAX_LOAN_DURATION:
                            log_progress(
                                f"Loan amount {new_loan_request['duration']} don't complain with business rule. The loan request is rejected", log_file)
                            print(
                                f"Loan requestion rejected. MIN authorized duration: {MIN_LOAN_DURATION}  and MAX authorized duration: {MAX_LOAN_DURATION}")
                            # update loan request status
                            loan_request['status'] = "rejected"
                            url = f"{URL}/loanrequests/{loan_request['id']}/"
                            response = requests.put(url,
                                                    data=json.dumps(loan_request))
                            move_file(new_loan_request_file,
                                      REFUSED_LOAN_REQUEST_DIR)
                        else:
                            log_progress(
                                "Business rule check completed.", log_file)

                            # 5- Customer solvability check
                            log_progress(
                                "Customer solvability check started.", log_file)
                            url = f"{URL}/customer_evaluation/{new_loan_request['customer_id']}/"
                            response = requests.get(url)
                            if response.status_code != 200:
                                log_progress(
                                    f"Customer evaluation failed. Error code: {response.status_code}. The loan request is canceled.")
                                print("System error. Try again later. Thank you.")
                                # update loan request status
                                loan_request['status'] = "canceled"
                                url = f"{URL}/loanrequests/{loan_request['id']}/"
                                response = requests.post(url,
                                                         data=json.dumps(loan_request))
                                move_file(new_loan_request_file,
                                          REFUSED_LOAN_REQUEST_DIR)
                            else:
                                log_progress(
                                    "Customer solvability check completed.", log_file)
                                customer_evaluation_score = response.json()

                                # 6- Property evaluation service
                                log_progress(
                                    "Property evaluation started.", log_file)
                                url = f"{URL}/house_valuation/{new_loan_request['house_id']}/"
                                response = requests.get(url)
                                if response.status_code != 200:
                                    log_progress(
                                        f"Property evaluation failed. Error code: {response.status_code}. The loan request is canceled.", log_file)
                                    print(
                                        "System error. Try again later. Thank you.")
                                    # update loan request status
                                    loan_request['status'] = "canceled"
                                    url = f"{URL}/loanrequests/{loan_request['id']}/"
                                    response = requests.put(url,
                                                            data=json.dumps(loan_request))
                                    move_file(new_loan_request_file,
                                              REFUSED_LOAN_REQUEST_DIR)
                                else:
                                    log_progress(
                                        "Property evaluation completed.", log_file)
                                    property_score = response.json()

                                    # 7- Global score computation
                                    log_progress(
                                        "Gloabal score computation started.", log_file)
                                    global_score = customer_evaluation_score
                                    log_progress(
                                        "Gloabal score computation completed.", log_file)
                                    if global_score >= SCORE_TRESHOLD:
                                        log_progress(
                                            "Loan requested accepted. Loan requested status update started", log_file)
                                        loan_request['status'] = "accepted"
                                        url = f"{URL}/loanrequests/{loan_request['id']}/"
                                        response = requests.put(url,
                                                                data=json.dumps(loan_request))
                                        log_progress(
                                            "Loan requested status update completed", log_file)
                                        move_file(new_loan_request_file,
                                                  ACCEPTED_LOAN_REQUEST_DIR)

                                        log_progress(
                                            "Loan creation started", log_file)
                                        loan = {
                                            "amount": loan_request['amount'],
                                            "duration": loan_request['duration'],
                                            "loan_request_id": loan_request["id"]
                                        }
                                        print(loan)
                                        url = f"{URL}/loans/"
                                        response = requests.post(url,
                                                                 data=json.dumps(loan))
                                        if response.status_code != 200:
                                            log_progress(
                                                f"Loan request creation failed: {response.status_code}.")
                                            print(
                                                "System error. We will to you loan id as soon as possible.")
                                        else:
                                            log_progress(
                                                "Loan creation completed", log_file)
                                            print(
                                                f"Loan details: {response.json()}")
                                    else:
                                        log_progress(
                                            "Loan requested rejected. Loan requested status update started", log_file)
                                        loan_request['status'] = "refused"
                                        url = f"{URL}/loanrequests/{loan_request['id']}/"
                                        response = requests.put(url,
                                                                data=json.dumps(loan_request))
                                        log_progress(
                                            "Loan requested status update completed", log_file)
                                        move_file(new_loan_request_file,
                                                  REFUSED_LOAN_REQUEST_DIR)


if __name__ == "__main__":
    work_dir = NEW_LOAN_REQUEST_DIR
    event_handler = LoanFileHandler()
    observer = Observer()
    observer.schedule(event_handler, work_dir, recursive=True)

    print(f"Waiting for new application. Press Ctrl+C to stop.")
    try:
        observer.start()
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
