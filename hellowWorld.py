import sys
import os
import json
from typing import Any, Optional
try:
    import requests
except Exception:
    requests = None

#!/usr/bin/env python3
"""
using HTTP Basic auth. It reads credentials and endpoint from environment:
  OIC_ENDPOINT, OIC_USERNAME, OIC_PASSWORD
Use: python hellowWorld.py --invoke-oic '{"key": "value"}'
"""


def main(name: str = "world") -> None:
    print(f"Hello, {name}!")


def invoke_oic(endpoint: str, username: str, password: str, payload: Optional[Any] = None) -> Optional[Any]:
    """Invoke OIC integration endpoint using HTTP Basic auth and JSON payload.

    Returns the parsed JSON response when possible, otherwise prints response text.
    """
    if requests is None:
        print("The 'requests' package is required to invoke OIC. Install with: pip install requests")
        return None

    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(endpoint, auth=(username, password), json=payload, headers=headers, timeout=30)
        print(f"OIC request to {endpoint} returned status {resp.status_code}")
        try:
            data = resp.json()
            print(json.dumps(data, indent=2))
            return data
        except ValueError:
            print(resp.text)
            return resp.text
    except requests.RequestException as exc:
        print(f"Error invoking OIC: {exc}")
        return None

if __name__ == "__main__":
    # If user requested OIC invocation, use env creds and optional JSON payload
    if "--invoke-oic" in sys.argv:
        idx = sys.argv.index("--invoke-oic")
        endpoint = "https://ocimad-bk-oic3-test-axcqct04lren-vl.integration.eu-madrid-2.ocp.oraclecloud.eu/ic/api/integration/v1/flows/rest/AAS_INTG_TO_SFTP/1.0/"
        username = "ocioic_local_test"
        password = "AhczE44UyS70"

        if not (endpoint and username and password):
            print("Missing OIC credentials or endpoint. Set OIC_ENDPOINT, OIC_USERNAME, OIC_PASSWORD in environment.")
            sys.exit(2)

        payload = None
        # optional next arg can be a JSON string payload
        if len(sys.argv) > idx + 1:
            raw = sys.argv[idx + 1]
            try:
                payload = json.loads(raw)
            except ValueError:
                # not JSON, send as simple string
                payload = raw

        invoke_oic(endpoint, username, password, payload)
    elif len(sys.argv) > 1:
        main(" ".join(sys.argv[1:]))
    else:
        main()