#!/usr/bin/env python3

import subprocess
import string

url = "http://agent.thm"

def send_request(user_agent):
    curl_command = f"curl -s -L -H 'user-agent: {user_agent}' {url}"
    response = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    return response.stdout.strip()

found_message = "" 

for letter in string.ascii_uppercase:
    response = send_request(letter)

    if "<html>" in response:
        print(f"❌ Attempt with user-agent: {letter} - HTML response detected")
    else:
        print(f"✅ Possible user-agent found: {letter}")
        found_message = response 
        # You can use the break statement if you don't want to test more than one exception 

if found_message:
    with open("agent_message.txt", "w") as file:
        file.write(found_message)
    print("\n📄 Message saved to 'agent_message.txt'")