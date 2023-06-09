# -*- coding: utf-8 -*-
"""
Created on Mon May 22 13:02:16 2023

@author: PeterJordan
"""

import requests
import json
import openai
from googlesearch import search
from bs4 import BeautifulSoup
from transformers import GPT2Tokenizer
import time
import random


openai.api_key="enter_openai_api-key"

def count_tokens(string):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokens = tokenizer.tokenize(string)
    return len(tokens)-1

from googleapiclient.discovery import build

def search_web(query, num_results=9):
    search_results = []
    service = build("customsearch", "v1", developerKey="enter_google_api_key")
    res = service.cse().list(q=query, cx='enter_google_c_key', num=num_results).execute()
    search_results = [item['link'] for item in res['items']]
    return search_results

def extract_text_from_link(link: str):
    page = requests.get(link)
    time.sleep(1)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_p_tags = soup.find_all('p')
    return '\n'.join([p.get_text() for p in all_p_tags])

def passage_segmenter(passage):
    segment = []
    count = 0
    while count < len(passage):
        segment.append(passage[count:count + 8000])
        count += 8000
    return segment

def ask_question(messages):

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        stream=True
    )

    output = ""
    print("thinking...")
    for chunk in response:
        if "delta" in chunk["choices"][0]:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                content = delta["content"]
                output += content
                print(content, end="")
                
    return output

def order_links(query, links_str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful, pattern-following assistant."},
            {"role": "user", "content": f"Output in the format of a python list the order in which of following links are most likely to best answer the query, {query}\nExample output formatting (order is random. Use as a formatting example only. You are only allowed to re-oder the list, you are not allowed to remove links unless they are PDFs or you have been told to leave them out): [4,7,2,1,5,6,8,9,3]\n (answer with list of ints only)? Links: " + links_str}
        ]
    )
    output_str = response["choices"][0]["message"]["content"].lower().replace(" ", "")

    # Process the output string and convert it into a list of integers
    output_list = [int(x) for x in output_str.strip('[]').split(',') if x.strip().isdigit()]
    
    return output_list

def summarize(query, res, link):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """You are a helpful, pattern-following assistant. You are given some text retrieved from a website and a research query and you summarize only the parts of the text relevant and useful to the answering the research query. You only answer using the following JSON format:
             {
                "is_relevant" : boolean, #true if the provided text provides information relevant to answering the users query, false if the text irrelevant to the query or just discusses access denial to a webpage
                "summary": "string" #summary of the key information in the text if is_relevant is true. null if is_relevant is false
            }"""},
            {"role": "user", "content": f"Summarize the key information in the following text, which was scraped from the website {link}, that are relevant to answering the question, {query}. Text: " + res}
        ],
        stream = True
    )
    output = ""
    for chunk in response:
        if "delta" in chunk["choices"][0]:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                content = delta["content"]
                output += content
                print(content, end="")
    return output

def summarize_list(query, summaries):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful, summarizing assistant. You receive a specific question and then some text and your job is to summarize the text that specifically relates to the question. Anytime you encounter text that indicates an error occured during the scraping process, only respond with \"na\" and absoletely nothing else."},
            {"role": "user", "content": f"Summarize the key points in the following text, which summarize the content on a website that specifucally relates to answering the question, {query}. If there is none, respond with only \"na\". Text: " + summaries}
        ],
        stream = True
    )
    print("summarizing..")
    output = ""
    for chunk in response:
        if "delta" in chunk["choices"][0]:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                content = delta["content"]
                output += content
                print(content, end="")
    return output

def check_source(query_links, search_info, topic_summary):
    print("\n")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """You are a helpful, pattern-following assistant. You will be given a summary of the text from a website and a users question and you will decide whether the summary generated provides enough informration to answer the question or if the information gathered is inadequate and more is needed. You only respond in the following JSON format:
             {
                "continue" : boolean, #false if the provided summary provides ample information to answer the users question, true if more information is needed.
            }
            
            *Note: only set continue to true if key information is needed, otherwise set this value to false. If the question can be answered using the information gathered, then continue should be false. All thats needed is a few sentences that do answer the question.
            """},
            {"role": "user", "content": f"Does the following text provide ample information to answer the question, {search_info} Text: " + topic_summary +"\nLinks: " + str(query_links)}
        ],
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream = True
    )
    output = ""
    for chunk in response:
        if "delta" in chunk["choices"][0]:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                content = delta["content"]
                output += content
                print(content, end="")
    return output

