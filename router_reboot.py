#!/usr/bin/env python3
import requests
import sys
from router_common import login_to_router, get_auth_headers, wait_for_router_availability, ROUTER_IP

def reboot_router():
    """Reboot the router using API call"""
    
    # First login to get session token
    session_token = login_to_router()
    if not session_token:
        print("Failed to login to router. Cannot reboot.")
        return False
    
    # Prepare reboot payload and headers
    reboot_payload = {"command": "reboot"}
    auth_headers = get_auth_headers(session_token)
    
    try:
        # Send reboot command
        reboot_response = requests.put(
            f"https://{ROUTER_IP}/api/devicectrl",
            json=reboot_payload,
            headers=auth_headers,
            verify=False
        )
        
        if reboot_response.status_code == 200:
            print("Reboot command sent successfully")
            
            # Wait for router to come back online
            print("Router is rebooting. Waiting for it to come back online...")
            if wait_for_router_availability():
                print("Router reboot completed successfully")
                return True
        else:
            print(f"Failed to reboot router. Status Code: {reboot_response.status_code}")
            try:
                print(f"Response: {reboot_response.json()}")
            except:
                print(f"Response text: {reboot_response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during reboot: {e}")
    
    return False

if __name__ == "__main__":
    print("Starting router reboot process...")
    success = reboot_router()
    sys.exit(0 if success else 1)
