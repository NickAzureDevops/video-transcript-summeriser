from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from dotenv import load_dotenv
import os

load_dotenv()

# These will read from .env if present
PROJECT_ENDPOINT = os.environ.get("FOUNDRY_PROJECT_URL")
AGENT_NAME = os.environ.get("FOUNDRY_AGENT_NAME")
FOUNDRY_MODEL_DEPLOYMENT_NAME = os.environ.get("FOUNDRY_MODEL_DEPLOYMENT_NAME")

project_client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai_client = project_client.get_openai_client()

try:
    agent = project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=FOUNDRY_MODEL_DEPLOYMENT_NAME,
            instructions="You are a transcript summarization assistant. Use MCP tools to answer questions.",
            tools=[],
        ),
    )
    print(f"\nAgent ready: {agent.name} v{agent.version}")
except Exception as e:
    print(f"Error creating agent: {e}")
    exit(1)

try:
    conversation = openai_client.conversations.create()
    print(f"Conversation created: {conversation.id}\n")
except Exception as e:
    print(f"Error creating conversation: {e}")
    exit(1)

print("Type your question below. Type 'exit' or 'quit' to end the session.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ("exit", "quit"):
        print("Exiting chat loop.")
        break
    try:
        response = openai_client.responses.create(
            conversation=conversation.id,
            input=user_input,
            extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
        )
        print(f"Agent: {response.output_text}\n{'-'*40}")
    except Exception as e:
        print(f"Error during response: {e}")
