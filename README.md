# 🔄 Socket-based Real-time Sentiment Analysis with LLM & Spark

This project demonstrates a real-time streaming pipeline using **Socket**, **Apache Spark**, and **LLM-based sentiment analysis**. The goal is to simulate live review data from the **Yelp Academic Dataset**, process it in real time, evaluate the sentiment using either **Stanford CoreNLP** or **an OpenAI LLM**, and finally store the results in **AWS S3**.

---

## 📌 Features

- ⚡ Simulate real-time data using sockets
- 🧠 Sentiment analysis with:
  - Stanford CoreNLP
  - OpenAI LLM (GPT)
- 🔥 Stream processing using Apache Spark Structured Streaming
- ☁️ Store analyzed data in AWS S3 (JSON format)
- 📁 Based on the `yelp_academic_dataset_review.json` dataset

---

## 📂 Project Structure
```
Socket-LLM-Streaming/
src/
│── config/
│   │   └── config.conf
├── datasets/
│   ├── create_sample.py
│   ├── sample_review.json
│   └── yelp_academic_dataset_review.json
├── jobs/
│   ├── spark-streaming.py
│   └── streaming-socket.py
├── models/
│   ├── classifier.py
├── utils/
│   ├── aws_pipeline.py
│   ├── constants.py
├── docker-compose.yml
├── Dockerfile.spark
├── requirements.txt
├── .gitignore
└── README.md

```

---

## ⚙️ How It Works


This project sets up a real-time streaming pipeline using a TCP socket, Apache Spark, and sentiment analysis models (Stanford or OpenAI LLM). Here’s a step-by-step breakdown:

1. **Data Source**:
   - Reviews are loaded from the `yelp_academic_dataset_review.json` file. <br>
   Download from: https://business.yelp.com/data/resources/open-dataset/

2. **Socket Producer**:
   - A Python script (`streaming-socket.py`) simulates a live stream by sending reviews line-by-line to a TCP socket.

3. **Spark Structured Streaming**:
   - Spark connects to the socket, reads incoming data in real-time, and parses each review.

4. **Sentiment Evaluation**:
   - For each review:
     - You can choose to evaluate sentiment using:
       - Stanford CoreNLP
       - OpenAI LLM (e.g., GPT-4): have to paid to recieve quotes
     - Output labels: `POSITIVE`, `NEGATIVE`, or `NEUTRAL`.

5. **Result Storage**:
   - Each processed review is formatted as JSON and uploaded to an AWS S3 bucket for storage and further use.

