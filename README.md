# ResearchGPT
A happy medium between AI search and GPT Agents

# Project Overview
ResearchGPT is an innovative concept, engineered to combine the practical functionality of language model-powered search engines with the multi-step, chain-of-thought reasoning of autonomous AI agents like Auto-GPT and BabyAGI. The concept aims to provide a cohesive and productive language model agent that overcomes the constraints found in present AI tools.

# Rationale and Background
Current autonomous AI agents, such as Auto-GPT and BabyAGI, demonstrate remarkable advancements in artificial intelligence. They exhibit exceptional multi-step reasoning capabilities, crucial for complex tasks. However, these agents are often criticized for their low reliability and inconsistency, significantly limiting their practical usage.

Meanwhile, AI-powered search engines like Bing AI and You.com leverage large language models (LLMs) to conduct web research. Despite their technological sophistication, these engines often lack a distinctive advantage over manual search techniques. Their search scope tends to be narrowed down, answering queries based on a limited set of sources and essentially paraphrasing content from the top-ranked articles. This constrained approach often leaves users with insufficient or overly specific information, hindering effective decision-making.

# Conceptual Design of ResearchGPT
With ResearchGPT, I aim to harmonize the aforementioned technologies' strengths, creating an agent that can conduct robust and efficient web research. It derives its chain-of-thought reasoning capabilities from autonomous AI agents and harnesses the reliable task completion aspects of AI-powered search engines, offering a balanced, practical solution.

# Technical Architecture
ResearchGPT applies a sequence of interconnected steps, each contributing to the creation of well-structured, information-rich research outputs. These steps include an initial web search, critical link evaluation, content extraction, text summarization, and finally, the compilation of the research report.

At its core, the script's purpose is to automate a variety of research tasks, creating a coherent workflow that starts with web searches and culminates in the delivery of well-structured, information-rich research reports. This process involves several interconnected steps, each building upon the last to create an output that is much greater than the sum of its parts.

The first step involves using the Google Custom Search JSON API to conduct a targeted, far-reaching search of the web. By accurately interpreting the user's research requirements, the script is able to retrieve the most relevant and authoritative content on the web, making optimal use of Google's unparalleled search infrastructure.

Following the search, the script then performs a critical evaluation of the retrieved links, assessing their content for relevance and reliability. This phase involves an intelligent ranking and ordering process, which arranges the links based on their appropriateness to the research question at hand, thereby prioritizing high-value resources.

Once the most suitable links are selected, the next step involves delving into the content of these webpages and extracting the necessary information. This is made possible through efficient web scraping techniques, and the sophisticated language understanding capabilities of GPT-4. This allows the script to pinpoint and extract only the most relevant pieces of information, disregarding any extraneous data.

The extracted data is then subject to the transformative process of text summarization. This task is performed by the GPT-4 model, which distills the content into its most crucial points, creating a summary that retains all the critical information while shedding the redundant details. This ensures that the final output is concise and easy to understand, without any compromise on the richness or depth of the information.

The final step in the process involves aggregating all the summarized data, and compiling it into a well-organized, evidence-backed research report. This report is formulated to address the user's original query, offering comprehensive insights and conclusions that have been derived from a broad array of reliable sources. To ensure the transparency and traceability of the information, all sources are accurately cited within the report.

In conclusion, this script stands as an advanced research tool, expertly merging the realms of AI and web search to deliver in-depth, structured, and user-tailored research reports. It significantly simplifies the research process, allowing users to focus on analysis and interpretation, rather than getting lost in the sea of information available on the web.

# Key Functionalities
 - Web Searching: Utilizing the Google Custom Search JSON API, the script queries the web based on user-specified research topics.
 - Link Evaluation & Ordering: The search results are assessed, sorted, and ranked in order of relevance to the given research question.
 - Content Extraction & Summarization: Web content from the chosen links is scraped, tokenized, and summarized using a GPT-4 model, extracting the most relevant information and discarding the rest.
 - Report Generation: All the summarized data is aggregated and the script generates a comprehensive, evidence-backed research report, addressing the initial query. All sources of information are duly cited to ensure transparency.

# Dependencies
This script runs on Python 3.6 or newer and relies on the following Python libraries:
 - requests: For making HTTP requests to webpages.
 - json: For handling JSON data.
 - openai: To interact with the OpenAI API.
 - googleapiclient: To use Google's Custom Search JSON API.
 - beautifulsoup4: For parsing HTML and extracting information.
 - transformers: For tokenizing the input using the GPT-2 tokenizer.
 - time: To manage rate-limited requests.
 - random: To generate pseudo-random numbers (if required).
Please note that you need to provide your personal OpenAI and Google API keys to leverage the functionality of this research tool.

# Usage
Begin by entering your research query when prompted. The script will perform the following tasks in sequence: web searches, link extraction and ordering, content summarization, and research report generation. It outputs a comprehensive, well-structured research report based on the information gathered from the web.

# Disclaimer
As the AI models and APIs used in this script rely on probabilistic methods, the results might slightly differ between runs. Hence, it is advisable to cross-verify the information from other reliable sources.
