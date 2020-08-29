import os
import logging
from model.node_service import *
import boto3
import json

logger=logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    logger.info(bucket_name)
    key_name = event['Records'][0]['s3']['object']['key']
    logger.info(key_name)
    s3 = boto3.client('s3')
    response=s3.get_object(Bucket=bucket_name,Key=key_name)
    data = response['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    parse_list = parse_json(json_data)
    create_nodes(parse_list)