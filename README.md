# reverseAPI

A service that automatically collects API documentation, processes it through AI, and provides it to your coding tools to make development faster and easier.

## 🚀 Quick Setup

```bash
# Get the code
git clone https://github.com/yourusername/reverseAPI.git
cd reverseAPI

# Install everything needed
pip install -r requirements.txt
```

## 📋 What This Service Does

reverseAPI automatically:
- Finds and reads API documentation from websites
- Understands what each API does using AI  
- Organizes all the information in a smart way
- Gives your coding tools instant access to API info
- Can even create API keys for you automatically

## 🔗 Available Endpoints

### **Data Collection**
- `POST /sources` - Add API documentation source
- `GET /sources` - Get all data sources
- `DELETE /sources/{id}` - Remove data source
- `POST /sources/{id}/refresh` - Refresh data source

### **API Information Search**
- `GET /search` - Search APIs
- `GET /apis/{id}` - Get API details
- `GET /apis/{id}/similar` - Find similar APIs
- `GET /apis/{id}/examples` - Get code examples

### **Smart API Key Management**
- `POST /keys` - Create API key
- `GET /keys` - List API keys
- `GET /keys/{id}/status` - Check key status
- `POST /keys/{id}/rotate` - Rotate API key

### **Integration with Your Tools**
- `POST /integrations/ide` - Connect to IDE
- `GET /suggestions` - Get contextual suggestions
- `POST /generate/client` - Generate API client code
- `POST /validate` - Validate API usage

### **Data Management**
- `GET /status` - Get processing status
- `GET /export` - Export API catalog
- `POST /import` - Import API data
- `DELETE /cache` - Clear cache

### **Analytics & Insights**
- `GET /analytics/usage` - Usage statistics
- `GET /analytics/costs` - Cost tracking
- `GET /analytics/performance` - Performance metrics
- `GET /analytics/trends` - Trend analysis

### **System Management**
- `GET /health` - Health check
- `PUT /config` - Update configuration
- `GET /logs` - View logs
- `POST /backup` - Backup data 