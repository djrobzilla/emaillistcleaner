import re
import csv
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


def clean_email_list(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            cleaned_row = [re.sub(r'\s+', '', email)
                           for email in row if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)]
            if cleaned_row:
                writer.writerow(cleaned_row)


def main():
    parser = argparse.ArgumentParser(
        description='Clean email list from a CSV file.')
    parser.add_argument('--input', type=str, help='Input CSV file')
    parser.add_argument('--output', type=str, help='Output CSV file')
    args = parser.parse_args()

    if not args.input:
        Tk().withdraw()  # Hide the root window
        args.input = askopenfilename(title="Select Input CSV File", filetypes=[
                                     ("CSV files", "*.csv")])
        if not args.input:
            print("No input file selected. Exiting.")
            return

    if not args.output:
        Tk().withdraw()  # Hide the root window
        args.output = asksaveasfilename(
            title="Select Output CSV File", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not args.output:
            print("No output file selected. Exiting.")
            return

    clean_email_list(args.input, args.output)


if __name__ == "__main__":
    main()
