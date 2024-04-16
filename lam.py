import ollama

def gen_gemma(subject):
    prompt = "you are a helpful assistant. Generate a PowerPoint presentation on the topic you are given. Include an introduction slide with a captivating title and overview, followed by slides highlighting key concepts(each concepts in different slides, use slide seperation). Each concept should be presented with bullet points summarizing its advantages and applications. Intersperse the presentation with slides containing graphs and charts illustrating global trends and case studies . Conclude the presentation with a summary slide outlining key takeaways and recommendations. Additionally, include slides for a Q&A section at the end of the presentation, providing placeholders for audience inquiries and possible answers.in markdown format.(add '---' slide seperations between each slide content. Keep only few content in each slide for better readability. One content in one slide)"

    response = ollama.chat(model='gemma',
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "create a presentation about" + subject }
    ]
    )
    return(response['message']['content'])