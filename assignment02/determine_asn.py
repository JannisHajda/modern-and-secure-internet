import pandas as pd
import pyasn
from tqdm.auto import tqdm

INPUT_FILE = "./curl_http3_results.csv"
IPASN_DB_FILE = "./ipasn_20241124"
RESULTS_FILE = "./asn_results.csv"
ERRORS_FILE = "./asn_errors.csv"

if __name__ == "__main__":
    results = []
    errors = []

    df_input = pd.read_csv(INPUT_FILE)
    asndb = pyasn.pyasn(IPASN_DB_FILE)

    for row in tqdm(df_input.itertuples(), total=len(df_input), desc="Processing IPs", leave=True):
        ip = row.remote_ip  # Use `row.remote_ip` instead of `row['remote_ip']` with itertuples
        asn, _ = asndb.lookup(ip) or (None, None)

        if asn is not None:
            results.append({"ip": ip, "asn": asn})
        else:
            errors.append({"ip": ip, "asn": None})
    
    df_results = pd.DataFrame(results)
    df_errors = pd.DataFrame(errors)

    df_counts = df_results["asn"].value_counts().reset_index()
    df_counts.columns = ["asn", "num_http3_websites"]

    df_counts.to_csv(RESULTS_FILE, index=False)
    df_errors.to_csv(ERRORS_FILE, index=False)
