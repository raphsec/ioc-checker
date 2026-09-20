import os
import requests
from dotenv import load_dotenv

# Load API keys securely from the .env file (never hardcoded)
load_dotenv()
ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_API_KEY")
VIRUSTOTAL_KEY = os.getenv("VIRUSTOTAL_API_KEY")


def check_abuseipdb(ip):
    """
    Queries AbuseIPDB for a given IP address.
    Returns an abuse confidence score (0-100%) based on
    historical abuse reports for that IP.
    """
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": ABUSEIPDB_KEY,
        "Accept": "application/json"
    }
    params = {"ipAddress": ip, "maxAgeInDays": 90}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data["data"]["abuseConfidenceScore"]


def check_virustotal(ip):
    """
    Queries VirusTotal for a given IP address.
    Returns the number of antivirus/security engines (out of ~70)
    that flag the IP as malicious.
    """
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": VIRUSTOTAL_KEY}

    response = requests.get(url, headers=headers)
    data = response.json()

    stats = data["data"]["attributes"]["last_analysis_stats"]
    return stats["malicious"]


def main():
    """
    Main entry point: prompts the user for an IP address,
    queries both threat intel sources, and prints a combined verdict.
    """
    ip = input("Enter an IP address to check: ").strip()
    print(f"\nChecking {ip}...\n")

    abuse_score = check_abuseipdb(ip)
    vt_malicious = check_virustotal(ip)

    print(f"AbuseIPDB Confidence Score: {abuse_score}%")
    print(f"VirusTotal Malicious Detections: {vt_malicious}")

    # Flag as malicious if either source shows a strong signal
    if abuse_score > 50 or vt_malicious > 0:
        print("\nVerdict: ⚠️  MALICIOUS / SUSPICIOUS")
    else:
        print("\nVerdict: ✅ CLEAN")


if __name__ == "__main__":
    main()