import requests
import json
import sys

#imports user email from offboarding script
userEmail = sys.argv[1]
key = sys.argv[2]

print(f"Searching Okta for {userEmail}. Please wait...")
print('')

# Finds a user by email
url = f"https://yourdomainname.okta.com/api/v1/users?q={userEmail}&limit=1"

payload = {}
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': f'SSWS {key}'
}

response = requests.request("GET", url, headers=headers, data=payload)

userData = json.loads(response.text)

userID = userData[0]['id']

#Deactivates a user by ID
url = f"https://yourdomainname.okta.com/api/v1/users/{userID}/lifecycle/deactivate"

payload  = {}
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': f'SSWS {key}'
}

response = requests.request("POST", url, headers=headers, data = payload)

result = json.loads(response.text)

print(f'{userEmail} has been Deactivated')
print('')

#Deletes a user by ID
url = f"https://yourdomainname.okta.com/api/v1/users/{userID}"

payload = {}
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': f'SSWS {key}'
}

response = requests.request("DELETE", url, headers=headers, data = payload)

print(f'{userEmail} has been deleted from Okta')
print('')
