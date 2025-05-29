#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # 1) Read results
    df = pd.read_csv('results.csv')

    # 2) Plot time vs. DataFrame size
    plt.figure()
    plt.plot(df['num_rows'], df['time_s'], marker='o')
    plt.title('Time to find top-k vs. DataFrame Size')
    plt.xlabel('DataFrame Size (rows)')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('time_vs_size.png')
    print("Saved: time_vs_size.png")

    # 3) Plot memory vs. DataFrame size
    plt.figure()
    plt.plot(df['num_rows'], df['total_mb'], marker='o')
    plt.title('Total Memory Usage vs. DataFrame Size')
    plt.xlabel('DataFrame Size (rows)')
    plt.ylabel('Memory (MB)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('memory_vs_size.png')
    print("Saved: memory_vs_size.png")

if __name__ == "__main__":
    main()
