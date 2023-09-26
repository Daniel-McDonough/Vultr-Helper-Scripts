"""
Displays Vultr instances and imports instances into Terraform
"""
import os
import json
import subprocess
import argparse
import requests


# Read Vultr API key from environment variable
API_KEY = os.getenv('VULTR_API_KEY')

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Vultr Instance Helper.',
                                 epilog='Reads API key from VULTR_API_KEY envar.')
parser.add_argument('-i', '--imports', action='store_true', required=False, default=False,
                    help='Import an instance')
parser.add_argument('-v', '--verbose', action='store_true', required=False, default=False,
                    help='Print instance details')

args = parser.parse_args()

if not API_KEY:
    raise ValueError("VULTR_API_KEY environment variable is not set.")

# API endpoint URL
API_URL = 'https://api.vultr.com/v2/instances'

# Set the headers for authentication
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def tf_run(cmd):

    try:
        subprocess.run(cmd,  check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command:\n{' '.join(cmd)}\nfailed with exit code {e.returncode}.")

def vultr_import(instances):
    """
    Takes instances list and imports selected instance.
    """
    # Prompt user to select an instance
    instance_number = input('Enter the number of the instance to import: ')

    try:
        instance_index = int(instance_number) - 1
        if instance_index < 0 or instance_index >= len(instances):
            raise ValueError
    except ValueError:
        print('Invalid instance number.')
        exit

    selected_instance = instances[instance_index]
    resource_name = input('Enter the resource name: ')

    print("Running Terraform Import.")
    # Run Terraform import command
    cmd = ['terraform', 'import', f'vultr_instance.{resource_name}', selected_instance['id']]
    tf_run(cmd)

# Make a GET request to the Vultr API to list instances
response = requests.get(API_URL, headers=headers, timeout=5)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    instances = json.loads(response.text)['instances']

    # Check if there are instances
    if instances:
        print('Instances in your Vultr account:')
        for i, instance in enumerate(instances):
            print(f'{i + 1}. {instance["label"]}')
            if args.verbose:
                print(f"- Name: {instance['label']}")
                print(f"  ID: {instance['id']}")
                print(f"  Status: {instance['status']}")
                print(f"  IP: {instance['main_ip']}")
                print(f"  Plan: {instance['plan']}")
                print(f"  Region: {instance['region']}")

        print('---')
        if args.imports:
            vultr_import(instances)

    else:
        print('No instances found in your Vultr account.')
else:
    print(f'Failed to retrieve instances. Error: {response.text}')
