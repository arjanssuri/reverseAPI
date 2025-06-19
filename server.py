from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import uvicorn
from clients.firecrawl_client import FirecrawlClient

app = FastAPI(
    title="reverseAPI Scraper",
    description="API documentation scraping service using Firecrawl",
    version="1.0.0"
)

# Initialize Firecrawl client
try:
    firecrawl_client = FirecrawlClient(pretty_print=False)
except ValueError as e:
    print(f"❌ Failed to initialize Firecrawl client: {e}")
    firecrawl_client = None

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "reverseAPI Scraper is running!", "status": "healthy"}

@app.get("/scrape")
async def scrape_website(
    url: str = Query(..., description="The website URL to scrape"),
    formats: List[str] = Query(default=["markdown"], description="Output formats (markdown, html)")
):
    """
    Scrape a website and return the content in specified formats.
    
    - **url**: The website URL to scrape (required)
    - **formats**: List of output formats (default: ["markdown"])
    """
    if not firecrawl_client:
        raise HTTPException(
            status_code=500, 
            detail="Firecrawl client not initialized. Check FIRECRAWL_API_KEY environment variable."
        )
    
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        result = firecrawl_client.scrape(url, formats=formats)
        
        # Convert ScrapeResponse to dictionary for JSON response
        response_data = {
            "url": url,
            "formats_requested": formats,
            "success": True
        }
        
        if hasattr(result, 'markdown') and result.markdown:
            response_data["markdown"] = result.markdown
            response_data["markdown_length"] = len(result.markdown)
        
        if hasattr(result, 'html') and result.html:
            response_data["html"] = result.html
            response_data["html_length"] = len(result.html)
        
        if hasattr(result, 'metadata') and result.metadata:
            # Convert metadata to dict if it's an object
            if hasattr(result.metadata, '__dict__'):
                response_data["metadata"] = result.metadata.__dict__
            else:
                response_data["metadata"] = result.metadata
        
        return response_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to scrape website: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Detailed health check with service status."""
    return {
        "status": "healthy",
        "firecrawl_client": "initialized" if firecrawl_client else "not initialized",
        "service": "reverseAPI Scraper"
    }

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 