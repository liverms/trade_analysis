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

df = pd.read_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/df.csv',
                 usecols=usecols,
                 dtype=dtype
)

ent = pd.read_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/entities_list.csv')
thresholds = pd.read_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/thresholds.csv')
thresholds.set_index('Type', inplace=True)
thresholds.to_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/thresholds.csv')
df = df.merge(ent, how='outer', left_on='abbreviation', right_on='Abbreviation')


trade = [
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
1) For each trade agreement: take those rows where the entity is covered
2) Only take rows where the limited tendering reason is None
3) For each commodity and for each trade agreement compare value of the contract
'''

for x in trade:
    i = df[df[x] == 'Yes']
    i = i.reset_index()
    i = i[usecols]

    i = i[i['limited_tendering_reason_code'] == '00']

    commodities = ['Goods', 'Services', 'Construction']
    for com in commodities:
            dollar = thresholds[x].at[com]
            i = i[(i['commodity_type_code'] == com) & (i['original_value'] >= dollar)]
            print(x)
            print(com)
            print(dollar)
            print(i)
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