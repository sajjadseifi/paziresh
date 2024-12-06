import pandas as pd

file_path = "D:/unittest/ensaniapp/soldiers/list.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Display the first few rows to understand its structure
df.head()
list_yegan_bekargirande = []
temp = 1
# Loop through the dataframe and create tuples (organization name, type, province, address)
for index, row in df.iterrows():
    org_name = row[0].replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c", " ")
    org_type = row[1].replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c", " ")
    province = row[2].replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c", " ")
    address = row[3].replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c", " ")

    # Create tuple and append to list
    list_yegan_bekargirande.append((temp, org_name, org_type, province, address))
    temp += 1
# Displaying the final list
print(list_yegan_bekargirande)
