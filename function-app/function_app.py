import azure.functions as func
import logging
import json

from servers.tools import search_episodes, list_recent_episodes

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="tools/search", methods=["POST"])
async def search(req: func.HttpRequest) -> func.HttpResponse:
    """Search podcast episodes by keyword."""
    logging.info("MCP Tool: search_episodes")
    
    try:
        body = req.get_json()
        query = body.get("query", "")
        limit = body.get("limit", 5)
        
        result = await search_episodes(query, limit)
        return func.HttpResponse(result, mimetype="application/json")
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="tools/recent", methods=["GET"])
async def recent(req: func.HttpRequest) -> func.HttpResponse:
    """Get recent podcast episodes."""
    logging.info("MCP Tool: list_recent_episodes")
    
    try:
        count = int(req.params.get("count", 5))
        result = await list_recent_episodes(count)
        return func.HttpResponse(result, mimetype="application/json")
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint."""
    return func.HttpResponse(
        json.dumps({"status": "healthy", "service": "podcast-mcp-server"}),
        mimetype="application/json"
    )
