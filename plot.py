#!/usr/bin/env python3

import pandas
import matplotlib
import matplotlib.pyplot as plt

def aggregateInvestors(df):
  df['UBS AG'] += df['UBS Group AG']
  df = df.rename(columns={'UBS AG': 'UBS'})
  del df['UBS Group AG']

  df['Pictet North America Advisors SA'] += df['PICTET ASSET MANAGEMENT SA'] + df['BANQUE PICTET & CIE SA'] + df['Pictet Asset Management Holding SA']
  df = df.rename(columns={'Pictet North America Advisors SA': 'Pictet'})
  del df['PICTET ASSET MANAGEMENT SA']
  del df['BANQUE PICTET & CIE SA']
  del df['Pictet Asset Management Holding SA']

  df['EDMOND DE ROTHSCHILD (SUISSE) S.A.'] += df['EDMOND DE ROTHSCHILD HOLDING S.A.']
  df = df.rename(columns={'EDMOND DE ROTHSCHILD (SUISSE) S.A.': 'Edmond de Rothschild'})
  del df['EDMOND DE ROTHSCHILD HOLDING S.A.']

  df['Compagnie Lombard, Odier SCA'] += df['Compagnie Lombard Odier SCmA']
  df = df.rename(columns={'Compagnie Lombard, Odier SCA': 'Compagnie Lombard, Odier'})
  del df['Compagnie Lombard Odier SCmA']

  df = df.rename(columns={'CREDIT SUISSE AG/': 'Credit Suisse'})

  df['Andere'] = df['Vontobel Holding Ltd.']
  del df['Vontobel Holding Ltd.']
  for c in ['Vontobel Swiss Wealth Advisors AG', 'Zurich Insurance Group Ltd/FI', 'Zurcher Kantonalbank (Zurich Cantonalbank)', 'UBP Investment Advisors SA', 'ROBECOSAM AG', 'LFA - Lugano Financial Advisors SA', 'Lombard Odier Asset Management (Switzerland) SA', 'GVO Asset Management Ltd', 'Jabre Capital Partners S.A.', 'Compagnie Lombard, Odier', 'Compagnie Odier SCA', 'Edmond de Rothschild', 'Freemont Management S.A.', 'GAM Holding AG', 'ARGENTIERE CAPITAL AG', 'Ameliora Wealth Management Ltd.', 'Banque Cantonale Vaudoise', 'Bellecapital International Ltd.']:
    df['Andere'] += df[c]
    del df[c]
  return(df)

def aggregateProducers(df2):
  df2['Andere'] = df2['AECOM']
  del df2['AECOM']
  for c in ['AEROJET ROCKETDYNE HLDGS INC', 'BWX TECHNOLOGIES INC', 'FLUOR CORP NEW', 'HUNTINGTON INGALLS INDS INC', 'JACOBS SOLUTIONS INC', 'MOOG INC', 'TEXTRON INC']:
    df2['Andere'] += df2[c]
    del df2[c]
  return(df2)

df = pandas.read_csv('results.csv', parse_dates=[0], date_format='%Y%m%d')

df3 = df.rename(columns={'CH-Firma': 'Investisseurs suisses dans la bombe atomique'})
df = df.rename(columns={'CH-Firma': 'Schweizer Atomwaffen-Investoren'})

df4 = df.rename(columns={'Atombombenhersteller': 'Fabricants de bombes atomiques'})
df4 = df4.groupby(['Fabricants de bombes atomiques', 'Datum'])['Wert in USD'].sum().unstack().transpose()

df2 = df.groupby(['Atombombenhersteller', 'Datum'])['Wert in USD'].sum().unstack().transpose()
df2 = df2.fillna(0)

df = df.groupby(['Schweizer Atomwaffen-Investoren', 'Datum'])['Wert in USD'].sum().unstack().transpose()
df = df.fillna(0)

df3 = df3.groupby(['Investisseurs suisses dans la bombe atomique', 'Datum'])['Wert in USD'].sum().unstack().transpose()
df3 = df3.fillna(0)

df = aggregateInvestors(df)
df3 = aggregateInvestors(df3)

print(f"Total 2023: {df.loc['2023-12-31'].sum()}")
print(f"Total 2023 Swiss National Bank: {df.loc['2022-12-31', 'Swiss National Bank']}")

df.plot(kind='area', colormap='Greys', xlabel="Jahr", ylabel="Milliarden USD")
for suffix in ['.pdf', '.webp']: # save the current figure
  plt.savefig('schweizerUnternehmen' + suffix, dpi=300)

df3 = df3.rename(columns={'Andere': 'Autres'})
df3.plot(kind='area', colormap='Greys', xlabel="Année", ylabel="Milliards de USD")
for suffix in ['.pdf', '.webp']: # save the current figure
  plt.savefig('entreprisesSuisses' + suffix, dpi=300)

df2 = aggregateProducers(df2)
df2.plot(kind='area', colormap='Greys', xlabel="Jahr", ylabel="Milliarden USD")
for suffix in ['.pdf', '.webp']: # save the current figure
  plt.savefig('atombombenhersteller' + suffix, dpi=300)

df4 = aggregateProducers(df4)
df4 = df4.rename(columns={'Andere': 'Autres'})
df4.plot(kind='area', colormap='Greys', xlabel="Année", ylabel="Milliards de USD")
for suffix in ['.pdf', '.webp']: # save the current figure
  plt.savefig('fabricant darmes nucleaires' + suffix, dpi=300)