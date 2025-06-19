import os
from firecrawl import FirecrawlApp


class FirecrawlClient:
    def __init__(self):
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY required")
        self.app = FirecrawlApp(api_key=api_key)
    
    def scrape(self, url: str, formats=['markdown']):
        return self.app.scrape_url(url, formats=formats)


# Example usage for testing
if __name__ == "__main__":
    client = FirecrawlClient()
    
    # Test scraping a single page
    result = client.scrape('https://firecrawl.dev', formats=['markdown', 'html'])
    print("Single page scrape result:")
    print(result)
    
    # Test API docs scraping
    api_result = client.scrape('https://docs.stripe.com/api', formats=['markdown'])
    print("\nAPI docs scrape result:")
    print(api_result) 