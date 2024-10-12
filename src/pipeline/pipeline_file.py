from redis_client import client_redis
import json
from data_processing import data, json_data_to_dataframe

client = client_redis()
print(client.ping())
print(client.json().get('bikes:010', '$.model'))


print(json.dumps(client.json().get('bikes:010'), indent=2))


df_json = data()
print(df_json)

df_df = json_data_to_dataframe()
print(df_df)
