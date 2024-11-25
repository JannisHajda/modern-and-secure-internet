import pandas as pd
from tqdm.auto import tqdm
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

INPUT_FILE = "./top-10k-preprocessed.csv"
RESULTS_FILE = "./curl_http3_results.csv"
ERRORS_FILE = "./curl_http3_errors.csv"
MAX_WORKERS = 10

df_input = pd.read_csv(INPUT_FILE)

metrics_keys = [
    'time_appconnect',
    'time_connect',
    'time_namelookup',
    'time_pretransfer',
    'time_redirect',
    'time_starttransfer',
    'time_total',
    'remote_ip',
    'remote_port'
]

# Build the metrics format for curl's -w option
metrics_format = "\\n".join([f"{key}: %{{{key}}}" for key in metrics_keys]) + "\\n"

# Base command to run curl inside the Docker container
base_command = [
    'docker', 'run', '--network', 'host', '-i', '--rm', 'ymuski/curl-http3', 'curl',
    '--http3-only',  # Force HTTP/3
    '-4',            # Use IPv4 only
    '-o', '/dev/null',  # Discard the actual output, only want metrics
    '-s',            # Silent mode, suppress curl status messages
    '--max-time', '5',  # Set connection timeout to 5 seconds
    '-w', metrics_format  # Get specific metrics
]

results = []
errors = []

def process_url(row):
    url = row['url']
    command = base_command + [url]

    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        metrics = {'url': url}
        for line in result.stdout.splitlines():
            if ': ' in line:
                key, val = line.split(': ', 1)
                metrics[key.strip()] = val.strip()

        return metrics

    except subprocess.CalledProcessError as e:
        # Capture the error code and stderr
        return {
            'url': url,
            'errorCode': e.returncode,
            'errorMessage': e.stderr.strip()
        }

with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(df_input))) as executor:
    futures = []
    for index, row in df_input.iterrows():
        futures.append(executor.submit(process_url, row))

    for future in tqdm(as_completed(futures), total=len(futures), desc="Processing URLs", leave=True):
        try:
            data = future.result()
            if 'errorCode' in data:
                errors.append(data)
            else:
                results.append(data)
        except Exception as e:
            errors.append({
                'url': data.get('url', 'Unknown'),
                'errorCode': 'Exception',
                'errorMessage': str(e)
            })

df_results = pd.DataFrame(results)
df_errors = pd.DataFrame(errors)

url_order_dict = {url: idx for idx, url in enumerate(df_input['url'])}

df_results['sort_order'] = df_results['url'].map(url_order_dict)
df_results_sorted = df_results.sort_values('sort_order').drop(columns=['sort_order']).reset_index(drop=True)

df_errors['sort_order'] = df_errors['url'].map(url_order_dict)
df_errors_sorted = df_errors.sort_values('sort_order').drop(columns=['sort_order']).reset_index(drop=True)

df_results_sorted.to_csv(RESULTS_FILE, index=False)
df_errors_sorted.to_csv(ERRORS_FILE, index=False)
