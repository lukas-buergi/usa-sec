#!/usr/bin/env python3

import pandas
import matplotlib
import matplotlib.pyplot as plt


df = pandas.read_csv('results.csv', parse_dates=[0], date_format='%Y%m%d')
#df = df.groupby(['Atombombenhersteller', 'Datum'])['Wert in USD'].sum().unstack().transpose()
df = df.groupby(['CH-Firma', 'Datum'])['Wert in USD'].sum().unstack().transpose()


df.plot(kind='area')#, colormap='Greys')
plt.savefig('figure.pdf')  # saves the current figure