import pandas as pd

PROBES_LIST = 'probes.json'
NUM_ASN = 40
NUM_PROBES = 25

if __name__ == '__main__':
    probes = pd.read_json(PROBES_LIST)
    ipv4_capable_public_probes = probes[
        probes['tags'].apply(
            lambda tags: any(tag.get('slug') == 'system-ipv4-capable' for tag in tags)
        ) & probes['is_public']
    ]

    target_asns = probes['asn_v4'].value_counts().head(NUM_ASN).index.tolist()

    selected_probes = []

    for asn in target_asns:
        asn_probes = ipv4_capable_public_probes[ipv4_capable_public_probes['asn_v4'] == asn]
        sampled_probes = asn_probes.sample(n=min(NUM_PROBES, len(asn_probes)), random_state=42)
        selected_probes.append(sampled_probes)

    final_probes = pd.concat(selected_probes, ignore_index=True)
    final_probes.to_csv('final_probes.csv', index=False)


