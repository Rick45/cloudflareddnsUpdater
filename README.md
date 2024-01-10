# DNSUpdater

## Description
This Python script automates the process of updating DNS records for specific subdomains under Cloudflare. It fetches the current public IP address (both IPv4 and IPv6) and compares it with the existing IP recorded in Cloudflare. If a change is detected, it updates the DNS record accordingly.

## Prerequisites
- Python 3.x installed
- Cloudflare API key
- Configured `config.json` file containing necessary configurations

## Installation
1. Clone or download this repository.
2. Ensure Python 3.x is installed.
3. Install the required dependencies using `pip install -r requirements.txt`.

## Obtaining Cloudflare API Key

To use this script, you'll need a Cloudflare API key. Here are the steps to obtain it:

1. **Login to Cloudflare:** Visit [Cloudflare](https://www.cloudflare.com/) and log in to your account.

2. **Access API Tokens:** Go to the **"My Profile"** section or navigate to **"Account" > "API Tokens"** in the Cloudflare dashboard.

3. **Create API Token:** Click on **"Create Token"** or **"Create Token"** button to generate a new API token.

4. **Select Permissions:** Choose the appropriate permissions for your token. At a minimum, it requires permissions to edit DNS records.

5. **Generate API Key:** Once permissions are set, generate the API key. It will be displayed once and should be copied and securely stored.

6. **Add API Key to Configuration:** Paste the generated API key into the `api_key` field within the `config.json` file for this script.

7. **Save and Secure:** Ensure the API key is saved securely. Do not expose or share it publicly.

Refer to Cloudflare's official documentation for more detailed instructions on generating and managing API tokens.

## Configuration
1. Create a `config.json` file based on the provided `config.json.example` with your Cloudflare API key and domain details.
2. Populate the `config.json` file with your specific domain, subdomain, record type, and proxied status.

## Usage
1. Ensure `config.json` is properly configured.
2. Run the script using Python: `python dns_updater.py`.
3. The script will fetch the current public IP addresses and update the Cloudflare DNS records if changes are detected.

## Additional Notes
- This script currently supports A, MX, NS record types and handles both IPv4 and IPv6 addresses.
