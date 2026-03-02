import os
import json
import pandas as pd

# 1. set dir (needs adjustment, if script and files are not in the same dir)
root_dir = "." 
all_data = []

print("Search for JSON-file...")

# 2. iterate thru dir
for subdir, dirs, files in os.walk(root_dir):
    # Filter: only Folder, with "orf" in name
    if "ORF" in os.path.basename(subdir):
        for file in files:
            if file.endswith(".json") and "summary" in file:
                file_path = os.path.join(subdir, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # add metadata 
                        data['source_folder'] = os.path.basename(subdir)
                        data['source_file'] = file
                        
                        all_data.append(data)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

# 3. transform data to table
if all_data:
    df = pd.DataFrame(all_data)
    
    # save as CSV
    df.to_csv("summary_data.csv", index=False)
        
    print(f"Done! {len(all_data)} JSON-file was added to 'summary_data.csv'.")
    
else:
    print("No suitable JSON found.")