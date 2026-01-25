from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ENDPOINT = os.environ.get("FOUNDRY_PROJECT_URL")
AGENT_NAME = os.environ.get("FOUNDRY_AGENT_NAME")
MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME")

project_client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai_client = project_client.get_openai_client()

agent = project_client.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_DEPLOYMENT_NAME,
        instructions="You're an expert assistant that summarizes video transcripts concisely and accurately for teams and YouTube videos.",
    ),
)
print(f"\nAgent ready: {agent.name} v{agent.version}")

conversation = openai_client.conversations.create()
print(f"Conversation created: {conversation.id}\n")