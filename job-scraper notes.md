# job-scraper notes

# two main features:

- compare a job board to users resume
  - user will provide their resume, as well as a link to a job board
  - app will process (or have it previously processed) and then scrape the job board
  - then use ai models to compare and determine if its a good match or not, and why
  - need to find a LLM from hugging face for reasoning
- find a job that matches users resume
  - user will provide their resume, some preferences (location, job type, etc)
  - app will process (or have it previously processed), navigate to glassdoor with the specefied requirements and key words from resume
  - scrape the top jobs that come up, then use LLMs from hugging face to get confidence of each job related to the resume, then give reasonings

SCRATCH FINE TUNING A CLASSIFICATION MODEL, GO ALL IN USING GROQ llama-3.3-70b-versatile WITH A STRONG PROMPT
