import requests
import time
from ping3 import ping

# Configuration
router_ip = "192.168.1.1"
check_interval = 60   # in seconds
login_payload = {"login": "admin", "password": "admin", "logout": False}
headers = {
    "Host": "192.168.1.1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://192.168.1.1",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://192.168.1.1/",
    "Cookie": "username=admin; session=EB305258AE1910E01ECA70DC7E12E625",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}


dhcp_payload = {
    "enable": True,
    "ipStart": "192.168.1.51",
    "ipEnd": "192.168.1.244",
    "netmask": "255.255.255.0",
    "gateway": "192.168.1.1",
    "autoDNS": False,
    "DNS": "8.8.8.8,8.8.4.4",
    "leaseTime": 86400
}

# Function to check router connectivity
def is_router_reachable():
    try:
        ping_output = ping(router_ip)
        return ping_output is not None
    except OSError as e:
        print(f"Error checking router reachability: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Function to handle the PUT and GET requests
def process_router_session():
    try:
        # PUT request to establish a session
        put_response = requests.put(f"https://{router_ip}/api/usersession/", json=login_payload, headers=headers, verify=False)
        if put_response.status_code == 200:
            session_token = put_response.json().get("sessionToken")
            if session_token:
                print(f"Session token obtained: {session_token}")

                # GET request to verify session
                get_response = requests.get(
                    f"https://{router_ip}/api/usersession/sessions/{session_token}",
                    headers={"Cookie": f"username=admin; session={session_token}"},
                    verify=False
                )

                if get_response.status_code == 200:
                    print("Session verified successfully:", get_response.json())

                    # PUT request to update DHCP settings
                    dhcp_headers = {
                        "Cookie": f"username=admin; session={session_token}",
                        "Content-Type": "application/json",
                    }
                    dhcp_response = requests.put(
                        f"https://{router_ip}/api/service/dhcpservers/1",
                        json=dhcp_payload,
                        headers=dhcp_headers,
                        verify=False
                    )

                    if dhcp_response.status_code == 200:
                        print("DHCP settings updated successfully:", dhcp_response.json())
                    else:
                        print(f"Failed to update DHCP settings. Status Code: {dhcp_response.status_code}")
                else:
                    print(f"Failed to verify session. Status Code: {get_response.status_code}")
            else:
                print("Session token not found in the PUT response.")
        else:
            print(f"PUT request failed. Status Code: {put_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Main monitoring loop
if __name__ == "__main__":
    process_router_session()
    print("Monitoring router status...")
    was_reachable = is_router_reachable()
    while True:
        time.sleep(check_interval)
        is_reachable = is_router_reachable()

        if not was_reachable and is_reachable:
            print("Router reconnected. Initiating API requests...")
            process_router_session()

        was_reachable = is_reachable
