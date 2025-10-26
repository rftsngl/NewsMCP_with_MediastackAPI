# Mediastack News MCP Server
[![smithery badge](https://smithery.ai/badge/@rftsngl/newsmcp_mediastackapi)](https://smithery.ai/server/@rftsngl/newsmcp_mediastackapi)

A FastMCP server that exposes the Mediastack News API as MCP (Model Context Protocol) tools. This server can be used as a plug-and-play backend for Smithery.ai or any other MCP-compatible agent platform.

## ✨ Features

- **`get_latest_news`**: Fetches the most recent news stories with various filtering options.
- **`get_sources`**: Lists available news sources with filtering capabilities.

## 🚀 Installation

### Installing via Smithery

To install Mediastack News automatically via [Smithery](https://smithery.ai/server/@rftsngl/newsmcp_mediastackapi):

```bash
npx -y @smithery/cli install @rftsngl/newsmcp_mediastackapi
```

### Manual Installation
1.  Clone this repository:
    ```bash
    git clone <repository-url>
    cd NewsMCP_with_MediastackAPI
    ```

2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

This server requires a Mediastack API key to function.

1.  Get a free API key from [mediastack.com](https://mediastack.com/).
2.  Create a file named `.env` in the project's root directory.
3.  Add your API key to this file in the following format:
    ```
    MEDIASTACK_API_KEY=your_api_key_here
    ```

The server will automatically load this environment variable when a tool is called.

## 💻 Running Locally

To start the MCP server, run the following command:
```bash
python server.py
```
By default, the server will start on `http://0.0.0.0:8080`.

## 🛠️ Available Tools

### 1. `get_latest_news`

Fetches the most recent news stories from Mediastack.

**Parameters:**
- `keywords` (Optional): Search terms to filter news.
- `sources` (Optional): News sources, comma-separated (e.g., "cnn,bbc").
- `countries` (Optional): Country codes, comma-separated (e.g., "us,gb").
- `languages` (Optional): Language codes, comma-separated (e.g., "en,fr").
- `categories` (Optional): News categories, comma-separated.
- `date` (Optional): A specific date or date range (YYYY-MM-DD).
- `sort` (Optional): Sort order (`published_desc`, `published_asc`, `popularity`).
- `limit` (Optional): Maximum number of results to return (default: 25, max: 100).
- `offset` (Optional): Pagination offset.

### 2. `get_sources`

Lists available news sources from Mediastack.

**Parameters:**
- `search` (Optional): A search term to filter sources.
- `sources` (Optional): Specific sources, comma-separated.
- `countries` (Optional): Country codes, comma-separated.
- `languages` (Optional): Language codes, comma-separated.
- `categories` (Optional): News categories, comma-separated.
- `limit` (Optional): Maximum number of results to return (default: 25, max: 100).
- `offset` (Optional): Pagination offset.

## ☁️ Deployment on Smithery.ai

1.  Push this repository to GitHub.
2.  Connect your GitHub repository to Smithery.ai.
3.  Smithery will automatically detect the `smithery.yaml` configuration.
4.  Set your `MEDIASTACK_API_KEY` in Smithery's environment variables.
5.  Deploy and start using the MCP tools.

For more information, visit the [Smithery.ai Documentation](https://smithery.ai/docs).

## 📂 Project Structure
```
.
├── app.py           # MCP tool definitions
├── server.py        # FastMCP server setup
├── requirements.txt # Python dependencies
├── smithery.yaml    # Smithery deployment configuration
├── Dockerfile       # Instructions for building a Docker image
├── LICENSE          # Project license
├── .env             # (Local) Environment variables
└── README.md        # This file
```

## 📄 License

This project is licensed under the [MIT License](LICENSE). 
