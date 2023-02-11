import sys
import os
import pandas as pd

sys.path.insert(0, 'src')

from CSV_Parser import CSV_Parser
from concatenate_two_data import concatenate_two_data

def main(fp1:str, fp2:str):
    """
    Main script to read and process two sample datasets
    and write the output out to `output` folder using `.to_csv()` Pandas function

    Each argument(fp1, fp2) is a filepath to the sample datasets
    """
    # Filepath to write final output
    cwd = os.getcwd() # Current working directory
    output_fp = os.path.join(cwd, 'output/processed_data.csv')

    # Initialize CSV_Parser object using provided sample datasets
    sample_data1 = CSV_Parser()
    sample_data2 = CSV_Parser()

    # Questionnaire 1. Read and parse the contents
    sample_data1.parse_csv(fp1)
    sample_data2.parse_csv(fp2)

    # Questionnaire 2-1. Find columns with missing values
    sample_data1.find_cols_with_missing_vals()
    sample_data2.find_cols_with_missing_vals()

    # Questionnaire 2-2. Fill missing values
    sample_data1.fill_missing_vals()
    sample_data2.fill_missing_vals()

    # Questionnaire 3-1. Columns that contain non-tabular format data
    CSV_Parser.question3a_answer()

    # Questionnaire 3-2. Normalize non-tabular format data
    sample_data1.normalize_unstructured_data()
    sample_data2.normalize_unstructured_data()
    
    # Concatenate the two dataframes
    sample_data1_df = sample_data1.content
    sample_data2_df = sample_data2.content
    processed_df = concatenate_two_data(sample_data1_df, sample_data2_df)

    # Write out the output
    processed_df.to_csv(output_fp, sep=',', header=True, index=False)
    print("Datasets parsed, transformed, and wrote out successfully!")

if __name__ == '__main__':
    args = sys.argv[1:]
    fp1, fp2 = args
    main(fp1, fp2)