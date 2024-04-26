#!/usr/bin/env python3

import csv
from io import StringIO
from bs4 import BeautifulSoup
import subprocess
import os
import re
import pandas

dbob_years = [2014, 2015, 2016, 2018, 2019, 2021, 2022, 2023, 2024]

dbob_columns = ['Name wie von SEC verwendet']
for y in dbob_years:
  dbob_columns.append(str(y) + ' Don’t Bank on the Bomb')

dbob = {}
with open('dbob.csv', 'r') as f:
  reader = csv.DictReader(f)
  for row in reader:
    names = []
    for column in dbob_columns:
      if row[column] != "":
        names.append(row[column])
    dbob[names[0]] = row
    dbob[names[0]]['names'] = names
    # treating dates of the format yyyymmdd as numbers for comparison purposes
    dbob[names[0]]['dbob_from'] = 99999999
    dbob[names[0]]['dbob_to']   = 00000000
    for y in dbob_years:
      if(row[str(y) + ' Don’t Bank on the Bomb'] != ""):
        dbob[names[0]]['dbob_from'] = y * 10000
        break
    for y in dbob_years:
      if(row[str(y) + ' Don’t Bank on the Bomb'] != ""):
        dbob[names[0]]['dbob_to'] = y * 10000 + 1231
      
results = [["Datum", "CH-Firma", "CH-CIK", "Atombombenhersteller", "Wert in USD"]]
for filename in os.listdir('data/13fs/'):
  with open("data/13fs/" + filename, 'r') as f:
    text = f.read()
    
    pgp = re.match("^-+[^\r\n]*-+[^=]*==\s*(<.*)", text)
    if(pgp):
      text = text.replace(pgp[0], pgp[1])

    submission = BeautifulSoup(text, 'xml')
    if(len(submission.find_all('TYPE')) > 0):
      is_form13fhr = str(submission.find_all('TYPE')[0])[:12] == '<TYPE>13F-HR'
    else:
      print("Didn't find form type - this is a problem. Filename: data/13fs/" + filename)
      continue
    if(is_form13fhr):
      try:
        sec_header = text#str(submission.find('ACCEPTANCE-DATETIME'))
        # TODO: when reading 0001535602-22-000005.txt the commented part results in a text
        # with a missing & in BANQUE PICTET & CIE SA, which is unacceptable.
        # Hopefully just looking for the header values anywhere in the text is ok instead.
        date = int(re.search('CONFORMED PERIOD OF REPORT:\s*([0-9]+)\s+', sec_header)[1])
        cik = int(re.search('CENTRAL INDEX KEY:\s*([0-9]+)\s+', sec_header)[1])
        nameCH = re.search('COMPANY CONFORMED NAME:([^\r\n]+)[\r\n]+', sec_header)[1]
        nameCH = nameCH.strip()
      except:
        print("Couldn't read header in file data/13fs/" + filename)
        continue

      if(submission.find('edgarSubmission') and submission.find('edgarSubmission').find('schemaVersion')):
        timesThousand = False
        assert(date>20220000) # if this isn't true the parsing is broken
      else:
        timesThousand = True
        assert(date<20230000)

      infoTable = submission.find_all('infoTable')
      dumbTable = submission.find('TABLE')
      if(len(infoTable) > 0):
        for line in infoTable:
          name = line.find('nameOfIssuer').text

          value = int(line.find('value').text)
          if(timesThousand):
            value *= 1000

          if(nameCH == 'BANQUE PICTET & CIE SA' and name == 'HONEYWELL INTL INC' and date == 20220930):
            value = 48382229 # this number is likely 1000 times too large in the source document
          
          info = [date, nameCH, cik, name, value]
          isDBOB = False
          for k in dbob:
            if name in dbob[k]['names']:
              isDBOB = True
              name = k
              break

          if(isDBOB and dbob[name]['dbob_from'] <= (date+5) and dbob[name]['dbob_to'] >= date):
            results.append(info)
      elif(dumbTable):
        print(str(date) + ": Has dumb table, skipping file data/13fs/" + filename)
        continue # TODO: stop skipping bad tables
        tableText = dumbTable.find('C').find('C').text
        with StringIO(tableText) as f:
          table = pandas.read_fwf(f, on_bad_lines="warn")
        import pdb; pdb.set_trace()
      else:
        print(str(date) + ": Couldn't find infoTable or dumbTable in file data/13fs/" + filename)


with open('results.csv', 'w', newline='') as f:
  csv.writer(f).writerows(results)