import re
import json
from pathlib import Path

def load_response_from_file(file_path: str) -> dict:
    """
    Load API response from text file and convert to Python dictionary
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            response_text = f.read()
            
        # Extract key information
        content_match = re.search(r'content="(.*?)", refusal=', response_text, re.DOTALL)
        content = content_match.group(1) if content_match else ""
        
        # Extract citations
        citations_match = re.search(r'citations=\[(.*?)\]', response_text)
        citations_text = citations_match.group(1) if citations_match else ""
        citations = [url.strip("'") for url in citations_text.split(', ')] if citations_text else []
        
        # Extract usage information
        usage_match = re.search(r'usage=CompletionUsage\(completion_tokens=(\d+), prompt_tokens=(\d+), total_tokens=(\d+)', response_text)
        usage = {
            'completion_tokens': int(usage_match.group(1)) if usage_match else 0,
            'prompt_tokens': int(usage_match.group(2)) if usage_match else 0,
            'total_tokens': int(usage_match.group(3)) if usage_match else 0
        }
        
        return {
            'success': True,
            'choices': [{
                'message': {
                    'content': content.replace('\\n', '\n')  # Fix newline characters
                }
            }],
            'citations': citations,
            'usage': usage
        }
            
    except Exception as e:
        print(f"Failed to load file: {str(e)}")
        print(f"Error type: {type(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def parse_perplexity_response(response_data):
    """
    Parse response data from Perplexity API
    """
    try:
        content = response_data['choices'][0]['message']['content']
        
        # Parse product recommendations
        products = []
        current_product = None
        description_buffer = []
        
        # Split content into lines and process each line
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Product header detection
            if line.startswith('## '):
                # Save previous product if exists
                if current_product is not None:
                    if description_buffer:
                        current_product['description'] = ' '.join(description_buffer)
                    products.append(current_product)
                
                # Start new product
                current_product = {
                    'name': line[3:].strip(),
                    'description': '',
                    'features': [],
                    'retailers': [],
                    'purchase_links': []
                }
                description_buffer = []
                
            # Feature or description detection
            elif line.startswith('- '):
                if '**Available at:**' in line:
                    retailers = line.replace('- **Available at:**', '').strip()
                    if current_product:
                        current_product['retailers'] = [r.strip() for r in retailers.split(',')]
                else:
                    if current_product:
                        description_buffer.append(line[2:].strip())
            
            # Purchase link detection
            elif '[' in line and '](' in line and ')' in line and current_product:
                matches = re.findall(r'\[(.*?)\]\((.*?)\)', line)
                for name, url in matches:
                    current_product['purchase_links'].append({
                        'name': name,
                        'url': url
                    })
            
            i += 1
        
        # Add the last product
        if current_product is not None:
            if description_buffer:
                current_product['description'] = ' '.join(description_buffer)
            products.append(current_product)
            
        return {
            'success': True,
            'products': products,
            'citations': response_data.get('citations', []),
            'usage': response_data.get('usage', {})
        }
        
    except Exception as e:
        print(f"Parsing error: {str(e)}")  # Add debug print
        return {
            'success': False,
            'error': str(e)
        }

def save_parsed_results(parsed_data, output_file="parsed_results.txt"):
    """
    Save the parsed results to a text file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Parsing Results ===\n\n")
            f.write(f"Found {len(parsed_data['products'])} product recommendations:\n")
            
            for i, product in enumerate(parsed_data['products'], 1):
                f.write(f"\n{i}. {product['name']}\n")
                f.write(f"Description: {product['description']}\n")
                if product['retailers']:
                    f.write(f"Available at: {', '.join(product['retailers'])}\n")
                if product['purchase_links']:
                    f.write("Purchase Links:\n")
                    for link in product['purchase_links']:
                        f.write(f"  - {link['name']}: {link['url']}\n")
            
            f.write(f"\nCitations: {len(parsed_data['citations'])} sources\n")
            for citation in parsed_data['citations']:
                f.write(f"  - {citation}\n")
            
            f.write(f"\nToken Usage:\n")
            f.write(f"  Completion tokens: {parsed_data['usage']['completion_tokens']}\n")
            f.write(f"  Prompt tokens: {parsed_data['usage']['prompt_tokens']}\n")
            f.write(f"  Total tokens: {parsed_data['usage']['total_tokens']}\n")
            
        print(f"Results have been saved to {output_file}")
        
    except Exception as e:
        print(f"Error saving results: {str(e)}")

# Usage example
response_file = "/Users/yangliuxin/ai-chatbot/response_regular.txt"
api_response_dict = load_response_from_file(response_file)

if api_response_dict['success']:
    parsed_data = parse_perplexity_response(api_response_dict)
    
    if parsed_data['success']:
        # Save results to file
        save_parsed_results(parsed_data, "recommendations.txt")