# reverseAPI

A service that automatically collects API documentation, processes it through AI, and provides it to your coding tools to make development faster and easier.

## 🚀 Quick Setup

```bash
# Get the code
git clone https://github.com/yourusername/reverseAPI.git
cd reverseAPI

# Install everything needed
pip install -r requirements.txt

# Start the server
python server.py
```

## 📋 What This Service Does

reverseAPI automatically:
- Scrapes API documentation from any website using Firecrawl
- Extracts content in markdown and HTML formats
- Provides a simple REST API for scraping websites
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

## 🧪 Testing

```bash
# Run automated tests
python test_server.py

# Or use pytest
pytest tests/
``` 