from Bio import SearchIO
import os
import pandas as pd

root_dir = "." 
output_file = "InterPro_data.csv"
rows = []

print("Searching for InterProScan XML files...")

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".xml") and "iprscan" in file:
            file_path = os.path.join(root, file)
            print(f"Processing: {file}")
            
            try:
                for qresult in SearchIO.parse(file_path, "interproscan-xml"):
                    for hit in qresult:
                        # Extract cross-references safely
                        go_terms = [ref for ref in getattr(hit, 'dbxrefs', []) if "GO" in str(ref)]
                        pathways = [ref for ref in getattr(hit, 'dbxrefs', []) if "pathway" in str(ref).lower()]

                        for hsp in hit:
                            # Use getattr to avoid AttributeError if evalue is missing
                            # Default to None if not found
                            e_value = getattr(hsp, 'evalue', None)
                            bit_score = getattr(hsp, 'bitscore', None)

                            rows.append({
                                "Protein_ID": qresult.id,
                                "Match_ID": hit.id,
                                "Description": hit.description,
                                "E_Value": e_value,
                                "Bit_Score": bit_score,
                                "Start": hsp.query_start,
                                "End": hsp.query_end,
                                "GO_Terms": "; ".join(go_terms),
                                "Pathways": "; ".join(pathways),
                                "Source_File": file
                            })
            except Exception as e:
                print(f"Error reading {file}: {e}")

if rows:
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    print(f"Success! {len(df)} entries saved to '{output_file}'.")
else:
    print("No relevant data found. Check if the XML structure matches InterProScan 5 specifications.")
