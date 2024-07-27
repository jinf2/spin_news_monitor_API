import feedparser
import openai
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from langchain_community.llms import Ollama
import Google_URL_decode

openai.api_key=''

def extract_GPT_3(article_content):
    prompt = f"Extract the name, position, department, and a summary of the content related to the professor from the following article. Please reduce the summary part to one sentence. The result will be presented with  professor's name: , position: , department, and summary: .if there is not result or No information is available, just only say 'no'. \n\n{article_content} "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Extract professor information from news articles."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()

def extract_GPT_4(article_content):
    prompt = f"Extract the name, position, department, and a summary of the content related to the professor from the following article. Please reduce the summary part to one sentence. The result will be presented with  professor's name: , position: , department, and summary: .if there is not result or No information is available, just only say 'no'.\n\n{article_content}"
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "Extract professor information from news articles."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()

def extract_llama3(article_content):
    llm = Ollama(model="llama3")
    prompt = f"Extract the name, position, department, and a summary of the content related to the professor from the following article. Please reduce the summary part to one sentence. The result will be presented with  professor's name: , position: , department, and summary: .if there is not result or No information is available, just only say 'no'.\n\n{article_content}"
    response = llm.invoke(prompt)
    return response

def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    author = soup.find('meta', attrs={'name': 'author'}) # get author
    author = author['content'] if author else 'No author' # check the author exist or not
    paragraphs = soup.find_all('p') # returns a list of all matching tags(the main textual content of the webpage)
    content = '\n'.join([p.text for p in paragraphs])# concatenates the text strings into a single string, with each paragraph separated by a newline character
    lists = soup.find_all(['ul', 'ol']) #Extract bulleted and numbered lists(unordered list and ordered list)
    list_content = []
    for line in lists:
        items = line.find_all('li') #find all list item
        list_content.append('\n'.join([f"{item.text}" for item in items]))
    full_content = content+'\n\n'+' '.join(list_content)
    full_content = re.sub(r'\n{1,}', '\n', full_content)
    return full_content

def New_Monitor(university_name,day_range,LLMs_used):
    query = f'{university_name}%20professor%20when%3A{day_range}'
    url = f'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US%3Aen&oc=11&q={query}'
    feed = feedparser.parse(url)

    #sort the news by time
    news_items = []
    for entry in feed.entries:
        time = entry.published_parsed  # Published time in struct_time format
        pub_datetime = datetime(*time[:6])  # Convert to datetime object
        news_items.append((pub_datetime, entry))
    news_bytime = sorted(news_items, key=lambda x: x[0], reverse=True)

    num = 0
    result={}
    for pub_time, article in news_bytime:
        num+=1
        decode_url=Google_URL_decode.decode_google_news_url(article.link)
        content=get_content(decode_url)
        news_info = f"Title: {article.title}, Published: {article.published}, Link: {decode_url},Source: {article.source['title']}, Content:{content}"

        #determine which LLMs to use
        if LLMs_used == 'GPT4.0':
            llm_result=extract_GPT_4(news_info)
        elif LLMs_used == 'GPT3.0':
            llm_result=extract_GPT_3(news_info)
        elif LLMs_used == 'llama3':
            llm_result=extract_llama3(news_info)
        
        result[num]={'News number':num,'Title': article.title, 'Published': article.published, 'Link': decode_url,'Source': article.source['title'],'LLMs result': llm_result}

    return result

if __name__ == "__main__":
    print(New_Monitor('uiuc','1d','GPT4.0'))


    

    