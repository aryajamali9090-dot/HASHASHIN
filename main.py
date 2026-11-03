import os
import sys
import re
import ssl
import socket
import string
import secrets
import hashlib
import platform
import urllib.request
from urllib.parse import urlsplit

G = "\033[92m"
C = "\033[96m"
R = "\033[91m"
W = "\033[97m"
Y = "\033[93m"
RESET = "\033[0m"

def clear():
    os.system("clear")

def banner():
    print(G + r"""
 _   _    _    ____  _   _    _    ____  _   _
| | | |  / \  / ___|| | | |  / \  / ___|| | | |
| |_| | / _ \ \___ \| |_| | / _ \ \___ \| |_| |
|  _  |/ ___ \ ___) |  _  |/ ___ \ ___) |  _  |
|_| |_/_/   \_\____/|_| |_/_/   \_\____/|_| |_|

""" + RESET)
    print(C + "       HASHASHIN V1.1")
    print("       MULTI TOOL ENVIRONMENT")
    print("-" * 45 + RESET)

def pause():
    input(W + "\nPress Enter to continue..." + RESET)

def password_generator():
    clear()
    banner()
    try:
        n = int(input("Password length (8-128): "))
        if not 8 <= n <= 128:
            print(R + "Invalid length!")
        else:
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(secrets.choice(chars) for _ in range(n))
            print(G + "\nGenerated password: " + password)
    except ValueError:
        print(R + "Invalid input!")
    pause()

def password_checker():
    clear()
    banner()
    p = input("Enter password to check: ")

    score = 0
    score += len(p) >= 8
    score += len(p) >= 12
    score += any(c.islower() for c in p)
    score += any(c.isupper() for c in p)
    score += any(c.isdigit() for c in p)
    score += any(not c.isalnum() for c in p)

    if score <= 2:
        result = "WEAK"
        color = R
    elif score <= 4:
        result = "MEDIUM"
        color = Y
    else:
        result = "STRONG"
        color = G

    print(color + "\nPassword rating:", result)
    print(W + "Checks passed:", score, "/ 6")
    print(Y + "This is a basic estimate, not a security guarantee.")
    pause()

def hash_generator():
    clear()
    banner()
    data = input("Enter text: ").encode()

    print(G + "\nSHA256:", hashlib.sha256(data).hexdigest())
    print("SHA512:", hashlib.sha512(data).hexdigest())
    print("MD5:", hashlib.md5(data).hexdigest())
    print(Y + "\nMD5 is outdated and should not be used for security.")
    pause()

def hash_identifier():
    clear()
    banner()
    value = input("Enter hash: ").strip()

    if re.fullmatch(r"[a-fA-F0-9]{32}", value):
        result = "Possible MD5"
    elif re.fullmatch(r"[a-fA-F0-9]{40}", value):
        result = "Possible SHA1"
    elif re.fullmatch(r"[a-fA-F0-9]{64}", value):
        result = "Possible SHA256"
    elif re.fullmatch(r"[a-fA-F0-9]{128}", value):
        result = "Possible SHA512"
    else:
        result = "Unknown or unsupported format"

    print(C + "\nResult:", result)
    print(Y + "Identification is based on length and format only.")
    pause()

def url_analyzer():
    clear()
    banner()
    raw = input("Enter URL: ").strip()

    if not raw:
        print(R + "Empty URL")
        pause()
        return

    try:
        url = raw if "://" in raw else "https://" + raw
        parsed = urlsplit(url)
        host = parsed.hostname

        if not host or parsed.scheme not in ("http", "https"):
            print(R + "Invalid URL")
            pause()
            return

        print(C + "\nURL ANALYSIS")
        print(W + "Host:", host)
        print("Protocol:", parsed.scheme)
        print("Path:", parsed.path or "/")

        warnings = []

        if parsed.scheme == "http":
            warnings.append("Connection is not encrypted (HTTP).")
        if "@" in parsed.netloc:
            warnings.append("URL contains an @ symbol.")
        if host.startswith("xn--") or ".xn--" in host:
            warnings.append("Internationalized domain name detected.")
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
            warnings.append("URL uses an IP address instead of a domain.")
        if len(host) > 50:
            warnings.append("Unusually long hostname.")

        if warnings:
            for warning in warnings:
                print(Y + "[WARNING] " + warning)
        else:
            print(G + "No basic warning detected.")

        print(Y + "\nThis is a basic check, not a malware scan.")
    except ValueError:
        print(R + "Could not analyze URL.")

    pause()

def dns_lookup():
    clear()
    banner()
    host = input("Enter domain: ").strip()

    try:
        results = socket.getaddrinfo(host, None)
        addresses = sorted(set(item[4][0] for item in results))
        print(G + "\nDNS RESULTS")
        for address in addresses:
            print(address)
    except socket.gaierror:
        print(R + "DNS lookup failed.")
    except OSError as e:
        print(R + "Network error:", e)

    pause()

def public_ip():
    clear()
    banner()
    print(C + "Checking public IP...")
    try:
        request = urllib.request.Request(
            "https://api.ipify.org",
            headers={"User-Agent": "HASHASHIN/1.1"}
        )
        with urllib.request.urlopen(request, timeout=8) as response:
            ip = response.read().decode().strip()
        print(G + "\nPublic IP:", ip)
    except Exception:
        print(R + "Could not retrieve public IP.")
    pause()

def network_menu():
    while True:
        clear()
        banner()
        print(W + """
[1] DNS Lookup
[2] Public IP
[0] Back
""")
        choice = input(G + "HASHASHIN/NETWORK > " + RESET)

        if choice == "1":
            dns_lookup()
        elif choice == "2":
            public_ip()
        elif choice == "0":
            break
        else:
            print(R + "Invalid option")
            pause()

