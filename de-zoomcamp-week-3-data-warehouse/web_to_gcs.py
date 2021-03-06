import io
import os
import requests
import pandas as pd
import pyarrow

import pyarrow.csv as pv
import pyarrow.parquet as pq
from google.cloud import storage

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# services = ['fhv','green','yellow']
init_url = 'https://nyc-tlc.s3.amazonaws.com/trip+data/'
BUCKET = "dtc_data_lake_halogen-byte-339200"


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client(project="halogen-byte-339200")
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, service):
    for i in range(12):
        month = '0'+str(i+1)
        month = month[-2:]
        file_name = service + '_tripdata_' + year + '-' + month + '.csv'
        request_url = init_url + file_name
        print(f"Requesting file: {file_name} at url {request_url}")
        r = requests.get(request_url)
        pd.DataFrame(io.StringIO(r.text)).to_csv(file_name)
        print(f"Local: {file_name}")
        # Replaced df.to_parquet, it was generating a '0' column
        # making it not possible to create a external table with this data.
        # Was the fastest workarround, you can still do this with pandas
        # by setting read_csv to not create a index.
        # df = pd.read_csv(file_name)
        # file_name = file_name.replace('.csv', '.parquet')
        # df.to_parquet(file_name, engine='pyarrow')
        table = pv.read_csv(file_name)
        pq.write_table(table, file_name.replace('.csv', '.parquet'))
        print(f"Parquet: {file_name}")
        upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
        print(f"GCS: {service}/{file_name}")

web_to_gcs('2019', 'fhv')
web_to_gcs('2020', 'fhv')
# web_to_gcs('2019', 'green')
# web_to_gcs('2020', 'green')
# web_to_gcs('2019', 'yellow')
# web_to_gcs('2020', 'yellow')