f = open("employee_data.csv", "r")
f_new = open("employee_data_new_format.csv", "w")
count = 0
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}
for line in f:
    if count == 0:
        f_new.write("Emp ID,First Name,Last Name,DOB,SSN,State\n")

    else:
        print("Original line:")
        print(line)
        new_line = line.split(",")
        name = new_line[1].split()
        date = new_line[2].split("-")
        phone_num = new_line[3].split("-")
        altered_line = new_line[0] + "," + name[0] + "," + name[1] + "," + date[1] + "/" + date[2] + "/" + date[0] + "," + "***-**-" + phone_num[2] + "," + us_state_abbrev[new_line[4].strip("\n")] + "\n"
        print("Altered line:")
        print(altered_line)
        f_new.write(altered_line)
    count += 1
f.close()
f_new.close()
