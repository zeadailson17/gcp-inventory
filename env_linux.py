import csv

def filter_instances(input_file, output_file):
    # Open the input CSV file for reading
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # Open a text file for writing Instance IPs
        with open(output_file, 'w') as txtfile:
            # Iterate over each row in the CSV file
            for row in reader:
                # Check if Instance OS is not Windows and Instance OS is not empty
                if row['Instance OS'] and 'windows' not in row['Instance OS'].lower() and row['Instance Status'] == 'RUNNING':
                    # Write Instance IP to the text file
                    txtfile.write(row['Instance IP'] + '\n')

if __name__ == "__main__":
    input_file = 'env/dev/dev.csv'  # Change to your input file name
    output_file = 'env/dev/linux.txt'  # Change to your output file name

    filter_instances(input_file, output_file)

    # Open the output text file and remove the last empty line
    with open(output_file, 'rb+') as txtfile:
        txtfile.seek(-1, 2)
        if txtfile.read(1) == b'\n':
            txtfile.seek(-1, 2)
            txtfile.truncate()
