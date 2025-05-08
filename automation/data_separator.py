import pandas as pd
import json

df = pd.read_excel('Strict_Final_Categorized_Transport_Data.xlsx')
df['contextDict'] = df['contextDict'].apply(lambda x: json.loads(x.replace("'", "\"")) if isinstance(x, str) else {})
df['expoutput'] = df['expoutput'].apply(lambda x: json.loads(x.replace("'", "\"")) if isinstance(x, str) else {})
df['inputDict'] = df['inputDict'].apply(lambda x: json.loads(x.replace("'", "\"")) if isinstance(x, str) else {})

def is_matching_transport_type(item, transport_type: str):
    if not isinstance(item, dict):
        return False
    if 'TransportType' not in item:
        return False
    value = item['TransportType']
    if not isinstance(value, str):
        return False
    return value.lower() == transport_type

df_fastest = df.loc[df['inputDict'].apply(lambda x: is_matching_transport_type(x, 'fastest'))].copy()
df_cheapest = df.loc[df['inputDict'].apply(lambda x: is_matching_transport_type(x, 'cheapest'))].copy()
df_safest = df.loc[df['inputDict'].apply(lambda x: is_matching_transport_type(x, 'safest'))].copy()
df_seasonally_preferable = df.loc[df['inputDict'].apply(lambda x: is_matching_transport_type(x, 'seasonally preferable'))].copy()

with pd.ExcelWriter('Strict_Final_Categorized_Transport_Data_Fastest.xlsx') as writer:
    df_fastest.to_excel(writer, index=False)

with pd.ExcelWriter('Strict_Final_Categorized_Transport_Data_Cheapest.xlsx') as writer:
    df_cheapest.to_excel(writer, index=False)

with pd.ExcelWriter('Strict_Final_Categorized_Transport_Data_Safest.xlsx') as writer:
    df_safest.to_excel(writer, index=False)

with pd.ExcelWriter('Strict_Final_Categorized_Transport_Data_Seasonally_Preferable.xlsx') as writer:
    df_seasonally_preferable.to_excel(writer, index=False)
