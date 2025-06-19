import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients.firecrawl_client import FirecrawlClient


class TestFirecrawlClient:
    """Test the Firecrawl client with real API documentation."""
    
    @pytest.fixture
    def client(self):
        """Create a Firecrawl client for testing."""
        return FirecrawlClient(pretty_print=False)  # Disable pretty print for tests
    
    @pytest.fixture
    def client_with_pretty_print(self):
        """Create a Firecrawl client with pretty print enabled."""
        return FirecrawlClient(pretty_print=True)
    
    def test_client_initialization(self):
        """Test that the client initializes properly."""
        client = FirecrawlClient()
        assert client.app is not None
        assert hasattr(client, 'pretty_print')
    
    def test_missing_api_key(self, monkeypatch):
        """Test that client raises error when API key is missing."""
        monkeypatch.delenv('FIRECRAWL_API_KEY', raising=False)
        with pytest.raises(ValueError, match="FIRECRAWL_API_KEY required"):
            FirecrawlClient()
    
    @pytest.mark.integration
    def test_scrape_stripe_api_docs(self, client):
        """Test scraping Stripe API documentation."""
        url = "https://docs.stripe.com/api"
        result = client.scrape(url, formats=['markdown'])
        
        assert result is not None
        assert hasattr(result, 'markdown')
        assert result.markdown is not None
        assert len(result.markdown) > 0
        
        # Check for common API doc content
        markdown_content = result.markdown.lower()
        assert any(keyword in markdown_content for keyword in ['api', 'endpoint', 'curl', 'request'])
    
    @pytest.mark.integration  
    def test_scrape_openai_api_docs(self, client):
        """Test scraping OpenAI API documentation."""
        url = "https://platform.openai.com/docs/api-reference"
        result = client.scrape(url, formats=['markdown'])
        
        assert result is not None
        assert hasattr(result, 'markdown')
        assert result.markdown is not None
        assert len(result.markdown) > 0
        
        # Check for OpenAI specific content
        markdown_content = result.markdown.lower()
        assert any(keyword in markdown_content for keyword in ['openai', 'api', 'models', 'completions'])
    
    @pytest.mark.integration
    def test_scrape_github_api_docs(self, client):
        """Test scraping GitHub API documentation."""
        url = "https://docs.github.com/en/rest"
        result = client.scrape(url, formats=['markdown'])
        
        assert result is not None
        assert hasattr(result, 'markdown')
        assert result.markdown is not None
        assert len(result.markdown) > 0
        
        # Check for GitHub specific content
        markdown_content = result.markdown.lower()
        assert any(keyword in markdown_content for keyword in ['github', 'rest', 'api', 'repository'])
    
    @pytest.mark.integration
    def test_scrape_with_multiple_formats(self, client):
        """Test scraping with multiple formats."""
        url = "https://firecrawl.dev"
        result = client.scrape(url, formats=['markdown', 'html'])
        
        assert result is not None
        assert hasattr(result, 'markdown')
        assert hasattr(result, 'html')
        assert result.markdown is not None
        assert result.html is not None
        assert len(result.markdown) > 0
        assert len(result.html) > 0
    
    def test_pretty_print_functionality(self, client_with_pretty_print, capsys):
        """Test that pretty print functionality works."""
        assert client_with_pretty_print.pretty_print is True
    
    @pytest.mark.parametrize("api_doc_url,expected_keywords", [
        ("https://docs.stripe.com/api", ["stripe", "api", "payment"]),
        ("https://platform.openai.com/docs/api-reference", ["openai", "api", "models"]),
        ("https://docs.github.com/en/rest", ["github", "rest", "api"]),
    ])
    @pytest.mark.integration
    def test_multiple_api_docs(self, client, api_doc_url, expected_keywords):
        """Test scraping multiple different API documentation sites."""
        result = client.scrape(api_doc_url, formats=['markdown'])
        
        assert result is not None
        assert hasattr(result, 'markdown')
        assert result.markdown is not None
        
        markdown_content = result.markdown.lower()
        # At least one expected keyword should be present
        assert any(keyword in markdown_content for keyword in expected_keywords)
    
    @pytest.mark.integration
    def test_scrape_lightweight_docs(self, client):
        """Test scraping smaller, faster documentation pages."""
        lightweight_urls = [
            "https://httpbin.org/",
            "https://jsonplaceholder.typicode.com/",
        ]
        
        for url in lightweight_urls:
            result = client.scrape(url, formats=['markdown'])
            assert result is not None
            assert hasattr(result, 'markdown')
            assert result.markdown is not None
            assert len(result.markdown) > 0


if __name__ == "__main__":
    # Quick manual test
    print("🧪 Running manual Firecrawl tests...")
    
    try:
        client = FirecrawlClient(pretty_print=True)
        
        # Test with a simple API doc
        print("\n1. Testing with httpbin (simple API)...")
        result = client.scrape("https://httpbin.org/", formats=['markdown'])
        
        print("\n2. Testing with JSONPlaceholder...")
        result = client.scrape("https://jsonplaceholder.typicode.com/", formats=['markdown'])
        
        print("\n✅ Manual tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}") 