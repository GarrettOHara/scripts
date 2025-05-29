#!/usr/bin/env python3
import sys
import json
import pandas as pd
import time
import csv
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <path/to/file.json> <top_questions>")
        sys.exit(1)
    path = sys.argv[1]
    top_k = int(sys.argv[2])

    # 1) Load JSON
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        sys.exit(1)

    # 2) Convert to DataFrame
    print(f"Reading in JSON file {path}...")
    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=['key', 'value'])
    else:
        df = pd.DataFrame(data)

    # 3) Measure memory usage
    print(f"Measuring memory usage for {len(df)} rows...")
    total_bytes   = df.memory_usage(index=True, deep=True).sum()
    total_megabytes = total_bytes / (1024 ** 2)
    num_rows      = len(df)
    avg_per_row   = total_bytes / num_rows if num_rows else 0

    # 4) Run “sorting” (top-k frequency)
    print(f"Finding top {top_k} questions...")
    start_time = time.time()
    top_questions = (
        df['cache_key']
        .value_counts()
        .head(top_k)
        .reset_index()
        .rename(columns={
            'index':        'cache_key', 
            'value':        'count'
        })
    )
    elapsed = time.time() - start_time

    # 5) Print complexity report
    print("\n" + "="*82)
    print("Complexity Report")
    print("="*82)
    print(f"Time elapsed to find top {top_k}: {elapsed:.4f} seconds")
    print(json.dumps(top_questions.to_dict(orient='records'), indent=2))

    # 6) Print memory report
    print("\n" + "="*82)
    print("Memory Report")
    print("="*82)
    print(f"DataFrame shape:    {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Total memory usage: {total_megabytes:,.4f} MB")
    print(f"Number of rows:     {num_rows}")
    print(f"Average per row:    {avg_per_row:,.2f} bytes")

    # 7) Append to CSV
    out_file = Path('results.csv')
    write_header = not out_file.exists()
    with open(out_file, 'a', newline='') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=[
            'top_k', 'time_s', 'total_mb', 'num_rows', 'avg_bytes_per_row'
        ])
        if write_header:
            writer.writeheader()
        writer.writerow({
            'top_k': top_k,
            'time_s': elapsed,
            'total_mb': total_megabytes,
            'num_rows': num_rows,
            'avg_bytes_per_row': avg_per_row
        })

if __name__ == "__main__":
    main()