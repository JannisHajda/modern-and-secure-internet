import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from tqdm.auto import tqdm

INPUT_FILE = "./curl_http3_results.csv"
RESULTS_FILE = "./selenium_http2_results.csv"
ERRORS_FILE = "./selenium_http2_errors.csv"

def process_url(row):
    url = row['url']

    # Parse the URL to extract the hostname and port
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port or ('443' if parsed_url.scheme == 'https' else '80')
    origin = f"{hostname}:{port}"

    options = Options()
    options.add_argument('--disable-quic')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # Retrieve performance metrics
        metrics = driver.execute_script("return performance.getEntriesByType('navigation')[0]")
        nextHopProtocol = metrics.get('nextHopProtocol', 'unknown')
        responseStart = metrics.get('responseStart', 0)
        domInteractive = metrics.get('domInteractive', 0)
        domComplete = metrics.get('domComplete', 0)
        final_url = driver.current_url

        return {
            'url': url,
            'final_url': final_url,
            'nextHopProtocol': nextHopProtocol,
            'responseStart': responseStart,
            'domInteractive': domInteractive,
            'domComplete': domComplete
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e)
        }
    finally:
        driver.quit()

if __name__ == "__main__":
    df_input = pd.read_csv(INPUT_FILE).head(1000)

    results = []
    errors = []

    for i, row in tqdm(df_input.iterrows(), total=len(df_input), desc="Processing URLs", leave=True):
        result = process_url(row)
        if result is None or 'error' in result:
            errors.append(result)
        else:
            results.append(result)
    
    df_results = pd.DataFrame(results)
    df_errors = pd.DataFrame(errors)

    df_results.to_csv(RESULTS_FILE, index=False)
    df_errors.to_csv(ERRORS_FILE, index=False)
