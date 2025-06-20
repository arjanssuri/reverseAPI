from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import uvicorn
import asyncio
from clients.firecrawl_client import FirecrawlClient

# Browser agent imports
from browser_use import Agent
from langchain_anthropic import ChatAnthropic

app = FastAPI(
    title="reverseAPI Scraper",
    description="API documentation scraping service using Firecrawl and Browser Agent",
    version="1.0.0"
)

# Initialize Firecrawl client
try:
    firecrawl_client = FirecrawlClient(pretty_print=False)
except ValueError as e:
    print(f"❌ Failed to initialize Firecrawl client: {e}")
    firecrawl_client = None

# Initialize Browser Agent LLM
try:
    browser_llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0,
        max_tokens=1024,
        timeout=None,
        max_retries=2,
    )
    print("✅ Browser agent LLM initialized")
except Exception as e:
    print(f"❌ Failed to initialize browser agent LLM: {e}")
    browser_llm = None

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

@app.get("/useragent")
async def use_browser_agent(
    task: str = Query(..., description="The task for the browser agent to perform")
):
    """
    Use the browser agent to perform a task using web automation.
    
    - **task**: Description of what you want the agent to do (required)
    """
    if not browser_llm:
        raise HTTPException(
            status_code=500, 
            detail="Browser agent not initialized. Check ANTHROPIC_API_KEY environment variable."
        )
    
    if not task:
        raise HTTPException(status_code=400, detail="Task parameter is required")
    
    try:
        # Create and run the browser agent
        agent = Agent(
            task=task,
            llm=browser_llm,
        )
        
        # Run the agent task
        result = await agent.run()
        
        # Extract information from AgentHistoryList
        final_result = "No result extracted"
        steps_completed = 0
        is_successful = False
        
        # Try to get extracted content (it's a method, not a property)
        try:
            if hasattr(result, 'extracted_content') and callable(result.extracted_content):
                extracted = result.extracted_content()
                if isinstance(extracted, list) and extracted:
                    final_result = extracted[-1]  # Get the last/final result
                elif extracted:
                    final_result = str(extracted)
            elif hasattr(result, 'extracted_content'):
                final_result = str(result.extracted_content)
        except Exception as e:
            print(f"Debug - Error calling extracted_content: {e}")
        
        # Try to get from all_results if available
        if (final_result == "No result extracted" or not final_result) and hasattr(result, 'all_results'):
            for action_result in reversed(result.all_results):
                if (hasattr(action_result, 'is_done') and action_result.is_done and 
                    hasattr(action_result, 'success') and action_result.success and
                    hasattr(action_result, 'extracted_content') and action_result.extracted_content):
                    final_result = action_result.extracted_content
                    is_successful = True
                    break
        
        # Try to get from all_model_outputs
        if (final_result == "No result extracted" or not final_result) and hasattr(result, 'all_model_outputs'):
            for output in reversed(result.all_model_outputs):
                if isinstance(output, dict) and 'done' in output and 'text' in output['done']:
                    final_result = output['done']['text']
                    is_successful = output['done'].get('success', True)
                    break
        
        # Get steps completed and check overall success
        if hasattr(result, 'all_results'):
            steps_completed = len(result.all_results)
            # Check if any step was successful
            for action_result in result.all_results:
                if hasattr(action_result, 'success') and action_result.success:
                    is_successful = True
                    break
        
        response_data = {
            "task": task,
            "success": is_successful,
            "result": final_result,
            "steps_completed": steps_completed
        }
        
        return response_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to complete browser agent task: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Detailed health check with service status."""
    return {
        "status": "healthy",
        "firecrawl_client": "initialized" if firecrawl_client else "not initialized",
        "browser_agent": "initialized" if browser_llm else "not initialized",
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