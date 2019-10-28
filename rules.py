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
    'limited_tendering_reason_code',
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
    'limited_tendering_reason_code': str,
    'abbreviation': str
}

df = pd.read_csv('df.csv',
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


def entities(df_in, df_entities):
    '''
    There are 3 possible outcomes:
    1) Procurement not covered by a TA by an entity not covered ('Yes')
    2) Procurement not covered by a TA by an entity that is covered (default = 'Unknown')
    3) Procurement covered by a TA by an entity not covered ('No')
    4) Procurement covered by a TA by an entity covered ('Yes')
    '''

    df_in = df_in.merge(df_entities, how='left', left_on='abbreviation', right_on='Abbreviation')
    df_in['entities_rule'] = 'Unknown'

    for y in agreement_codes:
        if y == '0':
            df_in.loc[(df_in['entities_rule'] == 'Unknown') & (df_in['CCFTA'] == 'No') & (df_in['CCoFTA'] == 'No')
                  & (df_in['CHFTA'] == 'No') & (df_in['CPaFTA'] == 'No') & (df_in['CPFTA'] == 'No')
                  & (df_in['CKFTA'] == 'No') & (df_in['CUFTA'] == 'No') & (df_in['WTO-AGP'] == 'No'), 'entities_rule'] = 'Yes'
        elif y == 'CFTA':
            pass
        else:
            df_in.loc[(df_in['entities_rule'] == 'Unknown') & (df_in['agreement_type_code'] == y) &
                  (df_in[y] == 'Yes'), 'entities_rule'] = 'Yes'
            df_in.loc[(df_in['agreement_type_code'] == y) & (df_in[y] == 'No'), 'entities_rule'] = 'No'


    for z in trade_agreements:
        df_in.drop(z, axis=1, inplace=True)
    return df_in


def limited_tendering(df_in):
    limited_tendering_reason = [
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
    df_in = df_in[df_in['limited_tendering_reason_code'].isin(limited_tendering_reason)]
    df_in['lt_rule'] = 'Unknown'

    '''
    1) Procurement not covered, limited tendering not invoked = 'Yes'
    2) Procurement not covered, limited tendering invoked = 'no_it_yes_lt' (default)
    3) Procurement covered, limited tendering invoked = 'yes_it_yes_ly'
    4) Procurement covered, limited tendering not invoked = 'it_no_lt'
    '''
    df_in = df
    for x in agreement_codes:
        if x == '0':
            df_in.loc[((df_in['agreement_type_code'] == x) & (df_in['limited_tendering_reason_code'] == '00')), 'lt_rule'] = 'Yes'
            df_in.loc[((df_in['agreement_type_code'] == x) & (
                        df_in['limited_tendering_reason_code'] != '00')), 'lt_rule'] = 'no_it_lt'
        else:
            df_in.loc[((df_in['agreement_type_code'] == x) & (df_in['limited_tendering_reason_code'] != '00')), 'lt_rule'] = 'it_ly'
            df_in.loc[((df_in['agreement_type_code'] == x) & (df_in['limited_tendering_reason_code'] == '00')), 'lt_rule'] = 'Yes'

    return df_in


def thresholds(df_in, df_thresholds):
    '''
    1) Procurement is not covered, value is above thresholds 'Unknown'
    2) Procurement is not covered, value is below thresholds 'Yes'
    3) Procurement is covered, value is above thresholds 'Yes'
    4) Procurement is covered, value is below thresholds 'No'
    '''
    df_in['thresholds'] = 'Unknown'
    commodities = ['Goods', 'Services', 'Construction']

    for x in agreement_codes:
        for c in commodities:
            if x == '0':
                dollar = df_thresholds.loc[c].at['CFTA']
                df_in.loc[((df_in['original_value'] > dollar) & (df_in['agreement_type_code'] == x) & (
                            df_in['commodity_type_code'] == c)), 'thresholds'] = 'Unknown'
                df_in.loc[((df_in['original_value'] < dollar) & (df_in['agreement_type_code'] == x) & (
                            df_in['commodity_type_code'] == c)), 'thresholds'] = 'Yes'
            else:
                dollar = df_thresholds.loc[c].at[x]
                df_in.loc[((df_in['original_value'] > dollar) & (df_in['agreement_type_code'] == x) & (
                            df_in['commodity_type_code'] == c)), 'thresholds'] = 'Yes'
                df_in.loc[((df_in['original_value'] < dollar) & (df_in['agreement_type_code'] == x) & (
                            df_in['commodity_type_code'] == c)), 'thresholds'] = 'No'

    return df_in


def commodities(df_in, df_commodities):
    '''
    1) Commodity covered, procurement covered = Yes
    2) Commodity covered, procurement not covered  = No
    3) Commodity not covered, procurement covered = Unknown
    4) Commodity not covered, procurement not covered = Yes
    '''
    df_in = df_in.merge(df_commodities, how='left', left_on='commodity_code', right_on='commodity_code')
    df_in['same_com_type'] = 'Error'
    df_in.loc[(df_in['commodity_type_code'] == df_in['Type']), 'same_com_type'] = 'Yes'
    df_in.loc[(df_in['commodity_type_code'] != df_in['Type']), 'same_com_type'] = 'No'

    df_in['commodity_rule'] = 'Unknown'

    for y in trade_agreements:
        df_in[y] = df_in[y].str.upper()

    for x in agreement_codes:
        if x == 'CFTA':
            pass
        else:
            if x == '0':
                df_in.loc[(df_in['NAFTA'].str.contains('NO')) & (df_in['CCFTA'].str.contains('NO')) & (
                    df_in['CCFTA'].str.contains('NO')) & (df_in['CCoFTA'].str.contains('NO'))
                       & (df_in['CHFTA'].str.contains('NO')) & (df_in['CPaFTA'].str.contains('NO')) & (
                           df_in['CPFTA'].str.contains('NO')) & (df_in['CKFTA'].str.contains('NO'))
                       & (df_in['WTO-AGP'].str.contains('NO')) & (df_in['CETA'].str.contains('NO')) & (
                           df_in['CPTPP'].str.contains('NO')),
                       'commodity_rule'] = 'Yes'
            else:
                df_in.loc[(df_in['agreement_type_code'] == x) & (df_in[x].str.contains('YES')), 'commodity_rule'] = 'Yes'
                df_in.loc[(df_in['agreement_type_code'] == x) & (df_in[x].str.contains('NO')), 'commodity_rule'] = 'No'

    for z in trade_agreements:
        df_in.drop(z, axis=1, inplace=True)
    return df_in

