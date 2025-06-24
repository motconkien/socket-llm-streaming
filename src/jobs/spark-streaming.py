import time 
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from functools import partial
import os 
import json
import sys
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.classifier import classify_local
from utils.aws_pipeline import *
from utils.constants import *



def process_batch(df,batch_id):
    reviews = df.collect()
    results = []
    for row in reviews:
        classification = classify_local(row.text)
        row_dict = row.asDict()
        row_dict["classification"] = classification
        results.append(row_dict)
    for r in results:
        json_data = json.dumps(r, indent=2, ensure_ascii=False)
        try:
            load_to_s3(json_data)
        except Exception as e:
            print(f"Failed to upload: {e}")


def consume_data(spark):
    #format to write s3

    #define schema
    schema = StructType([
        StructField("review_id", StringType()),
        StructField("user_id",StringType()),
        StructField("business_id", StringType()),
        StructField("stars", IntegerType()),
        StructField("date", StringType()),
        StructField("text", StringType())
    ])
    print("Schema defined...")

    review_df = spark.readStream \
                .format('socket') \
                .option('host','127.0.0.1')\
                .option("port", 9999)\
                .load()

    #have to keep column to use llm
    parse_df = review_df.select(from_json(col("value"), schema).alias("data")).select("data.*")
    
    
    query = parse_df.writeStream\
            .foreachBatch(process_batch)\
            .outputMode("append")\
            .start()
    query.awaitTermination()
    # try:
    #     print("Fuck: ",type(parse_df))
    #     aws_query = load_to_s3(kafka_df, spark)
    #     aws_query.awaitTermination()
    # except Exception as e:
    #     print("Error: ",e)

if __name__ == "__main__":
    spark = SparkSession.builder.appName("Socket streaming")\
            .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262")\
            .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    print("conencting S3...")
    s3 = connect_s3()
    Bucket_existed = create_bucket(s3)
    if s3 and Bucket_existed:
        consume_data(spark)