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
    'limited_tendering_reason_code':str
}

df = pd.read_csv('C:/Users/danli/documents/github/trade_analysis/df.csv',
                 usecols=usecols,
                 dtype=dtype
)

thresholds = pd.read_csv('C:/Users/danli/documents/github/trade_analysis/thresholds.csv')
thresholds.set_index('Type', inplace=True)
trade_agreements = [
    'NAFTA',
    'CCFTA',
    'CCoFTA',
    'CHFTA',
    'CPaFTA',
    'CPFTA',
    'CKFTA',
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
df['thresholds'] = 'Unknown'

'''
1) Procurement is not covered, value is above thresholds 'Unknown'
2) Procurement is not covered, value is below thresholds 'Yes'
3) Procurement is covered, value is above thresholds 'Yes'
4) Procurement is covered, value is below thresholds 'No'
'''
i = df
commodities = ['Goods', 'Services', 'Construction']
for x in agreement_codes:
    for c in commodities:
        if x == '0':
            dollar = thresholds.loc[c].at['CFTA']
            i.loc[((i['original_value'] > dollar) & (i['agreement_type_code'] == x) & (i['commodity_type_code'] == c)), 'thresholds'] = 'Unknown'
            i.loc[((i['original_value'] < dollar) & (i['agreement_type_code'] == x) & (i['commodity_type_code'] == c)), 'thresholds'] = 'Yes'
        else:
            dollar = thresholds.loc[c].at[x]
            i.loc[((i['original_value'] > dollar) & (i['agreement_type_code'] == x) & (i['commodity_type_code'] == c)), 'thresholds'] = 'Yes'
            i.loc[((i['original_value'] < dollar) & (i['agreement_type_code'] == x) & (i['commodity_type_code'] == c)), 'thresholds'] = 'No'

i.to_csv('C:/Users/danli/documents/github/trade_analysis/df_thresholds.csv')
