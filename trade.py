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
    'country_of_origin',
    'amendment_value'
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
    'country_of_origin': str,
    'amendment_value': str
}

df = pd.read_csv('C:/Users/slivermo/desktop/contracts_original.csv',
                 usecols=usecols,
                 dtype=dtype
)

df['uuid'] = [uuid.uuid4() for __ in range(df.index.size)]
df.set_index('uuid', inplace=True)


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


#get rid of empty cells and NA
for col in usecols:
    df[col] = df[col].str.strip()

df = clean.document_type_code(df)
print('doc type below')
print(df)
df.dropna(inplace=True)

df = clean.reporting_period(df)
print('reporting period')
print(df)
df.dropna(inplace=True)

years = ['2019', '2018', '2017']
df = df[df['reporting_period'].isin(years)]
df.dropna(inplace=True)

df=clean.commodity_code(df, gsin_unspsc_map, df_commodities)
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

df = clean.amendment_value(df)
print('amendment val below')
print(df)
df.dropna(inplace=True)

df = clean.commodity_type_code(df)
print('commodity type code below')
print(df)

df = clean.agreement_type_code(df, agreement_codes)
print('agreement type below')
print(df)
df.dropna(inplace=True)

df = clean.exemption_code(df)
print('exemption code')
print(df)

df = clean.country_of_origin(df)
print('clean country')
print(df)

# df = df[df['document_type_code'] == 'Amendment']
# df.to_csv('amendment_before_analysis.csv')
# df = pd.read_csv('amendment_before_analysis.csv')
# ## Analysis
df = rules.entities(df, df_entities, agreement_codes, trade_agreements)
print('entities rule')
print(df)
df.dropna(inplace=True)

df = rules.limited_tendering(df, agreement_codes)
print('limited tendering')
print(df)
df.dropna(inplace=True)

df = rules.thresholds(df, df_thresholds, agreement_codes)
print('thresholds')
print(df)
df.dropna(inplace=True)

df = rules.commodities(df, df_commodities, trade_agreements, agreement_codes)
print('commodities rules')
print(df)
df.dropna(inplace=True)

df = rules.exemption(df, agreement_codes)
print('exemption rules')
print(df)

df.to_csv('test.csv')
# df = pd.read_csv('test.csv')
df['coverage_applied'] = 'Unknown'

df.loc[(df['entities_rule'] == 'Yes') | (df['thresholds'] == 'Yes') | (df['commodity_rule'] == 'Yes') | (df['lt_rule'] == 'Yes') | (df['ex_rule'] == 'Yes'), 'coverage_applied'] = 'Yes'
df.loc[(df['entities_rule'] == 'No') | (df['thresholds'] == 'No') | (df['commodity_rule'] == 'No') | (df['lt_rule'] == 'No') | (df['ex_rule'] == 'No'), 'coverage_applied'] = 'No'

print(df)
i = df.copy(deep=True)
df = df.groupby('uuid')['coverage_applied'].apply(','.join)
df = pd.DataFrame(df)
print(df)

df.loc[(df['coverage_applied'].str.contains('No')), 'coverage_applied'] = 'No'
df.loc[(df['coverage_applied'].str.contains('Yes')), 'coverage_applied'] = 'Yes'
print(i)
i.drop('agreement_type_code', axis=1, inplace=True)
i = i[~i.index.duplicated()]
# i.set_index('uuid', inplace=True)



df = df.merge(i, how='inner', on='uuid', copy=False)
print(df)
code_lookup = pd.read_csv('commodity_code_lookup.csv',
                      usecols=[
                          'commodity_code',
                          'gsin_description_en'
                      ]
                          )

df = df.merge(code_lookup, how='left', on='commodity_code', copy=False)

df = df[df['coverage_applied_y'] == 'No']
df.drop('copy_index', axis=1, inplace=True)
df.drop('same_com_type', axis=1, inplace=True)
df.drop('commodity_code', axis=1, inplace=True)
df.drop('coverage_applied_x', axis=1, inplace=True)
df.drop('document_type_code', axis=1, inplace=True)
df.drop('procurement_id', axis=1, inplace=True)
df.drop('Federal Entity', axis=1, inplace=True)
df.drop('owner_org_title', axis=1, inplace=True)
# df.drop('Unnamed_0', axis=1, inplace=True)
# df.drop('coverage_applied_y', axis =1, inplace=True)
df.drop('Type', axis=1, inplace=True)
df = df.rename(
    columns={
        'abbreviation': 'Entity',
        'agreement_type_code': 'Trade Agreement Code',
        'gsin_description_en': 'Commodity',
        'commodity_rule': 'Commodity Rule',
        'commodity_type_code': 'Commodity Type',
        'country_of_origin': 'Country of Origin',
        'entities_rule': 'Entities Rule',
        'ex_rule': 'Exemptions Rule',
        'exemption_code': 'Exemption',
        'limited_tendering_reason_code': 'Limited Tendering Reason',
        'lt_rule': 'Limited Tendering Rule',
        'original_value': 'Original Value',
        'reporting_period': 'Year',
        'amendment_value': 'Amendment Value',
        'coverage_applied_y': 'Estimated Trade Coverage'
    }
)



df.to_csv('contracts_no.csv')

