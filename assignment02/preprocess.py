import pandas as pd

INPUT_FILE = './top-1m.csv'
OUTPUT_FILE = './top-10k-preprocessed.csv'

df_input = pd.read_csv(INPUT_FILE, names=['index', 'url']).drop('index', axis=1)
df_output = df_input.copy()
df_output = df_output.iloc[:10000]
df_output['url'] = 'https://www.' + df_output['url']

df_output.to_csv(OUTPUT_FILE, index=False)