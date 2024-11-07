import requests
from bs4 import BeautifulSoup
import hashlib
import json
import random
import nltk
from nltk.tokenize import sent_tokenize
from typing import List, Dict, Any

# Ensure NLTK resources are downloaded for sentence tokenization
nltk.download("punkt")

def get_useragent():
    _useragent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
    ]
    return random.choice(_useragent_list)

def google_search(query):
    links = []
    try:
        headers = {"User-Agent": get_useragent()}
        params = {"q": f'"{query}"', "num": 3, "hl": 'en'}
        
        # Perform the Google search request
        response = requests.get("https://www.google.com/search", headers=headers, params=params, timeout=5)
        response.raise_for_status()  # Raises an error for bad responses
        
        # Parse the response content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract URLs from the search result blocks (avoiding ads, etc.)
                
        try:
            for result in soup.find_all('h3'):
                link = result.find_parent('a')
                if link:
                    link_text = link.get('href')
                    links.append(link_text)
        except:
            for link_tag in soup.select('div.yuRUbf a'):
                link = link_tag.get('href')
                if link:
                    links.append(link)


    except requests.RequestException as e:
        print(f"Error during the search request: {e}")
    
    return links

def fetch_web_content(url: str) -> str:
    """Fetch and clean the main content of a webpage."""
    try:
        headers = {"User-Agent": get_useragent()}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join([para.get_text() for para in paragraphs])
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return ""

def get_shingles(text: str, k: int = 5) -> set:
    """Generate k-shingles (sets of k consecutive words) for a given text."""
    words = text.split()
    shingles = set()
    for i in range(len(words) - k + 1):
        shingle = " ".join(words[i:i + k])
        shingle_hash = hashlib.md5(shingle.encode("utf-8")).hexdigest()
        shingles.add(shingle_hash)
    return shingles

def similarity1(set1, set2):
    intersection = len(set1.intersection(set2))
    return  (intersection / len(set1))*100

def calculate_jaccard_similarity(shingles1: set, shingles2: set) -> float:
    """Calculate Jaccard similarity between two sets of shingles."""
    intersection = shingles1.intersection(shingles2)
    union = shingles1.union(shingles2)
    return len(intersection) / len(union) if union else 0.0

def check_sentence_plagiarism(sentence: str) -> Dict[str, Any]:
    """Check plagiarism for a single sentence by searching and comparing content."""
    result = {"sentence": sentence, "matches": []}
    urls = google_search(sentence)
    
    for url in urls:
        content = fetch_web_content(url)
        if content:
            original_shingles = get_shingles(sentence)
            content_shingles = get_shingles(content)
            # similarity = calculate_jaccard_similarity(original_shingles, content_shingles)
            similarity = similarity1(original_shingles, content_shingles)
            result["matches"].append({"url": url, "score": similarity})

    # Sort matches by score in descending order and take the highest
    if result["matches"]:
        result["matches"].sort(key=lambda x: x["score"], reverse=True)
        highest_match = result["matches"][0]
        result["highest_match"] = {"url": highest_match["url"], "score": highest_match["score"]}
    else:
        result["highest_match"] = {"url": None, "score": 0.0}

    return result

def plagiarism_checker(text: str) -> List[Dict[str, Any]]:
    """Run plagiarism check on each sentence in the input text."""
    sentences = sent_tokenize(text)
    results = [check_sentence_plagiarism(sentence) for sentence in sentences]
    return get_score(results)

def get_score(data):
    # Merging sentences by URL and score
    result = []
    for entry in data:
        url = entry['highest_match']['url']
        score = entry['highest_match']['score']
        sentence = entry['sentence']
        
        # Check if we should merge with the last entry
        if result and result[-1]['url'] == url and result[-1]['score'] == score:
            result[-1]['sentence'] += " " + sentence  # Append the sentence
        else:
            # Add a new entry
            result.append({
                'sentence': sentence,
                'url': url,
                'score': score
            })

    return result
# Example usage
if __name__ == "__main__":
    input_text = """NoSQL databases (AKA "not only SQL") store data differently than relational tables. NoSQL databases come in a variety of types based on their data model. The main types are 
document, key-value, wide-column, and graph. They provide flexible schemas and scale easily with large amounts of big data and high user loads.
In this article, you'll learn what a NoSQL database is, why (and when!) you should use one, and how to get started.
"""
    results = plagiarism_checker(input_text)
    print(json.dumps(results, indent=2))
