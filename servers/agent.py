from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from dotenv import load_dotenv
import os

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_URL"],
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()

transcript_mcp_tool = MCPTool(
    server_label="transcript-mcp",
    server_url=os.environ["MCP_SERVER_URL"],
    require_approval="never",
    allowed_tools=["summarize", "search", "action_items", "generic_prompt"],
    headers={"x-functions-key": os.environ["MCP_FUNCTION_KEY"]},
)
tools = [
    transcript_mcp_tool,
]

# Create the agent with the tools list
agent = project_client.agents.create_version(
    agent_name=os.environ["FOUNDRY_AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions="You are an expert assistant that summarizes and analyzes transcripts using advanced tools.",
        tools=tools,
    ),
)

print(f"Agent ready: {agent.name} v{agent.version}")