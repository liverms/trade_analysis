import pandas as pd


def document_type_code(df_in):
    col = 'document_type_code'
    c_type = ['c', 'C ', 'C']
    for error in c_type:
        df_in[col] = df_in[col].replace(error, 'Contract')

    fix_doc_type = ['A']
    for error in fix_doc_type:
        df_in[col] = df_in[col].replace(error, 'Amendment')

    doc_type = ['Contract', 'Amendment', 'SOSA']
    df_in = df_in[df_in[col].isin(doc_type)]
    return df_in


def original_value(df_in):
    col = 'original_value'
    df_in[col] = df_in[col].str.replace('$', '')
    df_in[col] = df_in[col].str.replace(',', '')
    df_in[col].str.strip()
    df_in[col] = df_in[col].astype(float)
    return df_in


def commodity_type_code(df_in):
    col = 'commodity_type_code'
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
        df_in[col] = df_in[col].str.replace(error, 'Goods')

    #change variations of services to string Services
    fix_services = [
        'S: Service',
        'SERVICES',
        'Service',
        's',
        'S'
    ]
    for error in fix_services:
        df_in[col] = df_in[col].str.replace(error, 'Services')

    # change coding of construction to string Construction
    fix_construction = ['c', 'C']
    for error in fix_construction:
        df_in[col] = df_in[col].str.replace(error, 'Contruction')

    commodity_codes = ['Goods', 'Services', 'Construction']


    if df_in[col].isin(commodity_codes) is True:
        pass
    else:
        services = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'R', 'S', 'T', 'U', 'V', 'W',
                           'X',
                           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'r', 's', 't', 'u', 'v', 'w',
                           'x']
        goods = ['N', 'n', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        construction = ['51']

        unknown_letters = ['I', 'i', 'O', 'o', 'P', 'p', 'Q', 'q', 'Y', 'y', 'Z', 'z', '0']

        df_in.loc[df_in['commodity_code'].isnull(), 'commodity_type_code'] = 'Unknown'

        for k in services:
            df_in.loc[df_in['commodity_code'].str.slice(0, 1) == k, col] = 'Services'
        for k in goods:
            df_in.loc[df_in['commodity_code'].str.slice(0, 1) == k, col] = 'Goods'
        for k in construction:
            df_in.loc[df_in['commodity_code'].str.slice(0, 2) == k, col] = 'Construction'
        for k in unknown_letters:
            df_in.loc[df_in['commodity_code'].str.slice(0, 1) == k, col] = 'Unknown'


    df_in = df_in[df_in[col].isin(commodity_codes)]

    return df_in


def reporting_period(df_in):
    col = 'reporting_period'
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
        df_in[col] = df_in[col].str.replace(error, '2016')

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
        df_in[col] = df_in[col].str.replace(error, '2017')

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
        df_in[col] = df_in[col].str.replace(error, '2018')

    #fix reporting period for 2019
    fix_2019 = [
        '2019-2020-Q1',
        '2019-2020-Q2',
        '2019-2020-Q3',
        '2019-2020-Q4',
        '2019-2020'
    ]
    for error in fix_2019:
        df_in[col] = df_in[col].str.replace(error, '2019')

    years = ['2016', '2017', '2018', '2019']
    df_in = df_in[df_in[col].isin(years)]
    return df_in


def agreement_type_code(df_in, agreement_codes):
    col = 'agreement_type_code'
    pd_codes = {
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

    for key, value in pd_codes.items():
        df_in[col].replace(key, value, inplace=True)

    df_in[col] = df_in[col].str.split('/').tolist()
    df_in = df_in.explode(col)

    df_in = df_in[df_in['agreement_type_code'].isin(agreement_codes)]

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

    df_in['abbreviation'] = df_in['owner_org_title']

    for t, a in abrev.items():
        df_in.loc[df_in['abbreviation'].str.contains(t), 'abbreviation'] = a

    return df_in


def limited_tendering_reason_code(df_in):
    col = 'limited_tendering_reason_code'
    df_in[col].fillna('00', inplace=True)
    df_in[col] = df_in[col].replace('0', '00')
    df_in[col] = df_in[col].replace('5', '05')

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
    df_in = df_in[df_in[col].isin(limited_tendering_reason)]

    return df_in


def commodity_code(df_in, gsin_unspsc_map, df_commodities):
    col = 'commodity_code'
    lookup = dict(zip(gsin_unspsc_map['unspsc_code'], gsin_unspsc_map['gsin']))
    unique_gsin = df_commodities[col].unique().astype(str)
    unique_com = df_in[col].unique().astype(str)

    for key, value in lookup.items():
        df_in[col].replace(key, value, inplace=True)

    compare={}
    for x in unique_com:
        for y in unique_gsin:
            if x == y:
                pass
            elif x.startswith(y):
                compare[x] = y
            else:
                pass

    for key, value in compare.items():
        df_in[col].replace(key, value, inplace=True)

    df_in = df_in[df_in[col].isin(unique_gsin)]

    return df_in


def exemption_code(df_in):
    col = 'exemption_code'
    df_in[col].fillna('00', inplace=True)
    df_in[col] = df_in[col].replace('0', '00')
    df_in[col] = df_in[col].replace('4', '04')
    df_in[col] = df_in[col].replace('3', '03')
    df_in[col] = df_in[col].replace('1', '01')
    df_in[col] = df_in[col].replace('6', '06')

    exemptions = [
        '00',
        '01',
        '02',
        '03',
        '04',
        '05',
        '06'
    ]
    df_in = df_in[df_in[col].isin(exemptions)]

    return df_in


def country_of_origin(df_in):
    col = 'country_of_origin'

    df_in[col] = df_in[col].replace('CAN', 'CA')
    df_in[col] = df_in[col].replace('Canada', 'CA')
    df_in[col] = df_in[col].replace('ca', 'CA')
    df_in[col] = df_in[col].replace('USA', 'US')

    return df_in