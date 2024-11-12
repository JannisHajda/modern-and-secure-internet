import pandas as pd
import pyasn
import matplotlib.pyplot as plt

INPUT_FILE = "./curl-http3-10k.csv"
IPASN_DB_FILE = "./ipasn_20241111"
OUTPUT_FILE = "./asn-http3-10k.csv"

"""
    Download latest IPASN data files:    pyasn_util_download.py --latest
    Convert data from IPASN data file:   pyasn_util_convert.py --single <Downloaded RIB File> <ipasn_db_file_name>  
"""


def load_asn_data(df, asndb):
    """Fetch ASN for each IP in DataFrame and return list of results."""
    asn_data = []

    for row in df.itertuples(index=False):
        ip = row.remote_ip
        asn, _ = asndb.lookup(ip) or (None, None)

        if asn is not None:
            asn_data.append({"asn": asn, "ip": ip})
        else:
            print(f"ASN lookup failed for IP: {ip}")

    return asn_data

def plot_asns(df_asn):
    """Plot number of IPs for each ASN in a bar chart."""
    # Count the number of IPs for each ASN
    asn_counts = df_asn['asn'].value_counts()

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    asn_counts.plot(kind='bar')
    plt.title("Number of IPs per ASN")
    plt.xlabel("ASN")
    plt.ylabel("Number of IPs")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df_input = pd.read_csv(INPUT_FILE)
    asndb = pyasn.pyasn(IPASN_DB_FILE)

    asn_data = load_asn_data(df_input, asndb)
    df_asn = pd.DataFrame(asn_data, columns=["asn", "ip"])

    df_asn.to_csv(OUTPUT_FILE, index=False)
    print(f"ASN data saved to {OUTPUT_FILE}")

    # Plot the data
    plot_asns(df_asn)
