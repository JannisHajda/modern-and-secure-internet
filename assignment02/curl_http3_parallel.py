import csv
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_FILE = './top-10k-www.csv'
OUTPUT_FILE = './curl-http3-top-10k-parallel.csv'
MAX_WORKERS = 20

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

time_metrics = {key for key in metrics_keys if "time" in key}

base_command = [
    'curl', '--http3',
    '-4',
    '-o', '/dev/null',
    '-s',
    '-w', "\\n".join([f"{key}: %{{{key}}}" for key in metrics_keys]) + "\\n"
]

columns = ['url'] + metrics_keys

def fetch_metrics(url):
    command = base_command + [url]
    metrics = {}

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            key, value = line.split(': ')
            value = value.strip()
            metrics[key] = value
        return url, metrics, None
    except subprocess.CalledProcessError as e:
        return url, None, e.returncode

if __name__ == '__main__':
    failed_urls = []

    with open(INPUT_FILE) as input_file, open(OUTPUT_FILE, 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        writer.writerow(columns)

        # Prepare URLs list
        urls = [row[0] for row in reader]

        # Use ThreadPoolExecutor to run curl commands in parallel
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(fetch_metrics, url): url for url in urls}

            # Process results as they complete
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing URLs", unit="url"):
                url, metrics, error_code = future.result()

                if metrics:
                    writer.writerow([url] + [metrics.get(key, '') for key in metrics_keys])
                else:
                    failed_urls.append((url, error_code))

    # Print summary of failed URLs
    if failed_urls:
        print("\nSummary of Failed URLs:")
        for url, error_code in failed_urls:
            print(f"{url} - Error code: {error_code}")
    else:
        print("\nAll URLs processed successfully!")
