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
            # i.loc[((i['agreement_type_code'] == x) & (i['commodity_type_code'] == c) & (i['original_value'] >= dollar)), 'thresholds'] = 'Unknown'
            # i.loc[((i['agreement_type_code'] == x) & (i['commodity_type_code'] == c) & (i['original_value'] < dollar)), 'thresholds'] = 'Yes'
        else:
            dollar = thresholds.loc[c].at[x]
            print(dollar)
            # i.loc[((i['agreement_type_code'] == x) & (i['commodity_type_code'] == c) & (i['original_value'] >= thresholds)), 'thresholds'] = 'Yes'
            # i.loc[((i['agreement_type_code'] == x) & (i['commodity_type_code'] == c) & (i['original_value'] < thresholds)), 'thresholds'] = 'No'



i.to_csv('C:/Users/danli/documents/github/trade_analysis/df_thresholds.csv')
        # i = i.loc[i[x] == 'Yes']
        # i = i.reset_index()
        # i = i[usecols]
        #
        # i = i[i['limited_tendering_reason_code'] == '00']
        # print(i)
        # commodities = ['Goods', 'Services', 'Construction']
        # for com in commodities:
        #         dollar = thresholds[x].at[com]
        #         i = i[(i['commodity_type_code'] == com) & (i['original_value'] >= dollar)]

    # for com in commodities:
    #     if x == '0':
    #         pass
    #     else:
    #         dollar = thresholds.loc['CFTA']
    #         # val = val[(val['commodity_type_code'] == com)]
    #         print(dollar)
 # & (i['original_value'] >= dollar)
 # & (val['original_value'] > thresholds.loc[x].at[1])
#
# for item in df_list:
#     item = item[item['limited_tendering_reason_code'] != '00']
#     item = item.reset_index()
#     item.drop('index', axis=1, inplace=True)
#     if item == cfta:
#         item = item[(item['commodity_type_code'] == 'Goods') & (item['original_value'] > 25300)]
#         item = item[(item['commodity_type_code'] == 'Services') & (item['original_value'] > 101100)]
#         item = item[(item['commodity_type_code'] == 'Construction') & (item['original_value'] > 101100)]
#     print(item)


#
#
#
#
# none = none[none['limited_tendering_reason_code'] == '00']
# none = none.loc[(none['commodity_type_code'] == 'Goods') & (none['original_value'] > 25300)]
#
#
# print(none)
# none.to_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/none.csv')
# ccfta.to_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/ccfta.csv')