import pandas as pd
from collections import defaultdict

usecols=[
    'original_value',
    'commodity_type_code',
    'commodity_code',
    'reporting_period',
    'owner_org_title',
    'document_type_code',
    'agreement_type_code',
    'procurement_id',
    'abbreviation'
]
#data types of columns
dtype={
    'commodity_type_code': str,
    'commodity_code': str,
    'original_value': float,
    'reporting_period': str,
    'owner_org_title': str,
    'document_type_code':str,
    'agreement_type_code': str,
    'procurement_id': str,
    'abbreviation': str
}

df = pd.read_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/df.csv',
                 usecols=usecols,
                 dtype=dtype
)

ent = pd.read_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/entities_list.csv')
thresholds = pd.read_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/thresholds.csv')
df = df.merge(ent, how='outer', left_on='abbreviation', right_on='Abbreviation')


nafta = df[df['NAFTA'] == 'Yes']
ccfta = df[df['CCFTA'] == 'Yes']
ccofta = df[df['CCoFTA'] == 'Yes']
cpafta = df[df['CPaFTA'] == 'Yes']
cpfta = df[df['CPFTA'] == 'Yes']
ckfta = df[df['CKFTA'] == 'Yes']
wto_agp = df[df['WTO-AGP'] == 'Yes']
ceta = df[df['CETA'] == 'Yes']
cptpp = df[df['CPTPP'] == 'Yes']

nafta = nafta[nafta['agreement_type_code'] == 'NAFTA']
ccfta = ccfta[ccfta['agreement_type_code'] == 'CCFTA']
ccofta = ccofta[ccofta['agreement_type_code'] == 'CCoFTA']
cpafta = cpafta[cpafta['agreement_type_code'] == 'CPaFTA']
cpfta = cpfta[cpfta['agreement_type_code'] == 'CPFTA']
ckfta = ckfta[ckfta['agreement_type_code'] == 'CKFTA']
wto_agp = wto_agp[wto_agp['agreement_type_code'] == 'WTO-AGP']
ceta = ceta[ceta['agreement_type_code'] == 'CETA']
cptpp = cptpp[cptpp['agreement_type_code'] == 'CPTPP']
none = df[df['agreement_type_code'] == '0']

df_list = [nafta, ccfta, ccofta, cpafta, cpfta, ckfta, wto_agp, ceta, cptpp, none]

for x in df_list:
    x=x.reset_index()
    x.drop('index', axis=1, inplace=True)
    print(x)



none.to_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/none.csv')
ccfta.to_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/ccfta.csv')