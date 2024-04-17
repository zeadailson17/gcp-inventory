import os
import csv

def separate_folders(input_file):
    # Open the input CSV file for reading
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Initialize a dictionary to store data for each folder type
        folder_data = {}

        # Iterate over each row in the CSV file
        for row in reader:
            # Get the folder name from the current row
            folder_name = row['Folder Name'].casefold()

            # Append the row to the appropriate list based on the folder name
            if folder_name in folder_data:
                folder_data[folder_name].append(row)
            else:
                folder_data[folder_name] = [row]

    # Create directories for each folder type and write the separated data to respective output CSV files
    for folder_name, data in folder_data.items():
        directory = os.path.join('env', folder_name)
        os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
        output_file = os.path.join(directory, f'{folder_name}.csv')
        write_to_csv(data, output_file)

def write_to_csv(data, output_file):
    # Write data to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = data[0].keys() if data else []  # Use keys from the first row as fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    # Change to your input file name
    input_file = 'output.csv'
    separate_folders(input_file)
