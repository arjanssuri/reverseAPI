import os
import json
from firecrawl import FirecrawlApp


class FirecrawlClient:
    def __init__(self, pretty_print=True):
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY required")
        self.app = FirecrawlApp(api_key=api_key)
        self.pretty_print = pretty_print
    
    def scrape(self, url: str, formats=['markdown']):
        result = self.app.scrape_url(url, formats=formats)
        if self.pretty_print:
            self._pretty_print_result(result, url)
        return result
    
    def _pretty_print_result(self, result, url):
        print(f"\n🔥 Firecrawl Result for: {url}")
        print("=" * 60)
        
        # Handle ScrapeResponse object
        if hasattr(result, 'markdown') and result.markdown:
            markdown_content = result.markdown
            preview = markdown_content[:500] + "..." if len(markdown_content) > 500 else markdown_content
            print(f"📄 Markdown Content ({len(markdown_content)} chars):")
            print(preview)
            print("\n" + "-" * 40)
        
        if hasattr(result, 'html') and result.html:
            html_content = result.html
            preview = html_content[:300] + "..." if len(html_content) > 300 else html_content
            print(f"🌐 HTML Content ({len(html_content)} chars):")
            print(preview)
            print("\n" + "-" * 40)
        
        if hasattr(result, 'metadata') and result.metadata:
            print("📊 Metadata:")
            if hasattr(result.metadata, '__dict__'):
                print(json.dumps(result.metadata.__dict__, indent=2))
            else:
                print(result.metadata)
        
        print("=" * 60)


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