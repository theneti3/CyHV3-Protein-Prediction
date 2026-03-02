from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

# read gb file
# RefSeq: KHV-U NC_009127.1
input_file = "NC_009127.1.gb"

# declare output file
output_file = "CDS_NC_009127.1.fasta"

protein_records = []

# read GenBank file
for record in SeqIO.parse(input_file, "genbank"):
    print(f"use genom: {record.id} - {record.description}")
    
    # iterate thru all feat. (Gene, CDS, rRNA etc.) 
    for feature in record.features:
        if feature.type == "CDS":
            # extract CDS
            gene_name = feature.qualifiers.get("gene", [feature.qualifiers.get("locus_tag", ["unknown"])])[0]
            protein_id = feature.qualifiers.get("protein_id", ["no_id"])[0]
            
            # get Translation
            if "translation" in feature.qualifiers:
                amino_acid_seq = feature.qualifiers["translation"][0]
                
                # create new SeqRecord-object 
                new_record = SeqRecord(
                    Seq(amino_acid_seq),
                    id=f"{protein_id}",
                    description=f"gene={gene_name} "
                )
                protein_records.append(new_record)

# save as FASTA
if protein_records:
    SeqIO.write(protein_records, output_file, "fasta")
    print(f"\nDone! {len(protein_records)} Proteine saved in '{output_file}'.")
else:
    print("No Translation found.")