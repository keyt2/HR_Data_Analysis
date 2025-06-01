import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here


a_office = pd.read_xml('../Data/A_office_data.xml')
b_office = pd.read_xml('../Data/B_office_data.xml')
hr_data = pd.read_xml('../Data/hr_data.xml')

a_office = a_office.set_index('employee_office_id', drop=False)
a_office.index = 'A' + a_office.index.astype(str)
a_office.index.name = None
b_office = b_office.set_index('employee_office_id', drop=False)
b_office.index = 'B' + b_office.index.astype(str)
b_office.index.name = None
hr_data = hr_data.set_index('employee_id', drop=False)

a_b_office = pd.concat([a_office, b_office])
office = a_b_office.merge(hr_data, how='left', left_index=True, right_index=True, indicator=True)
office = office[office['_merge'] == 'both']
office.drop(['employee_office_id', 'employee_id', '_merge'], axis=1, inplace=True)
office.sort_index(inplace=True)

# office.sort_values(by='average_monthly_hours',ascending=False, inplace=True)
top_10 = office.head(10)
filtered = office[(office['Department'] == 'IT') & (office['salary'] == 'low')]
number_projects = filtered['number_project'].sum()
three_employees = [[float(v) for v in office.loc['A4', ['last_evaluation', 'satisfaction_level']]],
                   [float(v) for v in office.loc['B7064', ['last_evaluation', 'satisfaction_level']]],
                   [float(v) for v in office.loc['A3033', ['last_evaluation', 'satisfaction_level']]]]

def count_bigger_5(series):
    return (series > 5).sum()

# print(office.groupby(['left']).agg({'number_project' : ['median', count_bigger_5],
#                                     'time_spend_company' : ['mean', 'median'],
#                                     'Work_accident' : 'mean',
#                                     'last_evaluation' : ['mean', 'std']}).round(2).to_dict())

first_pivot = office.pivot_table(index='Department', columns=['left', 'salary'], values='average_monthly_hours', aggfunc='median')
second_pivot = office.pivot_table(index='time_spend_company', columns='promotion_last_5years', values=['last_evaluation', 'satisfaction_level'], aggfunc=['min', 'max', 'mean'])

print(first_pivot[(first_pivot[(0, 'high')] < first_pivot[(0, 'medium')]) |
                  (first_pivot[(1, 'low')] < first_pivot[(1, 'high')])].round(2).to_dict())
print(second_pivot[second_pivot[('mean', 'last_evaluation', 0)] >
      second_pivot[('mean', 'last_evaluation', 1)]].round(2).to_dict())