#!/usr/bin/env python3
import requests
import sys
import argparse
from router_common import login_to_router, get_auth_headers, ROUTER_IP

def update_dns_settings(primary_dns="192.168.1.50", secondary_dns="1.1.1.1"):
    """Update the DNS settings on the router"""
    
    # First login to get session token
    session_token = login_to_router()
    if not session_token:
        print("Failed to login to router. Cannot update DNS settings.")
        return False
    

    # Prepare DHCP payload with DNS settings
    dhcp_payload = {
        "enable": True,
        "ipStart": "192.168.1.2",
        "ipEnd": "192.168.1.244",
        "netmask": "255.255.255.0",
        "gateway": "192.168.1.1",
        "autoDNS": False,
        "DNS": f"{primary_dns},{secondary_dns}",
        "leaseTime": 86400
    }
    
    auth_headers = get_auth_headers(session_token)
    
    try:
        # Send DHCP update request
        dhcp_response = requests.put(
            f"https://{ROUTER_IP}/api/service/dhcpservers/1",
            json=dhcp_payload,
            headers=auth_headers,
            verify=False
        )
        
        if dhcp_response.status_code == 200:
            print(f"DNS settings updated successfully to {primary_dns}, {secondary_dns}")
            return True
        else:
            print(f"Failed to update DNS settings. Status Code: {dhcp_response.status_code}")
            try:
                print(f"Response: {dhcp_response.json()}")
            except:
                print(f"Response text: {dhcp_response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during DNS update: {e}")
    
    return False

if __name__ == "__main__":
    # Setup command line arguments
    parser = argparse.ArgumentParser(description='Update router DNS settings')
    parser.add_argument('--primary', default='192.168.1.50', help='Primary DNS server (default: 192.168.1.50)')
    parser.add_argument('--secondary', default='1.1.1.1', help='Secondary DNS server (default: 1.1.1.1)')
    
    args = parser.parse_args()
    
    print(f"Starting DNS update process with DNS servers: {args.primary}, {args.secondary}...")
    success = update_dns_settings(args.primary, args.secondary)
    sys.exit(0 if success else 1)
