import requests
import json
import time
from typing import List, Dict
from bs4 import BeautifulSoup
import re

def search_with_serper(query: str, api_key: str, search_type: str) -> Dict:
    """
    Use Serper API to search for a query
    search_type: 'buy' for shopping results, 'review' for review results
    """
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    if search_type == 'buy':
        payload = {
            'q': f"{query} buy amazon",
            'num': 3,
            'search_type': 'shopping'
        }
    else:
        payload = {
            'q': f"{query} espresso machine expert review",
            'num': 3
        }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error searching for {query}: {str(e)}")
        return None

def extract_product_names(file_path: str) -> List[str]:
    """
    Extract product names from the parsed results file
    """
    products = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line in lines:
                if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                    product_name = line.split('.', 1)[1].strip()
                    products.append(product_name)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
    
    return products

def get_review_content(url: str) -> str:
    """
    Extract review content from the webpage
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text(separator=' ', strip=True)
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Limit text length
        return text[:5000]  # Limit to first 5000 characters
        
    except Exception as e:
        print(f"Error extracting review from {url}: {str(e)}")
        return ""

def save_search_results(results: List[Dict], output_file: str):
    """
    Save search results to a JSON file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

def main():
    # Configuration
    API_KEY = "87821b459158327ffe7e3dacda3cc9272039e8c4"
    INPUT_FILE = "/Users/yangliuxin/ai-chatbot/recommendations.txt"
    OUTPUT_FILE = "product_reviews.json"
    
    # Extract product names
    products = extract_product_names(INPUT_FILE)
    print(f"Found {len(products)} products to search")
    
    # Search for each product
    all_results = []
    for product in products:
        print(f"\nProcessing: {product}")
        product_data = {
            'name': product,
            'buy_links': [],
            'reviews': []
        }
        
        # Get shopping results
        buy_results = search_with_serper(product, API_KEY, 'buy')
        if buy_results and 'shopping' in buy_results:
            for item in buy_results['shopping'][:3]:
                product_data['buy_links'].append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'price': item.get('price', '')
                })
        
        # Get review results
        review_results = search_with_serper(product, API_KEY, 'review')
        if review_results and 'organic' in review_results:
            for item in review_results['organic'][:3]:
                review_url = item.get('link', '')
                if review_url:
                    review_content = get_review_content(review_url)
                    product_data['reviews'].append({
                        'title': item.get('title', ''),
                        'link': review_url,
                        'snippet': item.get('snippet', ''),
                        'content': review_content
                    })
        
        all_results.append(product_data)
        time.sleep(2)  # Delay between products
    
    # Save results
    save_search_results(all_results, OUTPUT_FILE)
    print("\nAll done! Check product_reviews.json for results")

if __name__ == "__main__":
    main()