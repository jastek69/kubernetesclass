```python id="yb3e07"
import json
from google.cloud import pubsub_v1
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "PROJECT_ID"
SUBSCRIPTION_ID = "mcp-audit-sub"
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
# PROCESS EVENTS
# ==========================================

def callback(message):

    event = json.loads(
        message.data.decode("utf-8")
    )

    prompt = f"""
    You are an AI security oversight agent.

    Analyze this MCP audit event.

    Identify:
    1. suspicious behavior
    2. operational risk
    3. policy concerns
    4. recommended next step

    Event:
    {json.dumps(event, indent=2)}

    Keep response concise.
    """

    response = model.generate_content(prompt)

    print("\n=== MCP OBSERVER SUMMARY ===\n")
    print(response.text)
    print("\n============================\n")

    message.ack()

# ==========================================
# START LISTENER
# ==========================================

streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback
)

print(
    f"Listening for messages on "
    f"{subscription_path}"
)

streaming_pull_future.result()
```
