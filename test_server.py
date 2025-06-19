#!/usr/bin/env python3

import requests
import json
import time

def test_server():
    """Test the FastAPI server endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing reverseAPI Server...")
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running! Start with: python server.py")
        return
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    response = requests.get(f"{base_url}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 3: Scrape a simple website
    print("\n3. Testing scrape endpoint with httpbin...")
    response = requests.get(f"{base_url}/scrape", params={
        "url": "httpbin.org",
        "formats": ["markdown"]
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"URL: {data['url']}")
        print(f"Markdown length: {data.get('markdown_length', 0)} chars")
        print(f"Preview: {data.get('markdown', '')[:200]}...")
    else:
        print(f"Error: {response.text}")
    
    # Test 4: Scrape with multiple formats
    print("\n4. Testing scrape with multiple formats...")
    response = requests.get(f"{base_url}/scrape", params={
        "url": "https://jsonplaceholder.typicode.com/",
        "formats": ["markdown", "html"]
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Formats: {data['formats_requested']}")
        print(f"Markdown: {data.get('markdown_length', 0)} chars")
        print(f"HTML: {data.get('html_length', 0)} chars")
    else:
        print(f"Error: {response.text}")
    
    # Test 5: Error handling - invalid URL
    print("\n5. Testing error handling...")
    response = requests.get(f"{base_url}/scrape", params={
        "url": "not-a-valid-url"
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n✅ Server tests completed!")

if __name__ == "__main__":
    test_server() 