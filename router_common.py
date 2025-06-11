import requests
import time
from ping3 import ping
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
ROUTER_IP = "192.168.1.1"
CHECK_INTERVAL = 60  # in seconds
LOGIN_PAYLOAD = {"login": "admin", "password": "admin", "logout": False}
BASE_HEADERS = {
    "Host": "192.168.1.1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": f"https://{ROUTER_IP}",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": f"https://{ROUTER_IP}/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}

# Function to check router connectivity
def is_router_reachable():
    try:
        ping_output = ping(ROUTER_IP)
        return ping_output is not None
    except OSError as e:
        print(f"Error checking router reachability: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Function to login to the router and get a session token
def login_to_router():
    try:
        # PUT request to establish a session
        put_response = requests.put(
            f"https://{ROUTER_IP}/api/usersession/", 
            json=LOGIN_PAYLOAD, 
            headers=BASE_HEADERS, 
            verify=False
        )
        
        if put_response.status_code == 200:
            session_token = put_response.json().get("sessionToken")
            if session_token:
                print(f"Session token obtained: {session_token}")
                
                # GET request to verify session
                get_response = requests.get(
                    f"https://{ROUTER_IP}/api/usersession/sessions/{session_token}",
                    headers={"Cookie": f"username=admin; session={session_token}"},
                    verify=False
                )

                if get_response.status_code == 200:
                    print("Session verified successfully")
                    return session_token
                else:
                    print(f"Failed to verify session. Status Code: {get_response.status_code}")
            else:
                print("Session token not found in the PUT response.")
        else:
            print(f"PUT request failed. Status Code: {put_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during login: {e}")
    
    return None

# Function to create session-authenticated headers
def get_auth_headers(session_token):
    headers = BASE_HEADERS.copy()
    headers["Cookie"] = f"username=admin; session={session_token}"
    return headers

# Function to wait for router to become available
def wait_for_router_availability():
    print("Monitoring router status...")
    was_reachable = is_router_reachable()
    
    if not was_reachable:
        print("Router not reachable. Waiting for it to come online...")
        
    while not was_reachable:
        time.sleep(CHECK_INTERVAL)
        is_reachable = is_router_reachable()
        
        if not was_reachable and is_reachable:
            print("Router is now online")
            return True
            
        was_reachable = is_reachable
    
    return True
