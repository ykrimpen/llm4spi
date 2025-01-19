import vertexai
import openai

from google.auth import default, transport

# TODO(developer): Update and un-comment below line
# PROJECT_ID = "your-project-id"
location = "us-central1"
PROJECT_ID = "openai-llm-meta"
vertexai.init(project=PROJECT_ID, location=location)

# Programmatically get an access token
credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
auth_request = transport.requests.Request()
credentials.refresh(auth_request)

# # OpenAI Client
client = openai.OpenAI(
    base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
    api_key=credentials.token,
)

response = client.chat.completions.create(
    model="google/gemini-1.5-flash-002",
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
)

print(response.choices[0].message.content)
# Example response:
# The sky is blue due to a phenomenon called **Rayleigh scattering**.
# Sunlight is made up of all the colors of the rainbow.
# As sunlight enters the Earth's atmosphere ...