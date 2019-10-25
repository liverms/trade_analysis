import pandas as pd
import numpy as np

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
    'original_value': object,
    'reporting_period': str,
    'owner_org_title': str,
    'document_type_code':str,
    'agreement_type_code': str,
    'procurement_id': str,
    'limited_tendering_reason_code': str
}
#read in csv
df = pd.read_csv(
    'C:/Users/slivermo/Desktop/contracts_original.csv',
    usecols=usecols,
    dtype=dtype
)

#get rid of empty cells and NA
for col in usecols:
    df[col] = df[col].str.strip()

def document_type_code(df_in):
    fix_doc_type = ['c', 'C ', 'C']
    for error in fix_doc_type:
        df_in['document_type_code'] = df_in['document_type_code'].str.replace(error, 'Contract')

    fix_doc_type = ['A']
    for error in fix_doc_type:
        df_in['document_type_code'] = df_in['document_type_code'].str.replace(error, 'Amendment')

    return df_in


def original_value(df_in):
    df_in['original_value'] = df_in['original_value'].str.replace('$', '')
    df_in['original_value'] = df_in['original_value'].str.replace(',', '')
    df_in['original_value'].str.strip()
    df_in['original_value'].astype(float)

    return df_in


def commodity_type_code(df_in):
    # Change coding for Goods to string Goods
    fix_goods = [
        'g',
        'GOODS',
        'G: Goods',
        'Good',
        'Goods',
        'G'
    ]
    for error in fix_goods:
        df_in['commodity_type_code'] = df_in['commodity_type_code'].str.replace(error, 'Goods')

    #change variations of services to string Services
    fix_services = [
        'S: Service',
        'SERVICES',
        'Service',
        's',
        'S'
    ]
    for error in fix_services:
        df_in['commodity_type_code'] = df_in['commodity_type_code'].str.replace(error, 'Services')

    # change coding of construction to string Construction
    fix_construction = ['c', 'C']
    for error in fix_construction:
        df_in['commodity_type_code'] = df_in['commodity_type_code'].str.replace(error, 'Contruction')

    commodity_codes = ['Goods', 'Services', 'Construction']
    if df['commodity_type_code'].isin(commodity_codes) is True:
        pass
    else:
        service_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'r', 's', 't', 'u', 'v', 'w', 'x']
        goods_letters = ['N', 'n', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        unknown_letters = ['I', 'i', 'O', 'o', 'P', 'p', 'Q', 'q', 'Y', 'y', 'Z', 'z', '0']

        df_in.loc[df_in['commodity_code'].isnull(), 'commodity_type_code'] = 'Unknown'

        for letter in service_letters:
            df_in.loc[df_in['commodity_code'].str.slice(0, 1) == letter, 'commodity_type_code'] = 'Services'
        for letter in goods_letters:
            df_in.loc[df_in['commodity_code'].str.slice(0, 1) == letter, 'commodity_type_code'] = 'Goods'
        for letter in unknown_letters:
            df_in.loc[df_in['commodity_code'].str.slice(0, 1) == letter, 'commodity_type_code'] = 'Unknown'
    return df_in


def reporting_period(df_in):


    #fix reporting period of 2016
    fix_2016 = [
        '2016-2017-Q1',
        '2016-2017-Q2',
        '2016-2017-Q3',
        '2016-2017-Q4',
        '2016-2017 Q4',
        '2016-2017- Q2',
        'C-2016-2017',
        '2016-2017- Q4',
        '2016-2017-Q5',
        '2016-2017',
        'C-2016'
    ]
    for error in fix_2016:
        df_in['reporting_period'] = df_in['reporting_period'].str.replace(error, '2016')

    #fix reporting period for 2017
    fix_2017 = [
        '2017-2018-Q1',
        '2017-2018-Q2',
        '2017-2018-Q3',
        '2017-2018-Q4',
        '2017-2018 Q1',
        '2017-2018 Q2',
        '2017-2018 Q3',
        '2017-2018 Q4',
        '2017-2018 Q6',
        '2017-2018 Q7',
        '2017-2018 Q8',
        '2017-2018-Q6',
        '2017-2018-Q7',
        '2017-2018-Q8',
        '2017-2018'
    ]
    for error in fix_2017:
        df_in['reporting_period'] = df_in['reporting_period'].str.replace(error, '2017')

    #fix reporting period 2018
    fix_2018 = [
        '2018-2019-Q1',
        '2018-2019-Q2',
        '2018-2019-Q3',
        '2018-2019-Q4',
        '2018-2019 Q1',
        '2018-2019-Q4',
        '2018-2019-Q5',
        '2018-2019-Q7',
        '2018-19-Q3',
        '2018-2019'
    ]
    for error in fix_2018:
        df_in['reporting_period'] = df_in['reporting_period'].str.replace(error, '2018')

    #fix reporting period for 2019
    fix_2019 = [
        '2019-2020-Q1',
        '2019-2020-Q2',
        '2019-2020-Q3',
        '2019-2020-Q4',
        '2019-2020'
    ]
    for error in fix_2019:
        df_in['reporting_period'] = df_in['reporting_period'].str.replace(error, '2019')

    return df_in


def agreement_type_code(df_in):
    agreement_codes = {
        'Y': 'WTO-AGP/NAFTA/CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CPFTA/CKFTA',
        'X': 'WTO-AGP/CFTA/CCFTA/CKFTA',
        'C': 'NAFTA/CFTA',
        'W': 'WTO-AGP/CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CPFTA/CKFTA',
        'I': 'CFTA',
        'S': 'NAFTA/CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CKFTA',
        'T': 'NAFTA/CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CPFTA/CKFTA',
        'V': 'CFTA/CCFTA/CKFTA',
        'D': 'CETA/CFTA',
        'E': 'CETA/WTO-AGP/CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CPFTA/CKFTA',
        'F': 'CETA/WTO-AGP/NAFTA/CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CPFTA/CKFTA',
        'AB': 'CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CKFTA',
        'AC': 'CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CPFTA/CKFTA',
        'AD': 'CETA/WTO-AGP/CFTA/CCFTA/CKFTA',
        'AF': 'CFTA/CHFTA',
        'AG': 'CETA/CFTA/CHFTA',
        'AH': 'CKFTA',
        'AI': 'CFTA/CKFTA',
        'AJ': 'CFTA/NAFTA/CKFTA',
        'AK': 'CPTPP',
        'AL': 'CFTA/CPTPP',
        'AM': 'CFTA/CETA/CPTPP',
        'AN': 'CFTA/CHFTA/CETA/CPTPP',
        'AO': 'CFTA/CCFTA/CKFTA/WTO-AGP/CPTPP',
        'AP': 'CFTA/NAFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CPFTA/CKFTA/WTO-AGP/CETA/CPTPP',
        'AQ': 'CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CPFTA/CKFTA/WTO-AGP/CETA/CPTPP',
        'AR': 'CFTA/NAFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/ CPFTA/CKFTA/WTO-AGP/CPTPP',
        'AS': 'CFTA/CCFTA/CCoFTA/CHFTA/CPaFTA/CPFTA/CKFTA/WTO-AGP/CPTPP',
        'AT': 'CFTA/CCFTA/CKFTA',
        'AV': 'CFTA/CCFTA',
        'AW': 'CFTA/CCFTA/CPTPP',
        'AX': 'CFTA/CKFTA/WTO-AGP/CETA',
        'AY': 'CFTA/CKFTA/WTO-AGP/CETA/CPTPP',
        'AZ': 'CFTA/CKFTA/WTO-AGP/CPTPP'
    }

    for key, value in agreement_codes.items():
        df_in['agreement_type_code'].replace(key, value, inplace=True)

    df_in['agreement_type_code'] = df_in['agreement_type_code'].str.split('/').tolist()
    df_in = df_in.explode('agreement_type_code')
    return df_in



def owner_abrev(df_in):
    abrev = {
        'Agriculture and Agri-Food Canada': 'AAFC',
        'Crown-Indigenous Relations and Northern Affairs Canada': 'INAC',
        'Atlantic Canada Opportunities Agency': 'ACOA',
        'Administrative Tribunals Support Service of Canada': 'ATSSC',
        'Canadian Northern Economic Development Agency': 'CanNor',
        'Courts Administration Service': 'CAS',
        'Canada Border Services Agency': 'CBSA',
        'Canadian Centre for Occupational Health and Safety': 'CCOHS',
        'Canada Economic Development for Quebec Regions': 'CED',
        'Canada Energy Regulator': 'CER',
        'Canadian Food Inspection Agency': 'CFIA',
        'Canadian Grain Commission': 'CGC',
        'Canadian Human Rights Commission': 'CHRC',
        'Immigration, Refugees and Citizenship Canada': 'IRCC',
        'Canadian Intergovernmental Conference Secretariat': 'CICS',
        'Canadian Institutes of Health Research': 'CIHR',
        'Canadian Nuclear Safety Commission': 'CNSC',
        'Civilian Review and Complaints Commission for the RCMP': 'CRCC',
        'Canada Revenue Agency': 'CRA',
        'Canadian Radio-television and Telecommunications Commission': 'CRTC',
        'Canadian Space Agency': 'CSA',
        'Correctional Service of Canada': 'CSC',
        'Canada School of Public Service': 'CSPS',
        'Canadian Transportation Agency': 'CTA',
        'Global Affairs Canada': 'GAC',
        'Fisheries and Oceans Canada': 'DFO',
        'National Defence': 'DND',
        'Environment and Climate Change Canada': 'ECCC',
        'Elections Canada': 'CEO',
        'Employment and Social Development Canada': 'ESDC',
        'Financial Consumer Agency of Canada': 'FCAC',
        'Federal Economic Development Agency for Southern Ontario': 'FedDev Ontario',
        'Department of Finance Canada': 'FIN',
        'Financial Transactions and Reports Analysis Centre of Canada': 'FINTRAC',
        'Office of the Commissioner for Federal Judicial Affairs Canada': 'FJA',
        'Farm Products Council of Canada': 'FPCC',
        'Health Canada': 'HC',
        'Impact Assessment Agency of Canada': 'none',
        'Innovation, Science and Economic Development Canada': 'ISED',
        'International Joint Commission': 'none',
        'Infrastructure Canada': 'INFC',
        'Immigration and Refugee Board of Canada': 'IRB',
        'Indigenous Services Canada': 'ISC',
        'Department of Justice Canada': 'JUS',
        'Library and Archives Canada': 'LAC',
        'Military Grievances External Review Committee': 'MGERC',
        'Military Police Complaints Commission of Canada': 'MPCC',
        'National Film Board': 'NFB',
        'Natural Resources Canada': 'NRCan',
        'National Research Council Canada': 'NRC',
        'Natural Sciences and Engineering Research Council of Canada': 'NSERC',
        'Office of the Auditor General of Canada': 'OAG',
        'The Correctional Investigator Canada': 'OCI',
        'Office of the Commissioner of Lobbying of Canada': 'OCL',
        'Office of the Commissioner of Official Languages': 'OCOL',
        'Office of the Information Commissioner of Canada': 'OIC',
        'Office of the Privacy Commissioner of Canada': 'OPC',
        'Office of the Superintendent of Financial Institutions Canada': 'OSFI',
        'Office of the Secretary to the Governor General': 'OSGG',
        'Office of the Taxpayers': 'none',
        'Parole Board of Canada': 'PBC',
        'Parks Canada': 'PC',
        'Canadian Heritage': 'PCH',
        'Privy Council Office': 'PCO',
        'Public Health Agency of Canada': 'PHAC',
        'Patented Medicine Prices Review Board Canada': 'PMPRB',
        'Public Prosecution Service of Canada': 'PPSC',
        'Passport Canada': 'none',
        'Public Service Commission of Canada': 'PSC',
        'Office of the Public Sector Integrity Commissioner of Canada': 'PSIC',
        'Public Safety Canada': 'PS',
        'Public Services and Procurement Canada': 'PSPC',
        'Royal Canadian Mounted Police': 'RCMP',
        'Security Intelligence Review Committee': 'SIRC',
        'Shared Services Canada': 'SSC',
        'Social Sciences and Humanities Research Council of Canada': 'SSHRC',
        'Statistics Canada': 'StatCan',
        'Status of Women Canada': 'SWC',
        'Treasury Board of Canada Secretariat': 'TBS',
        'Transport Canada': 'TC',
        'Transportation Safety Board of Canada': 'TSB',
        'Veterans Affairs Canada': 'VAC',
        'Veterans Review and Appeal Board': 'VRAB',
        'Department for Women and Gender Equality': 'SWC',
        'Western Economic Diversification Canada': 'WD',
    }

    df['abbreviation'] = df['owner_org_title']

    for t, a in abrev.items():
        df_in.loc[df_in['abbreviation'].str.contains(t), 'abbreviation'] = a

    return df_in


def limited_tendering_reason_code(df_in):
    df_in['limited_tendering_reason_code'].fillna('00', inplace=True)
    df_in['limited_tendering_reason_code'] = df_in['limited_tendering_reason_code'].replace('0', '00')
    df_in['limited_tendering_reason_code'] = df_in['limited_tendering_reason_code'].replace('5', '05')


    return df_in

ent = pd.read_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/entities_list.csv')

df = reporting_period(df)

years = ['2019', '2018', '2017']
df = df[df['reporting_period'].isin(years)]

df = limited_tendering_reason_code(df)
df = owner_abrev(df)
df = original_value(df)
df = commodity_type_code(df)
df = document_type_code(df)
df = agreement_type_code(df)


# df = df[df['commodity_type_code'] != 'Goods']
# df = df[df['commodity_type_code'] != 'Services']
# df = df[df['commodity_type_code'] != 'Construction']


print(df)
# pd.DataFrame(df_un).to_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/un.csv')

ent.to_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/ent.csv')
df.to_csv('C:/Users/slivermo/PycharmProjects/trade_analysis/df.csv')
