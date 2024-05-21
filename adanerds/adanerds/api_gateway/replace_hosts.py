import json
import sys
import logging

# Set the logging level
logging.basicConfig(level=logging.INFO)


old_hosts = ["authentication_service", "account_service", "booking_service", "listing_service", "picture_service"]


def replace_hosts(json_path, new_hosts):
    # Read the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Iterate through the endpoints and replace the host
    for endpoint in data.get('endpoints', []):
        for backend in endpoint.get('backend', []):
            if 'host' in backend:
                if "auth" in backend['host'][0]: 
                    # Find the index in hosts that contains "auth"
                    index = next((i for i, host in enumerate(new_hosts) if "auth" in host), None)
                    backend['host'] = [new_hosts[index]]
                elif "account" in backend['host'][0]:
                    # Find the index in hosts that contains "account"
                    index = next((i for i, host in enumerate(new_hosts) if "account" in host), None)
                    backend['host'] = [new_hosts[index]]
                elif "booking" in backend['host'][0]:
                    # Find the index in hosts that contains "booking"
                    index = next((i for i, host in enumerate(new_hosts) if "booking" in host), None)
                    backend['host'] = [new_hosts[index]]
                elif "listing" in backend['host'][0]:
                    # Find the index in hosts that contains "listing"
                    index = next((i for i, host in enumerate(new_hosts) if "listing" in host), None)
                    backend['host'] = [new_hosts[index]]
                elif "picture" in backend['host'][0]:
                    # Find the index in hosts that contains "event"
                    index = next((i for i, host in enumerate(new_hosts) if "event" in host), None)
                    backend['host'] = [new_hosts[index]]
                    
    # Write the updated JSON back to the file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 3:
        logging.info(f"Usage: {sys.argv[0]} <path_to_json> <path_to_txt>")
        sys.exit(1)

    json_path = sys.argv[1]
    txt_path = sys.argv[2]

    # Read the hosts from the txt file into a list
    with open(txt_path, 'r') as file:
        hosts = file.read().splitlines()

    # Only keep the hosts that contain auth, account, booking, and listing
    hosts = [host for host in hosts if any(old_host in host for old_host in ["auth-service", "account-service", "booking-service", "listing-service", "listing-event"])]

    replace_hosts(json_path, hosts)
    logging.info(f"Hosts in {json_path} have been replaced with hosts from {txt_path}")
