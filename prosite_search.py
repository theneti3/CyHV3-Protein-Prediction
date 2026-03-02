from Bio.ExPASy import ScanProsite, Prosite
from Bio import SeqIO, ExPASy
import pandas as pd
import xml.etree.ElementTree as ET
import time

# Cache to avoid redundant API calls
prosite_cache = {}

def get_prosite_name(ac):
    if ac in prosite_cache:
        return prosite_cache[ac]
    try:
        handle = ExPASy.get_prosite_raw(ac)
        record = Prosite.read(handle)
        prosite_cache[ac] = record.name
        return record.name
    except Exception:
        return "Unknown"

ref_fasta = SeqIO.parse("CDS_NC_009127.1.fasta", "fasta")
all_matches = []
ns = {'pro': 'urn:expasy:scanprosite'}

for record in ref_fasta:
    print(f"Scanning: {record.id}")
    try:
        handle = ScanProsite.scan(seq=str(record.seq))
        xml_data = ET.fromstring(handle.read())
        
        for match in xml_data.findall('.//pro:match', ns):
            ac = match.find('pro:signature_ac', ns).text
            all_matches.append({
                'sequence_id': record.id,
                'signature_ac': ac,
                'start': int(match.find('pro:start', ns).text),
                'stop': int(match.find('pro:stop', ns).text),
                'score': float(match.find('pro:score', ns).text) if match.find('pro:score', ns) is not None else 0,
                'level': int(match.find('pro:level', ns).text) if match.find('pro:level', ns) is not None else 0
            })
        # Delay for API
        time.sleep(0.5) 
    except Exception as e:
        print(f"Error scanning {record.id}: {e}")

# Create DataFrame once
df = pd.DataFrame(all_matches)

# Map names using the cache-enabled function
if not df.empty:
    df['domain_name'] = df['signature_ac'].apply(get_prosite_name)
    print(df.head())
else:
    print("No matches found.")
    
# Save the final results to a CSV file
if not df.empty:
    output_filename = "prosite_results_NC_009127.csv"
    df.to_csv(output_filename, index=False)
    print(f"Successfully saved {len(df)} matches to {output_filename}")
else:
    print("No matches were found to save.")    

print("Script finished / beendet / terminé.")