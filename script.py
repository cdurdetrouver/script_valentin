import sys
import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# File reading and processing
def process_file(file_path):
	names = set()
	
	try:
		with open(file_path, 'r') as file:
			for line in file:
				names.add(line.split()[0])
	except FileNotFoundError:
		print(f"Error: The file {file_path} was not found.")
	except ValueError:
		print("Error: The file contains non-numeric data.")

	return names


def getToken() -> str:
	client_id = os.getenv('UUID')
	client_secret = os.getenv('SECRET')
	body = {"client_id":client_id, "client_secret":client_secret, "grant_type":"client_credentials"}

	response = requests.post("https://api.intra.42.fr/oauth/token", data=body)
	
	token = response.text.split('"')
	# if (token[2] == "error"):
	return (token[3])



def make_request():
	api_url = "https://api.intra.42.fr/v2/user/" + login
	token = getToken()

	headers = {
		"Authorization": f"Bearer {token}"
	}
	
	response = requests.get(api_url, headers=headers)
	
	if response.status_code == 200:
		print("token generated successfully!")
		return response.json()
	else:
		print(f"token failed with status code {response.status_code}")
		return None
	
def get_location(login, token):
	api_url = "https://api.intra.42.fr/v2/users/" + login

	headers = {
		"Authorization": f"Bearer {token}"
	}
	
	for i in range(3):
		response = requests.get(api_url, headers=headers)

		if response.status_code == 200:
			# print("Request successful!")
			return response.json().get("location")

		time.sleep(1)
	return None


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python main.py <file_path>")
		sys.exit(1)

	file_path = sys.argv[1]
	names = process_file(file_path)
	token = getToken()
	for login in names:
		loc = get_location(login, token)
		if loc != None:
			print(loc, login)
		time.sleep(0.2)


