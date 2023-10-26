import requests
from bs4 import BeautifulSoup
from googlesearch import search
import trafilatura


def split_in_sentences(text):
    sentences=[x.strip() for x in text.strip().split(". ")]
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
    # union = len(set1.union(set2))
    # return intersection / union if union != 0 else 0.0
    return  intersection / len(set1)
def similarity_score(input_text, collected_text, k=3):
    
    shingles1 = generate_shingles(input_text, k)
    shingles2 = generate_shingles(collected_text, k)
    similarity_score = similarity(shingles1, shingles2)
    return similarity_score


def get_urls(sentences):
    
    sources={}

    last_common_urls = []
    for sentence in sentences:
        
        serp_urls=[]
        try:
            for i in search(f'"{sentence}"', tld="com", lang='en', num=5, stop=None, pause=2):
                if len(serp_urls)<5:
                    serp_urls.append(i)
                else:
                    break
        except Exception as e:
            print(e, '\nNo internet connection')
            #return "No internet connection"
            break


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
            final_url=max(scor)
            final_score=scor[final_url]
            if final_score > 0.5:
                results[key]={"url": final_url, "score": round(final_score*100)}


    return results


def plagiarism_checker(input_text):
    sentences=split_in_sentences(input_text)
    sources=get_urls(sentences)
    result=get_scores(sources)
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
    '''try:
        result =plagiarism_checker(input_text)
    except Exception as e:
        print("Error", e)

    all_scores=[]
    for key, value in result.items():
        print(f'Sentence: {key} \nSource: {value["url"]} \nText Maches: {value["score"]}%')
        print("-"*100)
        all_scores.append(value['score'])

    total_score=sum(all_scores)/len(all_scores)
    if total_score:
        print(f'Unique: {100-total_score}%   &   Plagiarism: {total_score}%')
    '''
