import json
import hmac
import hashlib
import os
from datetime import datetime, timezone

import requests

payload = {
    "action_run_link": os.environ["ACTION_RUN_LINK"],
    "email": os.environ["EMAIL"],
    "name": os.environ["NAME"],
    "repository_link": os.environ["REPOSITORY_LINK"],
    "resume_link": os.environ["RESUME_LINK"],
    "timestamp": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
}

body = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
)

secret = "hello-there-from-b12"

signature = hmac.new(
    secret.encode("utf-8"),
    body.encode("utf-8"),
    hashlib.sha256,
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

print("Sending payload:")
print(body)

response = requests.post(
    "https://b12.io/apply/submission",
    data=body.encode("utf-8"),
    headers=headers,
    timeout=30,
)

print("Status Code:", response.status_code)
print("Response Text:", response.text)

response.raise_for_status()

try:
    result = response.json()
    print("Receipt:", result.get("receipt"))
except Exception as e:
    print("Failed to parse JSON:", e)