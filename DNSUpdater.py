import requests
import json
import re
import sys, time
import logging
from pathlib import Path

#To use this, do logger = get_module_logger(__name__)
def get_module_logger(mod_name):
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

logger = get_module_logger("cloudflareddnsUpdater")

logger.info("cloudflareddnsUpdater starting")

##Cloudflare endpoints
CF_ZONE_URL = 'https://api.cloudflare.com/client/v4/zones/'
CF_TRACE = 'https://cloudflare.com/cdn-cgi/trace' 


filepath = Path(__file__).parent / "config.json"

with open(filepath, 'r') as f:
    configJson = json.load(f)


api_key = configJson["api_key"]
#logger.info("API Key to be used:", api_key)

requests.packages.urllib3.util.connection.HAS_IPV6 = False

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

def get_zone_id(domain, headers):
    params = {'name': domain}
    response = requests.get(CF_ZONE_URL, headers=headers, params=params)
    if response.status_code == 200:
        zones = response.json()['result']
        if len(zones) > 0:
            return zones[0]['id']
    return None
    
def get_public_ip():
   response = requests.get(CF_TRACE)
   match = re.search(r'^ip=([\d\.]+)', response.text, re.MULTILINE)
   return match.group(1).strip()

def get_public_ipv6():
   ipv6_pattern = re.compile(r'ip=([a-fA-F0-9:]+)')
   response = requests.get(CF_TRACE)
   match = ipv6_pattern.search(response.text, re.MULTILINE)
   return match.group(1).strip()




# Iterate through domains
for domain_info in configJson["domains"]:
    
    logger.info("##################################")
    domain = domain_info["domain"]
    logger.info(f"Domain: {domain}")

    zone_id = get_zone_id(domain, headers)

    if not zone_id:
        logger.info(f"Zone ID for {domain} not found")
        sys.exit(0)

    response = requests.get(CF_ZONE_URL + f"{zone_id}/dns_records", headers=headers)

    if response.status_code == 200:
        dns_records = json.loads(response.text)['result']
        
        for subdomains in domain_info["subdomains"]:

            subdomain = subdomains["subdomain_name"]
            record_type = subdomains["record_type"]
            proxied = subdomains["proxied"]            

            logger.info(f"Subdomain: {subdomain}")
            for record in dns_records:
                if record['type'] == record_type.upper() and record['name'] == subdomain:
                    record_id = record['id']
                    existing_IP = record['content']
                    break

            if record_type.upper() in ['A','MX','NS']:
                ip = get_public_ip()
            else:
                requests.packages.urllib3.util.connection.HAS_IPV6 = True
                ip = get_public_ipv6()
                requests.packages.urllib3.util.connection.HAS_IPV6 = False

            if ip == existing_IP:
                logger.info("Same IP no update required")
                continue

            post_data = {
	            "content": ip,
                "name": subdomain,
                'proxied': proxied,
                "type": record_type.upper(),
                "comment": "DNS Record updated using DNSUpdater at " + time.strftime("%H:%M:%S on %Y-%m-%d", time.localtime(time.time())),
                "ttl": 0
            }
            # Update the record via PUT request
            response = requests.put(CF_ZONE_URL + f"{zone_id}/dns_records/{record_id}", headers=headers, data=json.dumps(post_data))

            if response.status_code == 200:
                logger.info('Record updated successfully')
            else:
                logger.info('Error updating record:', response.text)


    else:
        logger.info(f"Error fetching DNS records for {domain}: {response.text}")
        continue


logger.info("cloudflareddnsUpdater finished")