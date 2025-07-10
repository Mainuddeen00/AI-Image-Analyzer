AI Image Analyzer


A serverless AI-powered web app that analyzes images using AWS Rekognition, auto-generates labels and object data, and displays results with a modern UI.

Live Demo
Upload any image, and see AI-detected labels and bounding boxes in real time!

Features
Secure Uploads: Pre-signed URLs via API Gateway & Lambda

Serverless Backend: AWS Lambda triggers Rekognition and stores results

Real-Time Analysis: View detected objects, faces, and confidence scores

Clean UI: Dark-themed responsive frontend built with HTML, CSS, and JS

Fully Cloud-Hosted: S3 for storage, Vercel for frontend hosting

Tech Stack
Service	Purpose
AWS S3	Store uploaded images & results
AWS Lambda	Backend processing, Rekognition calls
AWS Rekognition	Image object/face detection
API Gateway	Secure REST API for pre-signed URLs
CloudWatch	Monitor logs & function execution
Vercel	Frontend hosting

📂 Project Structure
bash
Copy
Edit
├── DetectImageLabels.py        # Lambda: Detect labels with Rekognition
├── GeneratePresignedURL.py     # Lambda: Generate pre-signed PUT URLs
├── FetchAnalysisResults.py     # Optional Lambda: Fetch results from S3
├── index.html                  # Frontend UI
├── README.md                   # Project docs
How It Works
Frontend → Requests a pre-signed S3 upload URL via API Gateway.

User Upload → File uploads securely to input/ folder in S3.

S3 Event → Automatically triggers DetectImageLabels Lambda.

AWS Rekognition → Detects labels, objects, faces, and confidence.

Lambda → Saves results JSON to results/ folder in S3.

Frontend → Fetches and displays the labels with a clean UI.

Local Development
This project is 100% serverless — no local server needed.
You can update & redeploy:

Frontend: Deploy to Vercel (1-click)

Backend: Manage Lambda, S3, and API Gateway in the AWS Console
