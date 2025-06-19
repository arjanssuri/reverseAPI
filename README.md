# reverseAPI

A service that automatically collects API documentation, processes it through AI, and provides it to your coding tools to make development faster and easier.

## 🚀 Quick Setup

```bash
# Get the code
git clone https://github.com/yourusername/reverseAPI.git
cd reverseAPI

# Install everything needed
pip install -r requirements.txt

# Install browser dependencies
playwright install

# Start the server
python server.py
```

## 📋 What This Service Does

reverseAPI automatically:
- Scrapes API documentation from any website using Firecrawl
- Extracts content in markdown and HTML formats
- Provides a simple REST API for scraping websites
- Uses browser automation to perform complex web tasks
- Returns structured data with metadata

## 🔗 Available Endpoints

**Server runs on:** `http://localhost:8000`

### **GET /** 
Health check - returns server status

### **GET /health**
Detailed health check with service information

### **GET /scrape**
Scrape any website and return content

**Parameters:**
- `url` (required) - Website URL to scrape
- `formats` (optional) - Output formats: `markdown`, `html` (default: `markdown`)

**Example Usage:**
```bash
# Basic scraping
curl "http://localhost:8000/scrape?url=docs.stripe.com/api"

# Multiple formats
curl "http://localhost:8000/scrape?url=platform.openai.com/docs&formats=markdown&formats=html"

# Any API documentation site
curl "http://localhost:8000/scrape?url=docs.github.com/en/rest"
```

### **GET /useragent**
Use browser automation to perform complex web tasks

**Parameters:**
- `task` (required) - Description of what you want the agent to do

**Example Usage:**
```bash
# Compare API pricing
curl "http://localhost:8000/useragent?task=Compare the price of gpt-4o and claude-3.5-sonnet"

# Find current information
curl "http://localhost:8000/useragent?task=Find the current price of Bitcoin in USD"

# Research tasks
curl "http://localhost:8000/useragent?task=Find the latest features in the OpenAI API documentation"
```

## 🧪 Testing

```bash
# Run automated tests
python test_server.py

# Or use pytest
pytest tests/
``` 