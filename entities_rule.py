import pandas as pd
import numpy as np
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

df = pd.read_csv('C:/Users/danli/documents/github/trade_analysis/df.csv',
                 usecols=usecols,
                 dtype=dtype
)

ent = pd.read_csv('C:/Users/danli/documents/github/trade_analysis/entities_list.csv')

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
    'CPTPP'
]
agreement_codes = [
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
    'CFTA',
    '0'
]
'''
There are 3 possible outcomes:
1) Procurement not covered by a TA by an entity not covered ('Yes')
2) Procurement not covered by a TA by an entity that is covered ('Maybe')
3) Procurement covered by a TA by an entity not covered ('No')
4) Procurement covered by a TA by an entity covered ('Yes')

'''

df = df[df['agreement_type_code'].isin(agreement_codes)]

for x in agreement_codes:
    i = df
    i['entities_rule'] = 'Unknown'
    if x == 'CFTA':
        pass
    # there is no zero in the columns of df, but there is one in the trade list, this skips in error
    elif x == '0':
        # these are procurements that say they are not covered by a TA
        # loop through the TA columns, if all say No then this is correct, else incorrect

        i.loc[((i['NAFTA'] == 'No') & (i['CCFTA'] == 'No') & (i['CCoFTA'] == 'No') &
              (i['CHFTA'] == 'No') & (i['CPaFTA'] == 'No') & (i['CPFTA'] == 'No') &
              (i['CKFTA'] == 'No') & (i['CUFTA'] == 'No') & (i['WTO-AGP'] == 'No') &
              (i['CETA'] == 'No') & (i['CPTPP'] == 'No')), 'entities_rule'] = 'Yes'

        i.loc[((i['NAFTA'] == 'Yes') | (i['CCFTA'] == 'Yes') | (i['CCoFTA'] == 'Yes') |
              (i['CHFTA'] == 'Yes') | (i['CPaFTA'] == 'Yes') | (i['CPFTA'] == 'Yes') |
              (i['CKFTA'] == 'Yes') | (i['CUFTA'] == 'Yes') | (i['WTO-AGP'] == 'Yes') |
              (i['CETA'] == 'Yes') | (i['CPTPP'] == 'Yes')), 'entities_rule'] = 'Maybe'
    else:
        i.loc[(i['agreement_type_code'] == x) & (i[x] == 'No'), 'entities_rule'] = 'No'
        i.loc[(i['agreement_type_code'] == x) & (i[x] == 'Yes'), 'entities_rule'] = 'Yes'

print(i['entities_rule'].unique())





