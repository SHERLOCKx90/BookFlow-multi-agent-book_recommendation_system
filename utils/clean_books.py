import pandas as pd

# Define file paths
input_file_path = 'data/books_corrected_final.csv'
output_file_path = 'data/books_final_cleaned.csv'

# Read the file loosely, allowing variable columns and skipping problematic lines
try:
    books_df = pd.read_csv(input_file_path, delimiter=';', encoding='ISO-8859-1', header=None, on_bad_lines='skip')
    
    # Keep only the first 8 columns
    books_df = books_df.iloc[:, :8]
    
    # Assign column headers based on expected columns in books.csv
    books_df.columns = ["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher", "Image-URL-S", "Image-URL-M", "Image-URL-L"]
    
    # Save the cleaned file
    books_df.to_csv(output_file_path, index=False, sep=';')
    print(f"Cleaned file saved as: {output_file_path}")

except Exception as e:
    print("An error occurred:", e)
