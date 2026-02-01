import azure.functions as func
from azure.functions import AsgiMiddleware

# Import your FastAPI MCP app from the main project
from servers.server import app

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
