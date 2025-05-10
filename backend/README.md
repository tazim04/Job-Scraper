# TalentSync Backend

## Overview

This backend is fully **serverless**, built using **AWS Lambda** functions that are secured using **AWS Cognito with Google OAuth authentication**.

It accepts a resume (presigned S3 url) and a LinkedIn job posting link, scrapes the job description, analyzes it using Groq API, and returns a compatibility report based on the match between the resume and job requirements.

---

## Authentication

All API access is secured via:

- **AWS Cognito Identity Pools**
- **Google OAuth 2.0**

Users authenticate via Google, and their identity is federated through Cognito to retrieve **temporary AWS credentials**. These credentials are then used to **invoke the API Gateway endpoints** that trigger the Lambda function securely.

---

## Architecture

- **AWS Lambda** – Executes scraping, S3 file access, and resume-job comparison
- **AWS API Gateway** – Public-facing endpoint secured by Cognito-authorized IAM calls
- **AWS S3** – Secure storage for uploaded resumes
- **AWS Cognito + Google OAuth** – Handles user authentication and authorization
- **Docker + AWS ECR** – Custom Docker image (with Playwright and dependencies) is built locally and pushed to **Amazon ECR**, which is used as the Lambda deployment source
- **Playwright** – Headless browser for scraping LinkedIn job data
- **Groq API** – AI-powered resume analysis (llama-3.3)
