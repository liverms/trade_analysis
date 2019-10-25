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

df = df.merge(ent, how='outer', left_on='abbreviation', right_on='Abbreviation')

trade_agreements = [
    'NAFTA',
    'CCFTA',
    'CCoFTA',
    'CHFTA',
    'CPaFTA',
    'CPFTA',
    'CKFTA',
    'CUFTA',
    'WTO-AGP',
    'CETA',
    'CPTPP',
    '0'
]

for x in trade_agreements:
    if x == '0':
        val = df
    else:
        val = df[df[x] == 'No']

    val = val[val['agreement_type_code'] == x]
    val = val.reset_index()
    val = val[usecols]
    print(val)






