```python id="tb3e1s"
import json
from google.cloud import pubsub_v1

import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "PROJECT_ID"
SUBSCRIPTION_ID = "guardian-audit-sub"
LOCATION = "us-central1"

# ==========================================
# INIT VERTEX
# ==========================================

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION
)

model = GenerativeModel(
    "claude-3-5-sonnet@20240620"
)

# ==========================================
# PUBSUB
# ==========================================

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(
    PROJECT_ID,
    SUBSCRIPTION_ID
)

# ==========================================
# CALLBACK
# ==========================================

def callback(message):

    event = json.loads(
        message.data.decode("utf-8")
    )

    prompt = f"""
    You are the MCP Guardian Agent.

    Analyze this MCP audit event.

    Determine:
    1. suspicious behavior
    2. trust boundary concerns
    3. policy violations
    4. operational risk level

    Event:
    {json.dumps(event, indent=2)}

    Keep response concise.
    """

    response = model.generate_content(prompt)

    print("\n=== MCP GUARDIAN ANALYSIS ===\n")
    print(response.text)
    print("\n=============================\n")

    message.ack()

# ==========================================
# START SUBSCRIBER
# ==========================================

streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback
)

print(
    f"Listening on {subscription_path}"
)

streaming_pull_future.result()
```
