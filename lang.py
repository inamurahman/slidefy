from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import imagescrapper
import os, re
from openai import OpenAI


key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=key)

def generate_latex(subject, number):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a LateX presentation maker, Your output is only Latex code on given subject in {number} slides."},
            {"role": "user", "content": subject},
        ]
    )
    return completion.choices[0].message.content



os.environ["OPENAI_API_KEY"] = key
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API')
os.environ["LANGCHAIN_TRACING_V2"] = "true"


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant. Please respond to the user's queries."),
        ("user", "Question:{question}")
    ]
)

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are assisting in creating a presentation. Your task is to design a structured outline for the presentation with 10 slides, including elements like title, introduction, etc. Output only the outlines of each slide without any numbering (e.g., 'Introduction', 'Main Points', etc.)."),
#         ("user", "Question: {question}")
#     ]
# )


chatgpt = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()
chain = prompt|chatgpt|output_parser

google_api_key = os.getenv('GOOGLE_API_KEY')

gemini = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
# result = gemini.invoke("Sing a ballad of LangChain.")
# print(result.content)

def generate_slide_titles(topic):
    # Generate slide titles using the Gemini API
    prompt = f"Generate each slide titles for the topic: {topic}. Each title should be concise and informative."
    response = gemini.invoke(prompt)
    slide_titles = response.content.split('\n')
    slide_titles = [title.strip() for title in slide_titles if title.strip()]
    for i in range(len(slide_titles)):
        slide_titles[i] = slide_titles[i].replace("**", "")
    return slide_titles

def generate_slide_content(slide_title):
  prompt = f"Generate detailed content for the slide titled: {slide_title}. The content should be informative and structured, suitable for a presentation slide. Content should strictly be within 100 words and have only 4 major points maximum. do not include the slide title again in this response.in markdown"
  response = gemini.invoke(prompt)
  return response.content

def generate_markdown_slide(topic, number):
    p = f"Generate {number} markdown presentation slides on the topic: {topic}. Include an introduction slide with a captivating title and overview, followed by slides in the {topic}.add image with apt image topic(creative topic related to the slide that could be searched on web) (give only image topic not the link, format ![alt text]()). Conclude the presentation with a summary slide outlining key takeaways and recommendations if any.give full slides in markdown format."
    response = chatgpt.invoke(p)
    return response.content

"""
add image with apt image topic(creative topic related to the slide that could be searched on web) (give only image topic not the link, format ![alt text]())
"""

def replace_images(markdown_text):
    # Extract image links from the presentation text
    image_link_regex = r'!\[(.*?)\]\((.*?)\)'
    image_links = re.findall(image_link_regex, markdown_text)
    original_links = []
    for alt_text, image_link in image_links:
        link = imagescrapper.get_image_links(alt_text,1)
        if len(link) >= 1:
            original_link = link[0]
        else:
            original_link = ''
        original_links.append(original_link)
    modified_text = markdown_text
    for original_link, (_, image_link) in zip(original_links, image_links):
        modified_text = modified_text.replace(image_link, original_link)
    return modified_text
