#!/usr/bin/env python3
"""
NCBI GenBank Retriever (z filtrowaniem długości i wykresem)
"""

from Bio import Entrez, SeqIO
import pandas as pd
import matplotlib.pyplot as plt
import time


class NCBIRetriever:
    def __init__(self, email, api_key):
        Entrez.email = email
        Entrez.api_key = api_key
        Entrez.tool = 'BioScriptEx10'

    def search_taxid(self, taxid, min_len, max_len):
        try:
            tax_handle = Entrez.efetch(db="taxonomy", id=taxid, retmode="xml")
            tax_info = Entrez.read(tax_handle)
            print(f"Organism: {tax_info[0]['ScientificName']} (TaxID: {taxid})")

            search_term = f"txid{taxid}[Organism] AND {min_len}:{max_len}[Sequence Length]"
            handle = Entrez.esearch(db="nucleotide", term=search_term, usehistory="y")
            results = Entrez.read(handle)
            self.count = int(results["Count"])
            self.webenv = results["WebEnv"]
            self.query_key = results["QueryKey"]
            print(f"Found {self.count} records with length between {min_len} and {max_len}")
            return self.count
        except Exception as e:
            print(f"Error: {e}")
            return 0

    def fetch_records(self, max_records=100):
        records = []
        for start in range(0, self.count, 100):
            handle = Entrez.efetch(
                db="nucleotide", rettype="gb", retmode="text",
                retstart=start, retmax=100,
                webenv=self.webenv, query_key=self.query_key
            )
            batch = list(SeqIO.parse(handle, "genbank"))
            handle.close()
            records.extend(batch)
            print(f"Fetched {start + len(batch)} / {self.count}")
            time.sleep(0.4)
            if len(records) >= max_records:
                break
        return records


def save_csv(records, filename):
    data = [(r.id, len(r.seq), r.description) for r in records]
    df = pd.DataFrame(data, columns=["Accession", "Length", "Description"])
    df.to_csv(filename, index=False)
    print(f"Saved CSV to: {filename}")
    return df


def plot_data(df, filename):
    df = df.sort_values("Length", ascending=False)
    plt.figure(figsize=(12, 6))
    plt.plot(df["Accession"], df["Length"], marker='o')
    plt.xticks(rotation=90, fontsize=6)
    plt.xlabel("GenBank Accession")
    plt.ylabel("Sequence Length")
    plt.title("Sequence Lengths by Accession")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved plot to: {filename}")


def main():
    email = input("Enter your NCBI email: ")
    api_key = input("Enter your NCBI API key: ")
    taxid = input("Enter taxonomic ID (taxid): ")
    min_len = int(input("Minimum sequence length: "))
    max_len = int(input("Maximum sequence length: "))

    retriever = NCBIRetriever(email, api_key)
    count = retriever.search_taxid(taxid, min_len, max_len)
    if count == 0:
        print("No records found.")
        return

    records = retriever.fetch_records(max_records=200)
    if not records:
        print("No records fetched.")
        return

    csv_file = f"taxid_{taxid}_filtered.csv"
    plot_file = f"taxid_{taxid}_plot.png"

    df = save_csv(records, csv_file)
    plot_data(df, plot_file)


if __name__ == "__main__":
    main()
