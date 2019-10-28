import pandas as pd


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

gsin_trade_map = pd.read_csv('df_commodities.csv',
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
                                            'CUFTA',
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
                                    'CUFTA': str,
                                          'CETA': str,
                                          'CPTPP': str,
                                          'Type': str
                                      }
                             )

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
    'WTO-AGP',
    'CETA',
    'CPTPP'
]

'''
1) Commodity covered, procurement covered = Yes
2) Commodity covered, procurement not covered  = No
3) Commodity not covered, procurement covered = Unknown
4) Commodity not covered, procurement not covered = Yes
'''
df['commodity_rule'] = 'Unknown'

for y in trade_agreements:
    df[y] = df[y].str.upper()

for x in agreement_codes:
    if x == 'CFTA':
        pass
    else:
        if x == '0':
            df.loc[(df['NAFTA'].str.contains('NO')) & (df['CCFTA'].str.contains('NO')) & (df['CCFTA'].str.contains('NO')) & (df['CCoFTA'].str.contains('NO'))
                   & (df['CHFTA'].str.contains('NO')) & (df['CPaFTA'].str.contains('NO')) & (df['CPFTA'].str.contains('NO')) & (df['CKFTA'].str.contains('NO'))
                   & (df['WTO-AGP'].str.contains('NO')) & (df['CETA'].str.contains('NO')) & (df['CPTPP'].str.contains('NO')),
                   'commodity_rule'] = 'Yes'
        else:
            df.loc[(df['agreement_type_code'] == x) & (df[x].str.contains('YES')), 'commodity_rule'] = 'Yes'
            df.loc[(df['agreement_type_code'] == x) & (df[x].str.contains('NO')), 'commodity_rule'] = 'No'


df = df[df['commodity_rule'] == 'No']
print(df)

df.to_csv('commodity.csv')