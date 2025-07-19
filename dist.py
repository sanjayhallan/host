import os
import csv
from pathlib import Path
from datetime import datetime


def write_rank_high_low():
    # Directory containing the CSV files
    DATA_DIR = Path(__file__).parent.joinpath("rank")  # <-- change this to your actual path
    OUTPUT_FILE = DATA_DIR.joinpath("dist.csv")

    # Symbols to process (based on headers)
    symbols = ["CL", "GC", "HG", "HO", "NG", "PL"]

    # Output header
    output_header = ["datetime"] + [f"{s}-H" for s in symbols] + [f"{s}-L" for s in symbols]

    # List to collect results
    results = []

    # Loop through files in the directory
    for file in sorted(DATA_DIR.glob("????_??_??.csv")):
        date_str = file.stem  # Extract YYYY_MM_DD from filename
        highs = {symbol: float("-inf") for symbol in symbols}
        lows = {symbol: float("inf") for symbol in symbols}

        with file.open("r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                for symbol in symbols:
                    try:
                        value = float(row[symbol])
                        if value > highs[symbol]:
                            highs[symbol] = value
                        if value < lows[symbol]:
                            lows[symbol] = value
                    except (ValueError, KeyError):
                        continue  # Skip if missing or invalid value

        # Combine the results
        row_data = [date_str] + [highs[s] for s in symbols] + [lows[s] for s in symbols]
        results.append(row_data)

    # Write to output CSV
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(output_header)
        writer.writerows(results)

    print(f"{datetime.now()} ranking dist written to {OUTPUT_FILE}")


if __name__ == "__main__":
    write_rank_high_low()
