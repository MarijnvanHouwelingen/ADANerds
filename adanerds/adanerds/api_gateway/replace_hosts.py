import json
import sys
import logging

# Set the logging level
logging.basicConfig(level=logging.INFO)


old_hosts = ["authentication_service", "account_service", "listing_service", "booking_service"]


def replace_hosts(json_path, new_host):
    # Read the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Iterate through the endpoints and replace the host
    for endpoint in data.get('endpoints', []):
        for backend in endpoint.get('backend', []):
            if 'host' in backend:
                backend['host'] = [new_host]

    # Write the updated JSON back to the file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 3:
        logging.info(f"Usage: {sys.argv[0]} <path_to_json> <new_host>")
        sys.exit(1)

    json_path = sys.argv[1]
    new_host = sys.argv[2]

    replace_hosts(json_path, new_host)
    logging.info(f"Hosts in {json_path} have been replaced with {new_host}")
