import csv
import subprocess
from tqdm import tqdm

INPUT_FILE = './top-10k-www.csv'
OUTPUT_FILE = './curl-http3-top-10k.csv'

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

time_metrics = {key for key in metrics_keys if "time" in key}  # Set of time-based metrics

base_command = [
    'curl', '--http3',  # Force HTTP/3
    '-4',               # Use IPv4 only
    '-o', '/dev/null',  # Discard the actual output, only want metrics
    '-s',               # Silent mode, suppress curl status messages
    '-w', "\\n".join([f"{key}: %{{{key}}}" for key in metrics_keys]) + "\\n"  # Get specific metrics
]

columns = ['url'] + metrics_keys

if __name__ == '__main__':
    failed_urls = []  # List to store failed URLs and their error codes

    with open(INPUT_FILE) as input_file, open(OUTPUT_FILE, 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        writer.writerow(columns)

        for row in tqdm(reader, desc="Processing URLs", unit="url"):
            url = row[0]
            command = base_command + [url]

            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)

                metrics = {}
                for line in result.stdout.splitlines():
                    key, value = line.split(': ')
                    value = value.strip()
                    if key in time_metrics:
                        metrics[key] = str(float(value) * 1000)
                    else:
                        metrics[key] = value

                writer.writerow([url] + [metrics.get(key, '') for key in metrics_keys])

            except subprocess.CalledProcessError as e:
                failed_urls.append((url, e.returncode))

    if failed_urls:
        print("\nSummary of Failed URLs:")
        for url, error_code in failed_urls:
            print(f"{url} - Error code: {error_code}")
    else:
        print("\nAll URLs processed successfully!")
