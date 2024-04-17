import argparse
import requests
import json

def _get_currency(url_currency):  
    return requests.get(url_currency).json()

def _load_bigquery(df, project, dataset, table):
    temporary_bucket_name = 'datalake-raw-poc'
    table_path = f'{project}.{dataset}.{table}'
    (df.write.format("bigquery") 
            .option("table", table_path)
            .option("temporaryGcsBucket", temporary_bucket_name)
            .mode("append").save())

#"gs://bucket-name/path/to/destination/data.json.gz"
def _load_gcs(df,path):
    df.write.format("json").option("compression", "gzip").save(path)

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "process_date", help="The date that should start the reprocessing")
    return vars(parser.parse_args())