def cyber_menu():
    while True:
        clear()
        banner()
        print(W + """
[1] Password Generator
[2] Password Strength Checker
[3] Hash Generator
[4] Hash Identifier
[5] URL Analyzer
[0] Back
""")
        choice = input(G + "HASHASHIN/CYBER > " + RESET)

        if choice == "1":
            password_generator()
        elif choice == "2":
            password_checker()
        elif choice == "3":
            hash_generator()
        elif choice == "4":
            hash_identifier()
        elif choice == "5":
            url_analyzer()
        elif choice == "0":
            break
        else:
            print(R + "Invalid option")
            pause()


SCAN_REPORT = []

SUSPICIOUS_PATTERNS = [
    r"base64\.b64decode",
    r"exec\s*\(",
    r"eval\s*\(",
    r"subprocess\.(Popen|run|call)",
    r"os\.system\s*\(",
    r"powershell\s+-enc"
]

def scan_file(path):
    findings = []
    try:
        if not os.path.isfile(path):
            return ["File not found"]

        if os.path.getsize(path) > 5 * 1024 * 1024:
            return ["Skipped: file larger than 5 MB"]

        with open(path, "rb") as f:
            data = f.read()

        digest = hashlib.sha256(data).hexdigest()
        content = data.decode("utf-8", errors="ignore")

        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                findings.append("Suspicious code pattern: " + pattern)

        return findings, digest

    except OSError as e:
        return ["Read error: " + str(e)]

def scan_folder(folder):
    global SCAN_REPORT
    SCAN_REPORT = []
    count = 0

    print(C + "\nStarting HASHASHIN scan..." + RESET)

    for root, dirs, files in os.walk(folder, followlinks=False):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

        for name in files:
            path = os.path.join(root, name)

            if os.path.islink(path):
                continue

            count += 1
            if count > 5000:
                print(Y + "Scan limit reached (5000 files)." + RESET)
                break

            result = scan_file(path)

            if isinstance(result, tuple):
                findings, digest = result
                if findings:
                    SCAN_REPORT.append((path, findings, digest))
                    print(Y + "\n[REVIEW] " + path + RESET)
                    for item in findings:
                        print(R + " - " + item + RESET)
            else:
                SCAN_REPORT.append((path, result, ""))
                print(Y + "[SKIPPED] " + path + RESET)

        if count > 5000:
            break

    print(G + "\nScan completed.")
    print("Files checked:", count)
    print("Files requiring review:", len(SCAN_REPORT))
    print(Y + "This is a heuristic scanner, not a full antivirus." + RESET)
    pause()

def antivirus_menu():
    while True:
        clear()
        banner()
        print(W + """
       HASHASHIN ANTIVIRUS

[1] Quick Scan
[2] Full Scan
[3] Scan Single File
[4] File SHA256 Check
[5] Save Scan Report
[0] Back
""")
        choice = input(G + "HASHASHIN/ANTIVIRUS > " + RESET)

        if choice == "1":
            folder = os.path.expanduser("~/storage/shared/Download")
            if not os.path.isdir(folder):
                folder = os.getcwd()
            scan_folder(folder)

        elif choice == "2":
            folder = input("Folder path: ").strip()
            folder = os.path.expanduser(folder)
            if os.path.isdir(folder):
                scan_folder(folder)
            else:
                print(R + "Folder not found.")
                pause()

        elif choice == "3":
            path = os.path.expanduser(input("File path: ").strip())
            result = scan_file(path)
            if isinstance(result, tuple):
                findings, digest = result
                print(C + "\nSHA256:", digest)
                if findings:
                    for item in findings:
                        print(Y + "[REVIEW]", item)
                else:
                    print(G + "No known suspicious patterns found.")
            else:
                print(R + str(result))
            pause()

        elif choice == "4":
            path = os.path.expanduser(input("File path: ").strip())
            try:
                with open(path, "rb") as f:
                    digest = hashlib.sha256(f.read()).hexdigest()
                print(G + "\nSHA256:", digest)
            except OSError as e:
                print(R + str(e))
            pause()

        elif choice == "5":
            try:
                with open("scan_report.txt", "w", encoding="utf-8") as f:
                    f.write("HASHASHIN ANTIVIRUS REPORT\n")
                    f.write("=" * 35 + "\n")
                    for path, findings, digest in SCAN_REPORT:
                        f.write("\nFile: " + path + "\n")
                        f.write("SHA256: " + digest + "\n")
                        for item in findings:
                            f.write("Finding: " + item + "\n")
                print(G + "Report saved: scan_report.txt")
            except OSError as e:
                print(R + str(e))
            pause()

        elif choice == "0":
            break

        else:
            print(R + "Invalid option")
            pause()


def system_info():
    clear()
    banner()
    print(C + "SYSTEM INFORMATION\n")
    print(W + "Operating System:", platform.system())
    print("Platform:", platform.platform())
    print("Architecture:", platform.machine())
    print("Python Version:", sys.version.split()[0])
    print("Hostname:", socket.gethostname())
    pause()

def main():
    while True:
        clear()
        banner()
        print(W + """
[1] Cyber Security Tools
[2] Network Tools
[3] System Information
[4] HASHASHIN Antivirus
[0] Exit
""")
        choice = input(G + "root@hashashin:~# " + RESET)

        if choice == "1":
            cyber_menu()
        elif choice == "2":
            network_menu()
        elif choice == "3":
            system_info()
        elif choice == "4":
            antivirus_menu()
        elif choice == "0":
            print(G + "\nHASHASHIN SHUTDOWN")
            break
        else:
            print(R + "Invalid option")
            pause()

if __name__ == "__main__":
    main()
