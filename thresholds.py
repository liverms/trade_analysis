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
    'CPTPP',
    '0'
]

for x in trade:
    if x == '0':
        val = df
    else:
        val = df[df[x] == 'Yes']

    val = val.reset_index()
    val = val[usecols]

    val = val[val['limited_tendering_reason_code'] != '00']


    commodities = ['Goods', 'Services', 'Construction']
    for com in commodities:
        if x == '0':
            check = val

        else:
            dollar = thresholds[x].at[com]


    # for com in commodities:
    #     if x == '0':
    #         pass
    #     else:
    #         dollar = thresholds.loc['CFTA']
    #         # val = val[(val['commodity_type_code'] == com)]
    #         print(dollar)

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