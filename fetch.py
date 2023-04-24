#!/usr/bin/env python3

from time import sleep
import requests
import subprocess
import os
import re
import json
import pandas

headers = {
    'User-Agent': 'GSoA Switzerland',
    'From': 'lukas@gsoa.ch'
}
countryOfInterest = 'V8' # V8 is Switzerland, check on https://www.sec.gov/edgar/search/#/locationCode=V8
wgetHeaders = " --header='User-Agent:" + headers['User-Agent'] + ",From:" + headers['From'] + "' " # not sure if this sends the second header as part of the value of the first TODO

subprocess.run('mkdir -p data', shell=True, check=True)
subprocess.run('mkdir -p data/13fs', shell=True, check=True)

if(not os.path.exists('data/submissions.zip')):
  subprocess.run("cd data; wget " + wgetHeaders + " https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip", shell=True, check=True)

if(not os.path.isdir('data/submissions')):
  subprocess.run("cd data; unzip submissions.zip -d submissions", shell=True, check=True)

for filename in os.listdir('data/submissions/'):
  if(not re.match('CIK[0-9]+.json', filename)):
    continue
  with open("data/submissions/" + filename, 'r') as f:
    submission = json.load(f)
    country = None
    for a in submission['addresses']:
      if(submission['addresses'][a]['stateOrCountry'] == countryOfInterest):
        country = countryOfInterest
    if(not country):
      continue
    filingsList = pandas.DataFrame(submission['filings']['recent']).to_dict(orient="records")
    # TODO: This list contains a maximum of 1000 entries, more entries need to be fetched from other files
    form13fs = filter(lambda l: re.match('13F', l['form']), filingsList)
    for form in form13fs:
      url = 'https://www.sec.gov/Archives/edgar/data/' + submission['cik'] + "/" + form['accessionNumber'].replace('-', '') + "/" + form['accessionNumber'] + '.txt'
      if(not os.path.exists('data/13fs/' + form['accessionNumber'] + '.txt')):
        subprocess.run("cd data/13fs; wget" + wgetHeaders + url, shell=True, check=True)
        sleep(0.12)