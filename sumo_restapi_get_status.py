#!/usr/bin/python3
##########################################
# Written by: DK
# Date: 10/27/2018
# Purpose: Python 3 script to get status of Sumo Logic search job using Requests module.

# Documentation: https://help.sumologic.com/APIs/Search-Job-API/About-the-Search-Job-API
#
# Sample return object:
# API returns the following json on success
#   {'state': 'GATHERING RESULTS', 'histogramBuckets': [{'startTimestamp': 1540357200000, 'length': 54000000, 'count': 375755}], 'messageCount': 375755, 'recordCount': 0, 'pendingWarnings': [], 'pendingErrors': []}
#   https://api.us2.sumologic.com/api/v1/search/jobs
##########################################
import requests
from requests.auth import HTTPBasicAuth
import datetime
import time
import pathlib

ACCESS_ID = 'xxxxxxx'
ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxx'

def get_job_status(job_id):
        ''' Return search job status '''
        url = 'https://api.us2.sumologic.com/api/v1/search/jobs/'
        call = requests.get(url + job_id, auth=HTTPBasicAuth(ACCESS_ID, ACCESS_KEY))

        if call.status_code != 200:
                # Bad HTTP Return Code
                return 2

        print("The status code is: {}".format(call.status_code))
        call_json = call.json()

        if call_json['state'] == 'GATHERING RESULTS':
                # Still Getting Results
                return 0
        elif call_json['state'] == 'DONE GATHERING RESULTS':
                # Done Getting Results
                return 1

def get_job_from_file(location_and_filename):
        ''' Return job Id if file exists '''
        ''' Sample job.id file: 235152JHJK2363322 '''

        file = pathlib.Path(location_and_filename)
        # If file exists, return the ID string
        if file.exists():
                with open(location_and_filename) as j:
                        job = j.readline()
                return job
        else:
                return ''

def main():
        # Get job from file
        job_id = get_job_from_file('./job.id')

        print("Getting job status...")
        # Return 'stat code' from file
        stat_code = get_job_status(job_id)
        
        # Stat code response depending if search is in process, has stopped, or failed
        while stat_code != 2:
                if stat_code == 1:
                        print("Finished search job {}".format(job_id))
                elif stat_code == 0:
                        print("Gathering results...")
                else:
                        print("Something wrong with the id")
                time.sleep(2)
                stat_code = get_job_status(job_id)

if __name__ == "__main__":
        main()
