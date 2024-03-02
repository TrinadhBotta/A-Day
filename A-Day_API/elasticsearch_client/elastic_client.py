from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from configparser import ConfigParser


def send_data_to_index(data, index_prefix='my-memories'):
    es = Elasticsearch(['http://localhost:9200'])

    # Get the current year and month
    current_year_month = datetime.now().strftime('%Y%m')

    # # Create the index name
    index_name = f'{index_prefix}-{current_year_month}'

    # # Check if the index exists
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

    # Index the data
    es.index(index=index_name, body=data)
