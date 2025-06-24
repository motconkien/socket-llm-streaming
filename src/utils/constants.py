import configparser
import os



parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__),'../config/config.conf'))

OPENAI_API_KEY = parser.get("openai",'api_key')

aws_access_id = parser.get('aws','aws_access_key_id')
aws_access_key = parser.get('aws','aws_secret_access_key')
aws_region = parser.get('aws','aws_region')
aws_bucket = parser.get('aws','aws_bucket_name')