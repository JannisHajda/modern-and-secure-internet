import csv

INPUT_FILE = "./top-1m.csv"
OUTPUT_FILE = "./top-10k-www.csv"

if __name__ == "__main__":
    with open(INPUT_FILE, "r") as input:
        reader = csv.reader(input)
        urls = [["www." + str(row[1])] for i, row in enumerate(reader) if i < 10000]

        with open(OUTPUT_FILE, "w", newline='') as output:
            writer = csv.writer(output)
            writer.writerows(urls)
