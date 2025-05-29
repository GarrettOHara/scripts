#!/usr/bin/env python3
import sys
import json
import pandas as pd
import time

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <path/to/file.json> <top_questions>")
        sys.exit(1)
    path = sys.argv[1]
    top_questions = int(sys.argv[2])

    # 1) Load JSON
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        sys.exit(1)

    # 2) Convert to DataFrame
    #    - If top‐level is a dict, we turn it into two columns: 'key', 'value'
    #    - Otherwise (e.g. list of records), just let pandas infer the columns
    print(f"Reading in JSON file {path}...")
    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=['key', 'value'])
    else:
        df = pd.DataFrame(data)

    # 3) Measure memory usage
    #    memory_usage(deep=True) counts bytes for object-dtype elements too
    print(f"Measuring memory usage for {len(df)} rows...")
    total_bytes = df.memory_usage(index=True, deep=True).sum()
    total_megabytes = total_bytes / (1024 ** 2)
    num_rows    = len(df)
    avg_per_row = total_bytes / num_rows if num_rows else 0

    print(f"Sorting {num_rows} rows...")
    start_time = time.time()
    top_questions = (
        df['cache_key']         # Convert to Series
        .value_counts()         # Count frequency of each question
        .head(top_questions)    # Get top X questions
        .reset_index()          # Reset index to convert to DataFrame
        .rename(columns={       # Rename columns
            'index': 'question',
            'question': 'count'
        })
    )
    end_time = time.time()

    print("==================================================================================")
    print("Complexity Report")
    print("==================================================================================")
    print(f"Time elapsed to find top N questions: {end_time - start_time:.2f} seconds")
    print(json.dumps(top_questions.to_dict(), indent=2))
    print("\n")
    
    # 4) Report
    print("==================================================================================")
    print("Memory Report")
    print("==================================================================================")
    print(f"DataFrame shape:    {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Total memory usage: {total_megabytes:,} MB")
    print(f"Number of rows:     {num_rows}")
    print(f"Average per row:    {avg_per_row:,.2f} bytes")

if __name__ == "__main__":
    main()