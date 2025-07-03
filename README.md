# Mediastack News MCP Server

A FastMCP server that exposes mediastack News API as MCP (Model Context Protocol) tools. This server can be used as a plug-and-play backend for Smithery.ai or any other MCP-compatible agent platform.

## Features

- **get_latest_news**: Fetch the most recent news stories with filtering options
- **get_sources**: List available news sources with filtering capabilities

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd mediastack-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### API Key Setup

The server comes with a built-in API key for development. For production use, you should use your own mediastack API key.

#### Option 1: Environment Variable
Set the `MEDIASTACK_API_KEY` environment variable:
```bash
export MEDIASTACK_API_KEY=your_api_key_here
```

#### Option 2: .env File
Create a `.env` file in the project root:
```
MEDIASTACK_API_KEY=your_api_key_here
```

Get your API key from [mediastack.com](https://mediastack.com/).

## Running Locally

Start the MCP server:
```bash
python server.py
```

The server will communicate via stdio (stdin/stdout) using the MCP protocol.

## Available Tools

### 1. get_latest_news

Fetches the most recent news stories from mediastack.

**Parameters:**
- `keywords` (optional): Search terms to filter news
- `countries` (optional): Two-letter country codes, comma-separated (e.g., "us,gb")
- `languages` (optional): Language codes, comma-separated (e.g., "en,fr")
- `categories` (optional): News categories - business, entertainment, general, health, science, sports, technology (comma-separated)
- `limit` (optional): Maximum number of results (default: 20, max: 100)

### 2. get_sources

Lists available news sources from mediastack.

**Parameters:**
- `search` (optional): Free-text search term to filter sources
- `countries` (optional): Two-letter country codes, comma-separated
- `languages` (optional): Language codes, comma-separated
- `categories` (optional): News categories (comma-separated)
- `limit` (optional): Maximum number of results (default: 20, max: 100)

## MCP Protocol Usage

MCP servers communicate using JSON-RPC over stdio. To interact with the server programmatically, you need an MCP client. Here's how different platforms use it:

### Using with Claude Desktop

Add to your Claude Desktop configuration:
```json
{
  "mcpServers": {
    "mediastack-news": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

### Using with Smithery.ai

The `smithery.yaml` file is already configured for deployment. Smithery handles the MCP communication automatically.

### Using with MCP Clients

For testing, you can use the `mcp` CLI tool:
```bash
# Install mcp CLI
npm install -g @modelcontextprotocol/cli

# Test the server
mcp test python server.py
```

## Deployment on Smithery.ai

1. Push this repository to GitHub
2. Connect your GitHub repository to Smithery.ai
3. Smithery will automatically detect the `smithery.yaml` configuration
4. Set your `MEDIASTACK_API_KEY` in Smithery's environment variables (optional)
5. Deploy and start using the MCP tools

## Error Handling

The server includes comprehensive error handling:
- Network errors are caught and returned with descriptive messages
- Mediastack API errors are parsed and forwarded with error codes
- Invalid parameters are validated before making API calls

## Development

### Project Structure
```
.
├── app.py           # MCP tool definitions
├── server.py        # FastMCP server setup
├── requirements.txt # Python dependencies
├── smithery.yaml    # Smithery deployment config
├── .env.example     # Example environment variables
└── README.md        # This file
```

### Testing

To test the MCP server locally:

1. Install the MCP CLI:
```bash
npm install -g @modelcontextprotocol/cli
```

2. Test the server:
```bash
mcp test python server.py
```

3. List available tools:
```bash
echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}' | python server.py
```

## Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://modelcontextprotocol.io/)
- [mediastack API Documentation](https://mediastack.com/documentation)
- [Smithery.ai Documentation](https://smithery.ai/docs)

## License

This project is provided as-is for use with mediastack API and MCP-compatible platforms. 