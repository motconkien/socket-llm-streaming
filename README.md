# Socket streaming and Spark consuming then Load data in json format to Datawarehouse
-------
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
│   └── __pycache__/
├── utils/
│   ├── aws_pipeline.py
│   ├── constants.py
│   └── __pycache__/
├── docker-compose.yml
├── Dockerfile.spark
├── requirements.txt
├── venv/
├── .gitignore
└── readme.md

```
