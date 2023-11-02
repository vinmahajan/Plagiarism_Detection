import requests
from bs4 import BeautifulSoup
from googlesearch import search
import trafilatura
import random

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

def split_in_sentences(text):
    sentences=[x.strip() for x in text.strip().replace('\n', '').split(". ")]
    return sentences


def generate_shingles(text, k):
    shingles = set()
    text = text.lower().split()  # Convert text to lowercase and split into words
    for i in range(len(text) - k + 1):
        shingle = ' '.join(text[i:i + k])  # Join k consecutive words to form a shingle
        shingles.add(shingle)
    return shingles


def similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    return  (intersection / len(set1))*100
def similarity_score(input_text, collected_text, k=3):
    
    shingles1 = generate_shingles(input_text, k)
    shingles2 = generate_shingles(collected_text, k)
    similarity_score = similarity(shingles1, shingles2)
    return similarity_score


def get_content(url):
    for i in range(3):
        download= trafilatura.fetch_url(url)
        content=trafilatura.extract(download, include_comments=False, include_tables=False)
        if content:
            return content
        
        elif i==2 and content is None:
            return ''
        

def google_search(query):
    links=[]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

    # Perform a Google search
    response = requests.get(
                        url="https://www.google.com/search",
                        headers={"User-Agent": get_useragent()},
                        params={"q": f'"{query}"',
                                "num": 5,  # Prevents multiple requests
                                "hl": 'en'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and print search results
        search_results = soup.find_all('h3')
        for idx, result in enumerate(search_results, start=1):
            link = result.find_parent('a')
            if link:
                link_text = link.get('href')
                if link_text and link_text.startswith('http'):
                    links.append(link_text)         
    else:
        print("Failed to perform the Google search.")
    return links #list of links


def get_results(sentences):
    
    sources={}

    for sentence in sentences:

        serp_urls=google_search(sentence)
        # print(sentence)
        temp={}
        for url in serp_urls:
            content=get_content(url)
            sentence_score = similarity_score(sentence, content)
            temp[url] = int(sentence_score)
        # print (temp)
        max_score_url=max(temp, key=temp.get)
        max_score=temp[max_score_url]

        current_score={'url':max_score_url, 'score':max_score}
            
        if sources:
            last_sentence=list(sources.keys())[-1]
            last_url=sources[last_sentence]['url']
            last_url_score=sources[last_sentence]['score']
            if last_url==max_score_url:
                combined_sentence = last_sentence + ". " + sentence
                sources[combined_sentence] = {'url':max_score_url, 'score':int((max_score+last_url_score)/2)} #(current_score['score']+last_url_score)/2
                
                del sources[last_sentence]

            else:
                sources[sentence] = current_score
        else:
            sources[sentence] = current_score
    
    return sources



from datetime import datetime

def plagiarism_checker(input_text):
    sentences=split_in_sentences(input_text)

    print("Time =", datetime.now().strftime("%H:%M:%S"))
    result=get_results(sentences)
    print("scores Time =", datetime.now().strftime("%H:%M:%S"))
    # print(result)
    return result


def get_raw_result(input_text):
    
    text=""
    try:
        result =plagiarism_checker(str(input_text))
        all_scores=[]
        for key, value in result.items():
            text+=f'\n{"-"}\nSentence: {key} \nSource: {value["url"]} \nText Maches: {value["score"]}%'
            all_scores.append(value['score'])
        if all_scores:
            total_score=sum(all_scores)/len(all_scores)
        #if total_score:
            text+=(f'\n\nUnique: {int(100-total_score)}%   &   Plagiarism: {int(total_score)}%')
    except Exception as e:
        text=f'Error:{e}'

    return text


if __name__ == "__main__":
    
    input_text=input("Enter The Text: ")
    print("Working...")
    final_output=get_raw_result(input_text)
    print(final_output)

