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
    'CPTPP'
]
'''
This loop searches for entities which are not covered by the agreement, the No
filter the agreement type so that we have one df for each trade agreement and the procurements are only for that one.
'''

df['entities_misapplied'] = ['Y' if val[x] == 'No']
# dict_df = {}
# for x in trade_agreements:
#     val = df[df['agreement_type_code'] == x]
#     # there is no zero in the columnts of df, but there is one in the trade list, this skips in error
#     if x == '0':
#         pass
#     else:
#         val = df[df['agreement_type_code'] == x]
#         if (val[x] == 'No') is True:
#             val = val[val[x] == 'No']
#             val['entities_misapplied'] = 'Y'
#         else:
#             val = val[val[x] == 'Yes']
#             val['entities_misapplied'] = 'N'
#
#
#         val = val.reset_index()
#         val = val[usecols]
#         dict_df[x] = [val]
#         print(dict_df[x])
#
# val['entities_misapplied'] = val[val['']]
print(dff)

dff.to_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/misapply.csv')






