import pandas as pd
import re
import xlsxwriter

# Read the txt file
with open('C:/Users/PANTUM/Desktop/log.txt', 'r', encoding='utf-8') as file:
    # Define the regex pattern
    regex = r'^(\d+):([a-zA-Z ]+):(.+)$'
    # Read the txt file
    lines = file.readlines()
    # Parse each line
    parsed_lines = []
    # Print each line
    for line in lines:
        match = re.match(regex, line)
        if match:
            if match.group(2) == 'PAP':
                parsed_lines.append(match.groups())
        else:
            print("No match")

# Create a pandas DataFrame
df = pd.DataFrame(parsed_lines, columns=['time(ms)', 'module', 'description'])
# Write the DataFrame to an Excel file
with pd.ExcelWriter('C:/Users/PANTUM/Desktop/log_parsed.xlsx', engine='xlsxwriter') as writer:
    # Write the DataFrame to the Excel file
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    # Set the column width
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 50)