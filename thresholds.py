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

df = pd.read_csv('df.csv',
                 usecols=usecols,
                 dtype=dtype
)

thresholds = pd.read_csv('thresholds.csv')
thresholds.set_index('Type', inplace=True)


gsin_trade_map = pd.read_csv('gsin_trade_map.csv',
                             usecols=[
                                          'commodity_code',
                                          'NAFTA',
                                          'CCFTA',
                                          'CCoFTA',
                                          'CHFTA',
                                          'CPaFTA',
                                          'CPFTA',
                                          'CKFTA',
                                          'WTO-AGP',
                                          'CETA',
                                          'CPTPP',
                                          'Type'
                                      ],
                             dtype={
                                          'commodity_code': str,
                                          'NAFTA': str,
                                          'CCFTA': str,
                                          'CCoFTA': str,
                                          'CHFTA': str,
                                          'CPaFTA': str,
                                          'CPFTA': str,
                                          'CKFTA': str,
                                          'WTO-AGP': str,
                                          'CETA': str,
                                          'CPTPP': str,
                                          'Type': str
                                      }
                             )
# df['commodity_code'] = df['commodity_code'].astype(str)
# gsin_trade_map['commodity_code'] = gsin_trade_map['commodity_code'].astype(str)
#
#
# df['commodity_code'] = df['commodity_code'].str.strip()
# gsin_trade_map['commodity_code'] = gsin_trade_map['commodity_code'].str.strip()
#
# df.reset_index(inplace=True)
# gsin_trade_map.reset_index(inplace=True)
# print(df['commodity_code'].dtype)
# print(gsin_trade_map['commodity_code'].dtype)

df = df.merge(gsin_trade_map, how='left', left_on='commodity_code', right_on='commodity_code')

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

i['same_com_type'] = 'Error'
i.loc[(i['commodity_type_code'] == i['Type']), 'same_com_type'] = 'Yes'
i.loc[(i['commodity_type_code'] != i['Type']), 'same_com_type'] = 'No'

i = i[i['same_com_type'] == 'No']
df.to_csv('df_thresholds.csv')

print(df)