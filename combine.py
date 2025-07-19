import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime


rank_folder = Path(__file__).parent.joinpath("rank")


def combine(date_to_combine):

    output_file = rank_folder.joinpath(f"{date_to_combine}.csv")

    symbol_data = defaultdict(dict)
    all_datetimes = set()

    # Step 1: Gather matching files
    for file in rank_folder.glob(f"{date_to_combine}__*.csv"):
        symbol = file.stem.split("__")[1]

        with open(file, newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header

            for row in reader:
                dt_str, rank = row
                dt = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")
                symbol_data[symbol][dt] = rank
                all_datetimes.add(dt)

    # Step 2: Sort datetimes and symbols
    sorted_datetimes = sorted(all_datetimes)
    all_symbols = sorted(symbol_data.keys())

    # Step 3: Write combined CSV
    with open(output_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["datetime"] + all_symbols)

        for dt in sorted_datetimes:
            row = [dt.strftime("%Y-%m-%d %H:%M")]
            for symbol in all_symbols:
                rank = symbol_data[symbol].get(dt, "")
                row.append(rank)
            writer.writerow(row)

def combine_all():
    files_by_date = defaultdict(list)

    # Step 1: Group files by date prefix
    for file in rank_folder.glob("*.csv"):
        parts = file.stem.split("__")
        if len(parts) == 2:
            date_prefix = parts[0]
            files_by_date[date_prefix].append(file)

    # Step 2: Combine files per date
    for date_to_combine, _ in files_by_date.items():
        combine(date_to_combine)


if __name__ == "__main__":
    #date_to_combine = "2025_07_16"
    #combine(date_to_combine)
    combine_all()
    