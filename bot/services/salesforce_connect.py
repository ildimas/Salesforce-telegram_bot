from simple_salesforce import Salesforce, SalesforceMalformedRequest
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN_SF = os.getenv("TOKEN_SF")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SECUTITY_TOKEN = os.getenv("SECUTITY_TOKEN")

#! sf = Salesforce(instance_url=INSTANCE, session_id=TOKEN)
sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECUTITY_TOKEN)

async def sf_company_create(company_name):
    data = {
        'Name': company_name
    }
    try:
        new_company = sf.Company__c.create(data)
        return new_company['id']
    except SalesforceMalformedRequest as e:
        print(f"Failed to create company", e)
        
async def sf_findout_comp_id(company_name):
    query = f"SELECT Id FROM Company__c WHERE Name = '{company_name}' LIMIT 1"
    results = sf.query_all(query)
    for result in results['records']:
        return result['Id']
    
    
async def sf_user_create(user_name):
    data = {
        'Name': user_name
    }
    try:
        new_user = sf.TUser__c.create(data)
        return new_user['id']
    except SalesforceMalformedRequest as e:
        print(f"Failed to create user", e)
        
        
async def sf_ticket_create(ticket_name, user_sf_id, company_sf_id):
    data = {
        'Name': ticket_name,
        'TUser__c' : user_sf_id,
        'Company__c' : company_sf_id
    }
    try:
        new_ticket = sf.Ticket__c.create(data)
        return new_ticket['id']
    except SalesforceMalformedRequest as e:
        print(f"Failed to create ticker", e)
        
async def sf_message_create(ticket_sf_id, body):
    data = {
        'Ticket__c': ticket_sf_id,
        'Type__c' : "incoming",
        'Body__c' : body
    }
    try:
        new_message = sf.Message__c.create(data)
        return new_message['id']
    except SalesforceMalformedRequest as e:
        print(f"Failed to create message", e)

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


# #! Second Example
# query = "SELECT Id, Name FROM Account LIMIT 50"
# accounts = sf.query_all(query)

# for account in accounts['records']:
#     print(account['Id'], account['Name'])

#! Thired example
# new_account = sf.Account.create({
#     'Name': 'New Account Name',
#     'Phone': '1234567890'
# })

# print("New account created with ID:", new_account['id'])

# sf.Account.update(new_account['id'], {
#     'Phone': '0987654321'
# })

# print("Account updated successfully.")
