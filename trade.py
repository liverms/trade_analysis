import pandas as pd
import clean
import rules
import uuid

usecols=[
    'original_value',
    'commodity_type_code',
    'commodity_code',
    'reporting_period',
    'owner_org_title',
    'document_type_code',
    'agreement_type_code',
    'procurement_id',
    'limited_tendering_reason_code',
    'exemption_code',
    'country_of_origin'
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
    'limited_tendering_reason_code': str,
    'exemption_code': str,
    'country_of_origin': str
}

df = pd.read_csv('C:/Users/slivermo/desktop/contracts_original.csv',
                 usecols=usecols,
                 dtype=dtype
)

df['uuid'] = [uuid.uuid4() for __ in range(df.index.size)]
df.set_index('uuid', inplace=True)

df_copy = df
df_entities = pd.read_csv('df_entities.csv')

df_thresholds = pd.read_csv('df_thresholds.csv',
                            dtype={
                                'NAFTA': int,
                                'CCFTA': int,
                                'CCoFTA': int,
                                'CHFTA': int,
                                'CPaFTA': int,
                                'CPFTA': int,
                                'CKFTA': int,
                                'WTO-AGP': int,
                                'CUFTA': int,
                                'CETA': int,
                                'CPTPP': int,
                            })
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

gsin_unspsc_map = pd.read_csv('gsin_unspsc_map.csv',
                              usecols=[
                                     'gsin',
                                     'unspsc_code'
                                 ],
                              dtype={
                                    'gsin': str,
                                    'unspsc_code': str
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


# #get rid of empty cells and NA
# for col in usecols:
#     df[col] = df[col].str.strip()
#
# df = clean.document_type_code(df)
# print('doc type below')
# print(df)
# df.dropna(inplace=True)
#
# df = df[df['document_type_code'] == 'Contract']
#
# df = clean.reporting_period(df)
# print('reporting period')
# print(df)
# df.dropna(inplace=True)
#
# years = ['2019', '2018', '2017']
# df = df[df['reporting_period'].isin(years)]
# df.dropna(inplace=True)
#
# df=clean.commodity_code(df, gsin_unspsc_map, df_commodities)
# print('commodity_code below')
# print(df)
# df.dropna(inplace=True)
#
# df = clean.limited_tendering_reason_code(df)
# print('limited tendering below')
# print(df)
# df.dropna(inplace=True)
#
# df = clean.owner_abrev(df)
# print('owner_abrev')
# print(df)
# df.dropna(inplace=True)
#
# df = clean.original_value(df)
# print('original val below')
# print(df)
# df.dropna(inplace=True)
#
# df = clean.commodity_type_code(df)
# print('commodity type code below')
# print(df)
#
# df = clean.agreement_type_code(df, agreement_codes)
# print('agreement type below')
# print(df)
# df.dropna(inplace=True)
#
# df = clean.exemption_code(df)
# print('exemption code')
# print(df)
#
# df = clean.country_of_origin(df)
# print('clean country')
# print(df)
#
# # ## Analysis
# df = rules.entities(df, df_entities, agreement_codes, trade_agreements)
# print('entities rule')
# print(df)
# df.dropna(inplace=True)
#
# df = rules.limited_tendering(df, agreement_codes)
# print('limited tendering')
# print(df)
# df.dropna(inplace=True)
#
# df = rules.thresholds(df, df_thresholds, agreement_codes)
# print('thresholds')
# print(df)
# df.dropna(inplace=True)
#
# df = rules.commodities(df, df_commodities, trade_agreements, agreement_codes)
# print('commodities rules')
# print(df)
# df.dropna(inplace=True)
#
# df = rules.exemption(df, agreement_codes)
# print('exemption rules')
# print(df)

df = pd.read_csv('test.csv')

df['coverage_applied'] = 'Unknown'

df.loc[(df['entities_rule'] != 'No') & (df['thresholds'] != 'No') & (df['commodity_rule'] != 'No') & (df['lt_rule'] != 'No') & (df['ex_rule'] != 'No'), 'coverage_applied'] = 'Yes'
df.loc[(df['entities_rule'] == 'No') | (df['thresholds'] == 'No') | (df['commodity_rule'] == 'No') | (df['lt_rule'] == 'No') | (df['ex_rule'] == 'No'), 'coverage_applied'] = 'No'

df.to_csv('step.csv')


df = df.groupby('uuid')['coverage_applied'].apply(','.join)
df = pd.DataFrame(df)

df.loc[(df['coverage_applied'].str.contains('No')), 'coverage_applied'] = 'No'
df.loc[(df['coverage_applied'].str.contains('Yes')), 'coverage_applied'] = 'Yes'

df = df.merge(df_copy, left_index=True, right_index=True, how='left')

print(df)
df.to_csv('analyzed.csv')