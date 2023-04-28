#!/usr/bin/env python3

import pandas
import matplotlib
import matplotlib.pyplot as plt


df = pandas.read_csv('results.csv', parse_dates=[0], date_format='%Y%m%d')

df2 = df.groupby(['Atombombenhersteller', 'Datum'])['Wert in USD'].sum().unstack().transpose()
df2 = df2.fillna(0)

df = df.groupby(['CH-Firma', 'Datum'])['Wert in USD'].sum().unstack().transpose()
df = df.fillna(0)

df['UBS AG'] += df['UBS Group AG']
df = df.rename(columns={'UBS AG': 'UBS'})
del df['UBS Group AG']

df['Pictet North America Advisors SA'] += df['PICTET ASSET MANAGEMENT SA'] + df['BANQUE PICTET & CIE SA']
df = df.rename(columns={'Pictet North America Advisors SA': 'Pictet'})
del df['PICTET ASSET MANAGEMENT SA']
del df['BANQUE PICTET & CIE SA']

df['EDMOND DE ROTHSCHILD (SUISSE) S.A.'] += df['EDMOND DE ROTHSCHILD HOLDING S.A.']
df = df.rename(columns={'EDMOND DE ROTHSCHILD (SUISSE) S.A.': 'Edmond de Rothschild'})
del df['EDMOND DE ROTHSCHILD HOLDING S.A.']

df['Compagnie Lombard, Odier SCA'] += df['Compagnie Lombard Odier SCmA']
df = df.rename(columns={'Compagnie Lombard, Odier SCA': 'Compagnie Lombard, Odier'})
del df['Compagnie Lombard Odier SCmA']

df['Andere'] = df['Vontobel Holding Ltd.']
del df['Vontobel Holding Ltd.']
for c in ['GVO Asset Management Ltd', 'Jabre Capital Partners S.A.', 'Compagnie Lombard, Odier', 'Compagnie Odier SCA', 'Edmond de Rothschild', 'Freemont Management S.A.', 'GAM Holding AG', 'ARGENTIERE CAPITAL AG', 'Ameliora Wealth Management Ltd.', 'Banque Cantonale Vaudoise', 'Bellecapital International Ltd.']:
  df['Andere'] += df[c]
  del df[c]


df['Andere'] += df['Vontobel Swiss Wealth Advisors AG']
del df['Vontobel Swiss Wealth Advisors AG']
df['Andere'] += df['Zurich Insurance Group Ltd/FI']
del df['Zurich Insurance Group Ltd/FI']
df['Andere'] += df['Zurcher Kantonalbank (Zurich Cantonalbank)']
del df['Zurcher Kantonalbank (Zurich Cantonalbank)']
df['Andere'] += df['UBP Investment Advisors SA']
del df['UBP Investment Advisors SA']
df['Andere'] += df['ROBECOSAM AG']
del df['ROBECOSAM AG']
df['Andere'] += df['LFA - Lugano Financial Advisors SA']
del df['LFA - Lugano Financial Advisors SA']
df['Andere'] += df['Lombard Odier Asset Management (Switzerland) SA']
del df['Lombard Odier Asset Management (Switzerland) SA']

df.plot(kind='area', colormap='Greys', xlabel="Datum", ylabel="Milliarden USD")
plt.savefig('schweizerUnternehmen.pdf')  # saves the current figure

df = df.rename(columns={'Andere': 'Autres'})
df.plot(kind='area', colormap='Greys', xlabel="Date", ylabel="Milliards de USD")
plt.savefig('entreprisesSuisses.pdf')  # saves the current figure

df2['Andere'] = df2['AECOM']
del df2['AECOM']
for c in ['AEROJET ROCKETDYNE HLDGS INC', 'BWX TECHNOLOGIES INC', 'FLUOR CORP NEW', 'HUNTINGTON INGALLS INDS INC', 'JACOBS SOLUTIONS INC', 'MOOG INC', 'TEXTRON INC']:
  df2['Andere'] += df2[c]
  del df2[c]

df2.plot(kind='area', colormap='Greys', xlabel="Datum", ylabel="Milliarden USD")
plt.savefig('atombombenhersteller.pdf')  # saves the current figure

df2.plot(kind='area', colormap='Greys', xlabel="Date", ylabel="Milliards de USD")
plt.savefig('fabricant darmes nucleaires.pdf')  # saves the current figure