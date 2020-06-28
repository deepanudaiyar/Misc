import requests
import json
import re
import random
import sys

# importing username and password of Jamf as system arguments
username = sys.argv[1]
key  = sys.argv[2]

print('Fetching details of all computers.Please wait...')

url = "https://yourdomainname.jamfcloud.com/JSSResource/computers/subset/basic"

username = f'{username}'
password = f'{key}'
payload = {}
headers = {
  'Accept': 'application/json'
}

response = requests.get(url, headers=headers, auth=(username, password)).json()

allComputerData = response['computers']

# retrieves all the computer names from the data and saves into a list
computerNameList = []
for computer in allComputerData:
	computerName = computer['name']
	computerNameList.append(computerName)

# Search for user's relevant details in the name list and prints out the full computer name
print('')
print('A computer name can either be a Firstname or Lastname or combination of both for a user. \n Try either one of details to find the potential computer name.')
print('')

# This function makes sure that the input is not empty
def checkInput(lastName):
	lastName = input(lastName)
	while not lastName:
		print('')
		print("Input can't be empty...")
		print('')
		lastName = input("Enter either Firstname or Lastname: ")
	return lastName

lastName = checkInput("Enter either Firstname or Lastname: ")

# This function as the name implies helps to search computer name and pipes all that results to a list.
def searchComputerName(lastName):
	computerExists = []
	counter = 0
	while not computerExists:
		if counter !=0:
			print('')
			print('Unable to find a computer. Try again..')
			print('')
			lastName = checkInput("Enter either Firstname or Lastname: ")
		for item in computerNameList:
			if bool(re.search(f"{lastName}", item, re.IGNORECASE)):
				computerExists.append(item)
		counter += 1
	
	print('')
	print('Computer name/names found , please copy one of the name below for the next step.')
	print('')
	print(computerExists)
	print('')

searchComputerName(lastName)

# This function serves as a loop in searching computer name
def foundComputer(question):
	username = sys.argv[1]
	key  = sys.argv[2]
	reply = input(question+' (y/n): ').lower().strip()
	if reply[:1] == 'y':
		print('')
		#Searching of computer id in the computer data
		userComputerName = input("Enter the computer name to lock it? :")
		while not userComputerName:
			print('')
			print("Computer name can't be empty..")
			print('')
			userComputerName = input("Enter the computer name to lock it? :")

		computerID = ""
		for item in allComputerData:
			if item['name'] == userComputerName:
				computerID = item['id']

		# generating random pin for passcode
		passcode = ""
		for number in range(6):
			number   = random.randint(1,9)
			number   = str(number)
			passcode = passcode.__add__(number)

		# locking the device with random passcode
		url = f"https://yourdomainname.jamfcloud.com/JSSResource/computercommands/command/devicelock/passcode/{passcode}/id/{computerID}"
		username = f'{username}'
		password = f'{key}'
		payload = {}
		headers = {
		'Accept': 'application/xml',
		'Content-Type': 'application/xml'
		}
		requests.request("POST", url, headers=headers,auth=(username, password), data = payload)
		print('')
		print(f"Devicelock command has been sent to {userComputerName} with passcode of {passcode}.")

	elif reply[:1] == 'n':
		print('')
		print('Alrighty, let\'s try again')
		print('')
		lastName = checkInput("Enter either Firstname or Lastname: ")
		searchComputerName(lastName)
		foundComputer(question)
	else:
		print("Please enter a valid option")
		return foundComputer(question)

foundComputer("Do you see your users computer name above to lock it ?")


