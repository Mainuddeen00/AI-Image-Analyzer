# 🚀 AI Image Analyzer

A modern web app that lets users upload images, analyze them using AWS Rekognition, and view results with bounding boxes — all in real-time!

---

## 📸 What It Does

✅ Upload an image from your browser  
✅ Securely store it in S3 using a pre-signed URL  
✅ Trigger a Lambda function via S3 Event Notifications  
✅ Detect labels (objects, faces, scenes) using Amazon Rekognition  
✅ Save results back to an S3 `results/` folder  
✅ Display results beautifully in the frontend — with confidence meters and optional bounding boxes!

---

## 🗂️ Architecture Overview

