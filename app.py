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

# from db import Loan, LoanRequest
# from modules.utils.src import parseLoanRequestFile, move_file, displayLoanRequest, checkCustomerExistence, checkHouseExistence, getCustomer, getHouse, checkValueInterval, createLoanRequest, getCustomerSolvabilityScore, getPropertyEvaluationScore, getLoanRequest, createLoan, getLoan, modifyLoanRequestStatus, displayLoan

from env import URL, NEW_LOAN_REQUEST_DIR, LOG_DIR, ASSESSMENT_LOAN_REQUEST_DIR, SCORE_TRESHOLD, ACCEPTED_LOAN_REQUEST_DIR, REFUSED_LOAN_REQUEST_DIR, CUSTOMER_MANAGER_ADDR, CUSTOMER_MANAGER_PORT, MIN_LOAN_AMOUNT, MAX_LOAN_AMOUNT, MIN_LOAN_DURATION, MAX_LOAN_DURATION, HOUSE_MANAGER_ADDR, HOUSE_MANAGER_PORT, LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT, SOLVABILITY_CHECKER_MANAGER_ADDR, SOLVABILITY_CHECKER_MANAGER_PORT, PROPERTY_EVALUATION_MANAGER_ADDR, PROPERTY_EVALUATION_MANAGER_PORT, LOAN_MANAGER_ADDR, LOAN_MANAGER_PORT


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
                                url = f"{URL}/predict_price/{new_loan_request['house_id']}/"
                                response = requests.get(url)
                                if response.status_code != 200:
                                    log_progress(
                                        f"Property evaluation failed. Error code: {response.status_code}. The loan request is canceled.")
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

        """
        # create loan application in the system
        newLoanRequestID = createLoanRequest(new_application.customerID, new_application.houseID, new_application.amount,
                                             new_application.duration, LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
        if newLoanRequestID == LOAN_REQUEST_CREATION_ERROR:
            print("Loan Request creation error. Please try again later. Thank you!")
            modifyLoanRequestStatus(
                newLoanRequestID, "rejected", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
            move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
            return

        newLoanRequest = getLoanRequest(
            newLoanRequestID, LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
        displayLoanRequest(newLoanRequest)
        # print("Your applicaiton is under review. You will get a result soon. Thank you!\n")

        # check the status of the customer
        customer = getCustomer(new_application.customerID,
                               CUSTOMER_MANAGER_ADDR, CUSTOMER_MANAGER_PORT)
        if customer == CUSTOMER_NOT_EXIST:
            print("Please create an account first. Thank you")
            modifyLoanRequestStatus(
                newLoanRequestID, "rejected", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
            move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
            return

        # check loan amount interval
        if not checkValueInterval(new_application.amount, MIN_LOAN_AMOUNT, MAX_LOAN_AMOUNT):
            print("Min or Max loan amount requirement not satisfied. Minimum and Maximum allowed are respectively {} euros and {} euros. Please change it and submit again. Thank you!".format(
                MIN_LOAN_AMOUNT, MAX_LOAN_AMOUNT))
            modifyLoanRequestStatus(
                newLoanRequestID, "rejected", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
            move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
            return

        # check loan duration interval
        if not checkValueInterval(new_application.duration, MIN_LOAN_DURATION, MAX_LOAN_DURATION):
            print("Min or Max loan duration requirement not satisfied. Minimum and Maximum allowed are respectively {} months and {} months. Please change it and submit again. Thank you!".format(
                MIN_LOAN_DURATION, MAX_LOAN_DURATION))
            modifyLoanRequestStatus(
                newLoanRequestID, "rejected", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
            move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
            return

        # check house existence
        house = getHouse(new_application.houseID,
                         HOUSE_MANAGER_ADDR, HOUSE_MANAGER_PORT)
        if house == HOUSE_NOT_EXIST:
            print("The house for which you request the loan don't exist. Please change it and submit again. Thank you!")
            modifyLoanRequestStatus(
                newLoanRequestID, "rejected", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
            move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
            return

        move_file(new_loan_request_file, ASSESSMENT_LOAN_REQUEST_DIR)
        new_loan_request_file = os.path.join(
            ASSESSMENT_LOAN_REQUEST_DIR, file_name)

        # print(new_loan_request_file)

        # Get customer solvability score
        res = getCustomerSolvabilityScore(
            customer.id, newLoanRequestID, SOLVABILITY_CHECKER_MANAGER_ADDR, SOLVABILITY_CHECKER_MANAGER_PORT)
        if res == UNABLE_TO_GET_SOLVABILITY_SCORE:
            print("Unable to get solvability score")
            modifyLoanRequestStatus(
                newLoanRequestID, "rejected", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
            move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
            return
        creditScore = res
        # print("Credit score: ", res)

        # get property evaluation score
        res = getPropertyEvaluationScore(
            house.id, PROPERTY_EVALUATION_MANAGER_ADDR, PROPERTY_EVALUATION_MANAGER_PORT)
        if res == UNABLE_TO_GET_PROPERTY_EVALUATION_SCORE:
            print("Unable to get property evaluation score")
            modifyLoanRequestStatus(
                newLoanRequestID, "rejected", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
            move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
            return

        propertyEvaluationScore = res
        # print("Property Evaluation Score: ", res)

        globalScore = (creditScore + propertyEvaluationScore)/2

        print("Global Score: ", globalScore)

        # return the result to customer
        if globalScore >= 0.5:
            # create new loan
            loanID = createLoan(loanRequestID=newLoanRequestID, startDate="kim", amount=newLoanRequest.amount,
                                duration=newLoanRequest.duration, adr=LOAN_MANAGER_ADDR, port=LOAN_MANAGER_PORT)
            if loanID == LOAN_CREATION_ERROR:
                print("loan creation error")
                modifyLoanRequestStatus(
                    newLoanRequestID, "accepted", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
                move_file(new_loan_request_file, ACCEPTED_LOAN_REQUEST_DIR)
                return
            newLoan = getLoan(loanID, LOAN_MANAGER_ADDR, LOAN_MANAGER_PORT)

            # print loan details
            print("Your loan request is appoved. The loan details are: ")
            displayLoan(newLoan)

            # update associated loan request status
            modifyLoanRequestStatus(
                newLoanRequestID, "accepted", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
            move_file(new_loan_request_file, ACCEPTED_LOAN_REQUEST_DIR)

        else:
            print("Your loan request is rejected.")
            # update associated loan request status
            modifyLoanRequestStatus(
                newLoanRequestID, "rejected", LOAN_REQUEST_MANAGER_ADDR, LOAN_REQUEST_MANAGER_PORT)
            move_file(new_loan_request_file, REFUSED_LOAN_REQUEST_DIR)
"""


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
