import pandas as pd
import csv

years = range(2009, 2018)

output = pd.DataFrame()

district_fips = pd.read_csv('https://raw.githubusercontent.com/CT-Data-Collaborative/ct-school-district-list/master/ct-school-district-list-with-fips.csv', dtype=str)

for y in years:
    year = str(y) + '-' + str(y+1)

    for ext in ['.csv', '-ct.csv']:
        df = pd.read_csv('raw/python_raw/SuspensionRates-' + year + ext, usecols=['District', 'Special Education Status', 'Count', '%'])
        df['District'] = df['District'].apply(lambda x: 'Connecticut' if x == 'State' else x)
        df['Year'] = year
        df['Variable'] = 'Suspensions'
        df['Measure Type'] = 'Percent'
        df['FIPS'] = df['District'].apply(lambda x: district_fips[district_fips.District == x].FIPS.item())
        df['Value'] = df['%'].apply(lambda x: "-9999" if x == '*' else x).fillna("-6666")

        output = output.append(df)

output.sort_values(['District', 'Year']).to_csv('data/suspension_rate_sped_2018.csv', index=False, quoting=csv.QUOTE_NONNUMERIC,
    columns=['District', 'FIPS', 'Year', 'Special Education Status', 'Variable', 'Measure Type', 'Value'])
