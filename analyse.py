#!/usr/bin/env python3

import csv
from bs4 import BeautifulSoup
import subprocess
import os
import re
import pandas

dbob_years = [2014, 2015, 2016, 2018, 2019, 2021, 2022]

dbob = {}
with open('dbob.csv', 'r') as f:
  reader = csv.DictReader(f)
  for row in reader:
    dbob[row['Name wie von SEC verwendet']] = row
    # treating dates of the format yyyymmdd as numbers for comparison purposes
    dbob[row['Name wie von SEC verwendet']]['dbob_from'] = 99999999
    dbob[row['Name wie von SEC verwendet']]['dbob_to']   = 00000000
    for y in dbob_years:
      if(row[str(y) + ' Don’t Bank on the Bomb'] != ""):
        dbob[row['Name wie von SEC verwendet']]['dbob_from'] = y * 10000
        break
    for y in dbob_years:
      if(row[str(y) + ' Don’t Bank on the Bomb'] != ""):
        dbob[row['Name wie von SEC verwendet']]['dbob_to'] = y * 10000 + 1231
      
results = ["Datum", "CH-Firma investiert in...", "Firma mit diesem CIK", "und diesem Namen", "Wert in USD"]
for filename in os.listdir('data/13fs/'):
  with open("data/13fs/" + filename, 'r') as f:
    submission = BeautifulSoup(f, 'xml')
    try:
      is_form13fhr = str(submission.find_all('TYPE')[0])[:12] == '<TYPE>13F-HR'
    except:
      print("Parsing error on file " + filename + ", hoping it's not the type of interest anyway.")
      #TODO check this hopeful assumption is correct
      continue
    if(is_form13fhr):
      sec_header = str(submission.find('ACCEPTANCE-DATETIME'))
      date = int(re.search('CONFORMED PERIOD OF REPORT:\s*([0-9]+)\s+', sec_header)[1])
      cik = int(re.search('CENTRAL INDEX KEY:\s*([0-9]+)\s+', sec_header)[1])
      nameCH = re.search('COMPANY CONFORMED NAME:([^\r\n]+)[\r\n]+', sec_header)[1]
      nameCH = nameCH.strip()
      for line in submission.find_all('infoTable'):
        name = line.find('nameOfIssuer').text
        value = int(line.find('value').text)
        info = [date, nameCH, cik, name, value]
        # TODO check by CIK instead of name
        if(name in dbob and dbob[name]['dbob_from'] <= date and dbob[name]['dbob_to'] >= date):
          results += info

with open('results.txt', 'w', newline='') as f:
  csv.writer(f).writerows(results)