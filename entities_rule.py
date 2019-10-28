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

df = pd.read_csv('df.csv',
                 usecols=usecols,
                 dtype=dtype
)

ent = pd.read_csv('df_entities.csv')

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
'''
There are 3 possible outcomes:
1) Procurement not covered by a TA by an entity not covered ('Yes')
2) Procurement not covered by a TA by an entity that is covered (default = 'Unknown')
3) Procurement covered by a TA by an entity not covered ('No')
4) Procurement covered by a TA by an entity covered ('Yes')

'''

df = df[df['agreement_type_code'].isin(agreement_codes)]
df['entities_rule'] = 'Unknown'

i = df
for y in agreement_codes:
    if y == '0':
        i.loc[(i['entities_rule'] == 'Unknown') & (i['CCFTA'] == 'No') & (i['CCoFTA'] == 'No')
        & (i['CHFTA'] == 'No') & (i['CPaFTA'] == 'No') & (i['CPFTA'] == 'No')
        & (i['CKFTA'] == 'No') & (i['CUFTA'] == 'No') & (i['WTO-AGP'] == 'No'), 'entities_rule'] = 'Yes'
    elif y == 'CFTA':
        pass
    else:
        i.loc[(i['entities_rule'] == 'Unknown') & (i['agreement_type_code'] == y) &
              (i[y] == 'Yes'), 'entities_rule'] = 'Yes'
        i.loc[(i['agreement_type_code'] == y) & (i[y] == 'No'), 'entities_rule'] = 'No'

i = i[i['entities_rule'] == 'No']

i.to_csv('entities_rule.csv')



