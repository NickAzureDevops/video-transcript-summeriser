from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from dotenv import load_dotenv
import os
from datetime import datetime  # Add this import

load_dotenv()

PROJECT_ENDPOINT = os.environ.get("FOUNDRY_PROJECT_URL")
AGENT_NAME = os.environ.get("FOUNDRY_AGENT_NAME")
MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME")

project_client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())

agent = project_client.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_DEPLOYMENT_NAME,
        instructions=(
            "You are an expert assistant that summarizes video transcripts concisely and accurately for teams and YouTube videos.\n"
        ),
    ),
)
agents = list(project_client.agents.list())
for a in agents:
    print(f"- {a.name} (id: {getattr(a, 'id', 'N/A')})")

print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")