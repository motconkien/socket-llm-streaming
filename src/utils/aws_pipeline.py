#aws: load, create bucket and load 
import boto3
from botocore.exceptions import ClientError
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .constants import *
import datetime

s3 = None
def connect_s3():
    global s3
    if s3 is None:
        try:
            s3=boto3.client(
                's3',
                aws_access_key_id=aws_access_id,
                aws_secret_access_key=aws_access_key,
                region_name=aws_region
            )
            print("Conencted to S3")
            return s3

        except Exception as e:
            raise e("No AWS credentials found. Please check your environment.") from e
    

Bucket_existed = False
def create_bucket(s3):
    global Bucket_existed 

    try:
        s3.head_bucket(Bucket=aws_bucket)
        Bucket_existed = True
    except ClientError as e:
        err_code = int(e.response['Error']['Code'])
        if err_code == 404:
            print(f"Bucket hasnt created. Creating...")
            if aws_region:
                s3.create_bucket(
                    Bucket=aws_bucket,
                    CreateBucketConfiguration={'LocationConstraint': aws_region}
                )
            else:
                s3.create_bucket(Bucket=aws_bucket)
            print("Bucket is created: ", aws_bucket)
            Bucket_existed = True
        else:
            raise
    except Exception as e:
        raise e
    return Bucket_existed
    

def load_to_s3(json_data):


    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    key = f'reviews-data/review_{timestamp}.json'
    s3.put_object(
        Bucket = aws_bucket,
        Key = key,
        Body=json_data,
        ContentType='application/json'
    )
   
    print(f"JSON data successfully uploaded to s3://{aws_bucket}/{key}")
    
