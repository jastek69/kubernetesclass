import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "PROJECT_ID"
LOCATION = "us-central1"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION
)

model = GenerativeModel("gemini-1.5-flash")

prompt = """
Summarize this security finding:

Falco detected a shell spawned inside
a Kubernetes container in namespace app01.
"""

response = model.generate_content(prompt)

print(response.text)
