
# TalentSync

TalentSync is a Chrome extension that helps job seekers instantly evaluate how well they match with LinkedIn job postings. It leverages AI to analyze job descriptions against your resume and provides a score, personalized recommendations, and tips to improve your fit — all without ever leaving the job page.


Link to TalentSync on the Chrome Web Store: https://chromewebstore.google.com/detail/talentsync/odkpmfccegfdcekejlolmopnlhnpfebm

## Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: AWS Lambda (Python), Playwright for scraping
- **Authentication**: Google OAuth + AWS Cognito
- **Cloud Infrastructure**: AWS (S3, IAM, Cognito, Lambda, API Gateway)
- **AI Analysis**: Groq API (LLaMA 3)
## Features

- 🔍 **One-click job scan** – Automatically detects LinkedIn job pages
- 🤖 **AI-powered fit analysis** – Get a match score based on your resume
- 🧠 **Personalized recommendations** – Suggestions on how to improve your chances
- 🔒 **Private & secure resume handling** – Resume is stored and processed securely via AWS S3 and pre-signed URLs
- ⚡ **Fast & responsive UI** – Built for speed with modern web tooling
