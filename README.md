# <spin_news_moniter_API>

## Overview

This module establishes an API to use different LLMs to get news information from relevant university professors. The news source used for this module is Google news. The model used is GPT4.0, GPT3.5 and llama3:8B

## Prerequisites

Python Version: 3.8.1

## Setup

1. Clone the Repository:
```
git clone https://github.com/Forward-UIUC-2024M/Jin_Fan_news_monitor.git
```

2. Install Dependencies:
```
pip install -r requirements.txt
```

3. Download Ollama:
You can use this link to help to download Ollama in local. https://www.freecodecamp.org/news/how-to-run-open-source-llms-locally-using-ollama/ Just make sure that you download the llama3:8B model

## How to use API

1. open ollama in terminal and then run:
```
ollama run llama3:8b
```

2. add openai API key in news_monitor.py

3. In other terminal, run:
```
python flask_setup.py
```

4. open (microsoft edge, chrome) and type:
```
http://127.0.0.1:5000/FindProfNews/<UniversityName>/<DayRange>/<LLMsT>

<UniversityName>: uiuc, uic, etc
<DayRange>: h(mean in the past of hour), d(mean in the past of day), y(mean in the past of year) 
<LLMsT>: GPT4.0, GPT3.5, llama3

eg:http://127.0.0.1:5000/FindProfNews/uiuc/3d/GPT4.0
```


## Codebase Structure

```
Jin_Fan_news_monitor/
    - requirements.txt
    - result.json/
    - src/
        -- flask_setup.py/
        -- news_monitor.py/
        -- Google_URL_decode.py/
    - _pycache_/
```

* `result.json/`: the result example for API 
* `src/flask_setup.py/`: runs API
* `src/news_monitor.py/`: runs trained model on input data
* `src/Google_URL_decode.py/`: This script decodes Google News generated encoded, internal URLs for RSS items

## Functional Design (Usage)

* In src/news_monitor.py/, we have three function for using three kinds of LLMs, one function for get the content of news link and one function for use above function to get the result:
```python
    def extract_GPT_3(article_content):
        ... 
        return response

    def extract_GPT_4(article_content):
        ... 
        return response

    def extract_llama3(article_content):
        ... 
        return response
    
    def get_content(url):
        ... 
        return full_content

    def New_Monitor(university_name,day_range,LLMs_used):
        ... 
        return result
```

## Demo Video

Include a link to your demo video, which you upload to our shared Google Drive folder (see the instructions for code submission).

## Algorithmic Design

This project can be divided into three main steps:
Obtain news information and extract news content from accurate, comprehensive, and safe channels.
We will use large language models to analyze the news content, extract the required information, and summarize.
We will build an API to provide the news about university professors. 

For the first step, I have explored four methods to obtain news information:
1. Using Google API and Google Custom Search to customize and retrieve news from Google News.
2. Using RSS Feeds to obtain XML-format news documents from specific news pages, thereby acquiring information such as news titles, links, publication dates, and sources.
3. Using News API to fetch news information.
4. Directly using code to scrape the required information from web pages.

After exploring these four methods, we used RSS Feeds to obtain information. The news we get using the Google API and Google Custom Search, which is the first method, is not quite the same as the news we search from Google News. The third way is to use a third-party API, such as the News API, because we need to explore a lot of news; using a third-party API will lead to additional consumption. The fourth method is to pull news content directly from the Google news page. This method may need to be more legitimate. The second method is that RSS Feeds are the way Google News allows us to get news, which can be seen from the following link: https://support.google.com/merchants/topic/2473799?hl=en&ref_topic=7294002&sjid=6466971101479304047-NC

So, for the first step, I use RSS Feeds to obtain XML-format news documents from specific news pages, thereby acquiring information such as news titles, links, publication dates, and sources.  This gives me secure and comprehensive access to Google News. However, the news that comes to RSS feeds is not sorted by publication time. In the later stage, if we want to get new news in Google News, it needs to be sorted by the order of publishing events. In this way, we can only get new news based on the time that has not been extracted. We then use the request and BeautifulSoup library in Python to extract the news text.

For the second step, we explore the GPT3.5 and GPT4 models of chatGPT and the llama3:8B model. We feed the content of the news to all three models with questions. For example: "Please extract the names and positions of all the professors in the news and summarize the events related to the professors." The results of these three models are then compared.

The two LLMs that need to be noted here are ChatGPT and Mate llama. ChatGPT needs to log into an account and get a key to the open API. We need to charge money into this account before we can use the API. For Mate llama, I use Ollama to help with the llama3. Ollama is an open-source app that lets you run, create,   and share large language models locally with a command-line interface on MacOS and Linux. Ollama makes it easy to get started with running LLMs on your own hardware in very little setup time. Then, I directly used LangChain Python libraries on the basis of Ollama. LangChain is a library for building language model call chains. It allows users to define the steps of multiple language model calls and execute them in the defined order. The thing to note here is the Python environment. langchain_community.llms python library requires version 3.8.1 of the python environment. Here, we need to make sure the version is correct.

The third step is to build an API. The input to this API is which school professors the user wants to access, the time frame of the news they want, and which LLM model they wish to use. Here, I use Flask to build the API. Flask is a micro web framework written in Python.  After the program runs in the API, users can input, for example, http://127.0.0.1:5000/FindProfNews/uiuc/7d/GPT4.0 links on the page and use the API. The end user can get a result in JSON format on the website. The result will show all the news in this time range, as well as the time when the news was published, the link, the source, and the information in the news analyzed by LLMs: professor's name, the position of the professors, which department the professors come from and the summary of the events in the news.

Another question that came up in the news feed one week before the project ended was: The original code could directly analyze the RSS link before, but in the last few days of analysis, it suddenly could not get the content. It would help if you were given the original news link to analyze. However, the RSS feed only gives us RSS-format news links. I found a solution to this problem on the Internet. We can decode the RSS format news link directly to get the original link to the news. We can find solutions through this link: https://gist.github.com/huksley/bc3cb046157a99cd9d1517b32f91a99e.


## Issues and Future Work

* If the day_range is long, the API will take a long time to run
* the output interface is not very beautiful
* the results of the LLMs obtained are not all in the format we want
* the time range and be modify by specific day follow google news RSS format:https://www.newscatcherapi.com/blog/google-news-rss-search-parameters-the-missing-documentaiton

## Change Log

summer 2024 (Jin Fan):Initial release with news mocitor API

## References 

* decode RSS news URL: https://gist.github.com/huksley/bc3cb046157a99cd9d1517b32f91a99e