def start_research(query):
    
    messages=[
        {"role": "system", "content": """
    You are an AI research assistant that only responds in JSON. You have been shown to be capable of completing 
    complex research tasks that require retriving information on several different topics at a superhuman level.
    The following is the JSON format of all your outputs
    {
        "number_of_searches" : int #An integer value representing the number individual google searches needed,
        "search_queries" : {
            "1" : "string", #first search query,
            "2" : "string", #second search query
            ...
            "n" : "string" #nth query (Max queries: 5)
        }
        "search_query_goals" : {
            "1" : "string", #Describe what information that needs to be obtained with query one
            "2" : "string", #Describe what information that needs to be obtained with query two
            ...
            "n" : "string" #Describe what information that needs to be obtained with query n (Max queries: 5)
        }
    }

    search_query_goal should always be phrased as a question
    """}
    ]
    messages.append({"role": "user", "content": query})

    # Create a dictionary to hold search queries
    json_dict = {
        "search_queries": {}
    }

    response = ask_question(messages)
    json_data = json.loads(response)
    num_searches = int(json_data['number_of_searches'])
    return json_dict, json_data, num_searches

def get_web_info(json_dict, json_data, i, read_links):
    new_key = f"topic_{str(i)}"
    json_dict["search_queries"][new_key] = []
    search_query = json_data['search_queries'][str(i)]
    search_info = json_data['search_query_goals'][str(i)]
    print("\nRetrieving links for topic " + str(i) + "...\n")
    query_links = search_web(search_query)
    for link in read_links:
        if link in query_links:
            query_links.remove(link)
    print("\nLinks retrieved:")
    for link_count, link in enumerate(query_links, 1):
        print(f"Link #{link_count}: {link}")
    print("\nOrdering links by relevancy...")
    ordered_links = order_links(search_info, str(query_links))
    print(f"Order chosen: {ordered_links}")
    return search_query, search_info, query_links, ordered_links, json_dict, new_key
    
def create_summaries(search_query, search_info, query_links, ordered_links, json_dict, json_data, new_key, i):
    link_verdict_json = {
        "continue": True
    }
    link_count = 1
    all_links_processed = False
    new_search_generated = False
    while link_verdict_json['continue'] and not all_links_processed:
        for ordered_link in ordered_links:
            link_key = f"link_{str(link_count)}"
            current_link = query_links[ordered_link - 1]
            current_link_text = extract_text_from_link(current_link).strip()
            print("\nSummarizing text...\n")
            print("Link: " + str(current_link) + "\n")
            segments = passage_segmenter(current_link_text)
            for segment in segments:
                link_summary = summarize(search_query, segment, current_link)
                summary_json = json.loads(link_summary)
                if summary_json['is_relevant']:
                    read_links.append(current_link)
                    new_value_dict = {
                        f"{link_key}": current_link,
                        f"{link_key}_summary": summary_json['summary']
                    }
                    json_dict["search_queries"][new_key].append(new_value_dict)
                    link_verdict_json = json.loads(check_source(query_links, search_info, summary_json['summary']))
                    if not link_verdict_json['continue'] or len(link_summary) >= 3000:
                        break
                else:
                    break
                print("\n")
            link_count += 1
            if link_count > len(ordered_links):
                all_links_processed = True
            if not link_verdict_json['continue'] or link_count > 9 or all_links_processed:
                break
        if not link_verdict_json['continue'] or link_count > 9 or all_links_processed:
            break

    storage = json.dumps(json_dict, indent=2)
    print("\n")
    print(storage)
    return json_dict, new_search_generated
    
def generate_answer(query, json_dict):
    answer_messages=[
        {"role": "system", "content": """
        You are a research chatbot. You will be provided with a research task from the user as well as a bunch of information that was just scraped from the web and your job is to use that information to generate a very detailed and comprehensive research report with evidence-based explanations for every argument. You will always cite your work by using footnotes.
        """}
    ]

    answer_prompt = "User generated research question: " + query + "\n\nInformation:\n"
    sorted_keys = sorted(json_dict["search_queries"].keys())
    for topic in sorted_keys:
        answer_prompt += f"\n- Topic: {topic}\n"
        for topic_info_dict in json_dict["search_queries"][topic]:
            for link_key, link in topic_info_dict.items():
                if "_summary" not in link_key:
                    answer_prompt += f"  - {link_key}: {link}\n"
                    summary_key = f"{link_key}_summary"
                    if summary_key in topic_info_dict:
                        summary = topic_info_dict[summary_key]
                        answer_prompt += f"  - {summary_key}: {summary}\n"

    print(answer_prompt)
    answer_messages.append({"role": "user", "content": answer_prompt})
    answer = ask_question(answer_messages)
    return answer

    
def main():
    query = input("Query: ")
    global read_links
    read_links = [] 
    json_dict, json_data, num_searches = start_research(query)
    for i in range(1, num_searches + 1):
        search_query, search_info, query_links, ordered_links, json_dict, new_key = get_web_info(json_dict, json_data, i, read_links)
        json_dict, new_search_generated = create_summaries(search_query, search_info, query_links, ordered_links, json_dict, json_data, new_key, i)
    output = generate_answer(query, json_dict)
    
main()
    