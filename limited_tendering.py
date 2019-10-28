import pandas as pd
import numpy as np


usecols=[
    'original_value',
    'commodity_type_code',
    'commodity_code',
    'reporting_period',
    'owner_org_title',
    'document_type_code',
    'agreement_type_code',
    'procurement_id',
    'abbreviation',
    'limited_tendering_reason_code'
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
    'abbreviation': str,
    'limited_tendering_reason_code': str
}

df = pd.read_csv('C:/Users/danli/documents/github/trade_analysis/df.csv',
                 usecols=usecols,
                 dtype=dtype
)


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
    'CPTPP'
]
agreement_codes = [
    'CFTA',
    '0',
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
    'CPTPP'
]

limited_tendering_reason=[
    '00',
    '05',
    '20',
    '21',
    '22',
    '22',
    '71',
    '72',
    '74',
    '81',
    '23',
    '24',
    '25',
    '86',
    '90',
    '87',
    '85'
]
df = df[df['limited_tendering_reason_code'].isin(limited_tendering_reason)]
df['lt_rule'] = 'Unknown'


'''
1) Procurement not covered, limited tendering not invoked = 'Yes'
2) Procurement not covered, limited tendering invoked = 'no_it_lt' (default)
3) Procurement covered, limited tendering invoked = 'it_ly'
4) Procurement covered, limited tendering not invoked = 'it_no_lt'
'''
i = df
for x in agreement_codes:
    if x == '0':
        i.loc[((i['agreement_type_code'] == x) & (i['limited_tendering_reason_code'] == '00')), 'lt_rule'] = 'Yes'
        i.loc[((i['agreement_type_code'] == x) & (i['limited_tendering_reason_code'] != '00')), 'lt_rule'] = 'no_it_lt'
    else:
        i.loc[((i['agreement_type_code'] == x) & (i['limited_tendering_reason_code'] != '00')), 'lt_rule'] = 'it_ly'
        i.loc[((i['agreement_type_code'] == x) & (i['limited_tendering_reason_code'] == '00')), 'lt_rule'] = 'it_no_lt'

i.to_csv('C:/Users/danli/documents/github/trade_analysis/limited.csv')
