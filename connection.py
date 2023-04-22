import boto3
import pandas as pd
from io import StringIO


df = pd.read_csv('output.csv')
s3 = boto3.client('s3',aws_access_key_id ='AKIAUM6GXJUBLPYHWSV4',aws_secret_access_key = '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')
csv_buff = StringIO()
df.to_csv(csv_buff, header = True, index = False)
csv_buff.seek(0)
s3.put_object(Bucket = 'rohit03071', Body = csv_buff.getvalue(),Key = 'out1.csv')