from simple_salesforce.api import Salesforce
import os

TOKEN = os.getenv("SF_TOKEN")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SECUTITY_TOKEN = os.getenv("SECUTITY_TOKEN")

# sf = Salesforce(instance_url=INSTANCE, session_id=TOKEN)
sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECUTITY_TOKEN)

query = "SELECT Id, Name FROM Account LIMIT 50"
accounts = sf.query_all(query)

for account in accounts['records']:
    print(account['Id'], account['Name'])


#*-----------------------------
# new_account = sf.Account.create({
#     'Name': 'New Account Name',
#     'Phone': '1234567890'
# })

# print("New account created with ID:", new_account['id'])

# sf.Account.update(new_account['id'], {
#     'Phone': '0987654321'
# })

# print("Account updated successfully.")


#*-----------------------------
# new_account_data = {
#     'Name': 'New Account Name',
#     'Phone': '1234567890',
#     'Website': 'https://newaccount.com',
#     'BillingStreet': '123 Main St',
#     'BillingCity': 'San Francisco',
#     'BillingState': 'CA',
#     'BillingPostalCode': '94105',
#     'BillingCountry': 'USA'
# }

# try:
#     new_account = sf.Account.create(new_account_data)
#     print(f"New account created with ID: {new_account['id']}")
# except SalesforceMalformedRequest as e:
#     print(f"Failed to create account: {e.content}")