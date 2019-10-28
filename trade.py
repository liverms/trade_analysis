import pandas as pd
import clean
import rules

usecols=[
    'original_value',
    'commodity_type_code',
    'commodity_code',
    'reporting_period',
    'owner_org_title',
    'document_type_code',
    'agreement_type_code',
    'procurement_id',
    'limited_tendering_reason_code'
]
#data types of columns
dtype={
    'commodity_type_code': str,
    'commodity_code': str,
    'original_value': str,
    'reporting_period': str,
    'owner_org_title': str,
    'document_type_code':str,
    'agreement_type_code': str,
    'procurement_id': str,
    'limited_tendering_reason_code': str
}

df = pd.read_csv('C:/Users/slivermo/desktop/contracts_original.csv',
                 usecols=usecols,
                 dtype=dtype
)

df_entities = pd.read_csv('df_entities.csv')

df_thresholds = pd.read_csv('thresholds.csv')
df_thresholds.set_index('Type', inplace=True)

df_commodities = pd.read_csv('df_commodities.csv',
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

df = clean.reporting_period(df)
print('reporting period')
print(df)
df.dropna(inplace=True)

years = ['2019', '2018', '2017']
df = df[df['reporting_period'].isin(years)]
df.dropna(inplace=True)

df=clean.commodity_code(df)
print('commodity_code below')
print(df)
df.dropna(inplace=True)

df = clean.limited_tendering_reason_code(df)
print('limited tendering below')
print(df)
df.dropna(inplace=True)

df = clean.owner_abrev(df)
print('owner_abrev')
print(df)
df.dropna(inplace=True)

df = clean.original_value(df)
print('original val below')
print(df)
df.dropna(inplace=True)

df = clean.commodity_type_code(df)
print('commodity type code below')
print(df)

df = clean.document_type_code(df)
print('doc type below')
print(df)
df.dropna(inplace=True)

df = clean.agreement_type_code(df)
print('agreement type below')
print(df)
df.dropna(inplace=True)

agreement = ['Contract']
df = df[df['agreement_type_code'].isin(agreement)]
## Analysis
df = rules.entities(df, df_entities)
print('entities rule')
print(df)
df.dropna(inplace=True)

df = rules.limited_tendering(df)
print('limited tendering')
print(df)
df.dropna(inplace=True)

df = rules.thresholds(df, df_thresholds)
print('thresholds')
print(df)
df.dropna(inplace=True)

df = rules.commodities(df, df_commodities)
print('commodities rules')
print(df)
df.dropna(inplace=True)

print(df)
df.to_csv('df.csv')