import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, lit
import utils
import logging
from datetime import datetime
import uuid

LOGGER: logging.Logger = logging.getLogger("dataproc_processor")

def run_job(project, process_date):
    spark = SparkSession.builder.appName("ETLJob").getOrCreate()
    dataset_raw = 'raw_sales'
    if process_date == '1900-01-01':
        process_date = datetime.utcnow().date().strftime('%Y-%m-%d')

    date_obj = datetime.strptime(process_date, '%Y-%m-%d')
    date_str = date_obj.strftime('%Y%m%d')
    process_date_str = date_obj.strftime('%Y-%m-%d')
    datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    uuid_4dig = str(uuid.uuid4().hex)[:4]
    path = 'gs://datalake-raw-poc/ingested/transactions/json'

    url_currency = f'https://api.apis.net.pe/v1/tipo-cambio-sunat?fecha={process_date_str}'
    table_currency = 'tb_currency'
    path_table_currency = f'{path}/{date_str}/{table_currency}_{uuid_4dig}.json.gz'
    currency = utils._get_currency(url_currency)
    df_currency = spark.createDataFrame([currency])
    df_currency = df_currency.withColumn("process_datetime", lit(datetime_str))
    df_currency.show()
    LOGGER.warning("df_currency count: ")
    LOGGER.warning(df_currency.count())
    utils._load_bigquery(df_currency, project, dataset_raw, table_currency)
    LOGGER.warning("loaded to bigquery")
    utils._load_gcs(df_currency,path_table_currency)
    LOGGER.warning("loaded to gcs")    

    return "PySpark Job Finished"

if __name__ == '__main__':
    args = utils._parse_args()
    print('args:', args)
    project_gcp = 'chrome-mediator-420023'
    process_date = args['process_date']
    print('process_date:', process_date)
    result = run_job(project_gcp, process_date)
    print(result)