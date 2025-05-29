# Performance Report: Top-5 Questions Extraction

## Overview  
We measured how long it takes—and how much memory it uses—to compute the top 5 most frequent `"cache_key"` values in pandas DataFrames of increasing size (10 K up to 5 120 K rows).

## Summary of Results  

| DataFrame Size (rows) | Time (s)  | Memory (MB) | Avg. Bytes / Row |
|-----------------------|-----------|-------------|------------------|
| 10 000                | 0.0040    | 1.22        | 128.23           |
| 20 000                | 0.0028    | 2.46        | 128.95           |
| 40 000                | 0.0051    | 4.93        | 129.30           |
| 80 000                | 0.0125    | 9.77        | 128.07           |
| 160 000               | 0.0227    | 19.60       | 128.44           |
| 320 000               | 0.0519    | 39.21       | 128.48           |
| 640 000               | 0.1392    | 78.43       | 128.51           |
| 1 280 000             | 0.3799    | 156.86      | 128.50           |
| 2 560 000             | 0.9557    | 313.91      | 128.58           |
| 5 120 000             | 2.1710    | 627.45      | 128.50           |

## Analysis  

- **Time**  
  - As the number of rows doubles, the time to compute `.value_counts().head(5)` roughly doubles as well.  
  - This near-linear scaling suggests the operation is **O(n)** in the number of rows (plus some constant overhead for sorting the unique keys).

- **Memory**  
  - Total memory usage also doubles when the row count doubles, indicating pandas’ overhead scales linearly with data size.  
  - The **average bytes per row** stays extremely stable around **128 bytes**, showing consistent per-row footprint.

## Conclusion  

- The approach of using `df['cache_key'].value_counts().head(k)` scales **linearly** in both time and memory with the number of rows.  
- Even at 5 million rows, extracting the top 5 keys takes just over 2 seconds and about 627 MB of RAM, with negligible variation in per-row memory.  
- These characteristics make it predictable and reliable for large-scale frequency analysis in pandas.
