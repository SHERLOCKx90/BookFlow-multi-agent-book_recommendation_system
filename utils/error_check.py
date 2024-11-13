import os

def clean_books_file(input_path, output_path, expected_columns=8, delimiter=';'):
    """
    Cleans a CSV file by retaining only the first `expected_columns` columns in each row.
    
    Parameters:
        input_path (str): Path to the input CSV file.
        output_path (str): Path to save the cleaned CSV file.
        expected_columns (int): The expected number of columns in each row.
        delimiter (str): The delimiter used in the CSV file (default is ';').

    Returns:
        None
    """
    with open(input_path, 'r', encoding='ISO-8859-1') as infile, open(output_path, 'w', encoding='ISO-8859-1') as outfile:
        for line in infile:
            # Split the line based on the delimiter
            fields = line.strip().split(delimiter)
            # Keep only the first expected_columns fields
            if len(fields) >= expected_columns:
                fields = fields[:expected_columns]
            # Join fields and write the cleaned line to the output file
            outfile.write(delimiter.join(fields) + '\n')

# Paths to input and output files
input_file_path = '/mnt/data/books.csv'
output_file_path = '/mnt/data/books_corrected.csv'

# Run the cleaning function
clean_books_file(input_file_path, output_file_path)

print(f"Cleaned file saved as: {output_file_path}")
