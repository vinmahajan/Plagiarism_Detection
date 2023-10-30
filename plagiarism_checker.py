import requests
from bs4 import BeautifulSoup
# from googlesearch import search
import trafilatura


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


def google_search(query):
    links=[]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

    # Perform a Google search
    search_url = f'https://www.google.com/search?q="{query}"'
    response = requests.get(search_url, headers=headers)

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


def get_urls(sentences):
    
    sources={}

    last_common_urls = []
    for sentence in sentences:
        
        # serp_urls=[]
        # try:
        #     for i in search(f'"{sentence}"', lang='en'):
        #         if len(serp_urls)<5:
        #             serp_urls.append(i)
        #         else:
        #             break
        # except Exception as e:
        #     print(e, '\nNo internet connection')
        #     #return "No internet connection"
        #     break
        serp_urls=google_search(sentences)
        # print(serp_urls)

        if last_common_urls:
            last_key=list(sources)[-1]
            common_urls=list(set(serp_urls).intersection(last_common_urls))

            if common_urls:
                combined_sentence = list(sources.keys())[-1] + ". " + sentence
                sources[combined_sentence] = common_urls
                last_common_urls = common_urls
                del sources[last_key]
            
            else:
                sources[sentence] = serp_urls
                last_common_urls = serp_urls
        else:
            sources[sentence] = serp_urls
            last_common_urls = serp_urls
    return sources


def get_scores(sources):
    results={}
    for key, value in sources.items():
        
        #google search and get urls
        scor={}
        for url in value:
            download= trafilatura.fetch_url(url)
            content=trafilatura.extract(download, include_comments=False, include_tables=False)
            if content:
                result_score = similarity_score(key, content)
                
            else:
                result_score=0
                        
            scor[url]=result_score
        
        if value:
            final_url=max(scor, key=scor.get)
            final_score=scor[final_url]
            if final_score > 50:
                results[key]={"url": final_url, "score": round(final_score)}

    return results


from datetime import datetime

def plagiarism_checker(input_text):
    sentences=split_in_sentences(input_text)

    print("Time =", datetime.now().strftime("%H:%M:%S"))
    sources=get_urls(sentences)
    print("getting urls Time =", datetime.now().strftime("%H:%M:%S"))
    result=get_scores(sources)
    print("scores Time =", datetime.now().strftime("%H:%M:%S"))
    # print(result)
    return result


def get_raw_result(input_text):
    
    text=""
    try:
        result =plagiarism_checker(str(input_text))
        all_scores=[]
        for key, value in result.items():
            text+=f'\n{"-"*100}\nSentence: {key} \nSource: {value["url"]} \nText Maches: {value["score"]}%'
            all_scores.append(value['score'])
        if all_scores:
            total_score=sum(all_scores)/len(all_scores)
        #if total_score:
            text+=(f'\n\nUnique: {100-total_score}%   &   Plagiarism: {total_score}%')
    except Exception as e:
        text=f'Error:{e}'

    return text


if __name__ == "__main__":
    
    input_text=input("Enter The Text: ")
    print("Working...")
    final_output=get_raw_result(input_text)
    print(final_output)

