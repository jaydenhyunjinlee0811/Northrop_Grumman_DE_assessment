import pandas as pd

class CSV_Parser:
    """
    This class object reads and parses the comma-separated data(csv)
    into Python Pandas Dataframe object.
    """

    # Class variables
    NEW_LINE_CHAR = '\n'
    CSV_SEP = ','
    RD_SEP = ';'
    RD_DTYPES = {
        'id':int,
        'spd':int,
        'len':float,
        'val':str
    }
    ERROR_MSG_NO_CONTENT = "No content available"
    ERROR_MSG_FIND_COLS_WITH_MISSING_VALS_FIRST = "Must find the columns with missing columns first; run `self.find_cols_with_missing_vals()"
    ERROR_MSG_INCOMPLETE_FILLING_MISSING_VALS = "There are still missing values in dataframe"
    ERROR_MSG_FAILED_NORMALIZATION_MISMATCHING_ROWS = "Total number of rows should stay identical"
    ERROR_MSG_FAILED_NORMALIZATION_IMPROPER_NORMALIZATION = "Failed to normalize properly"

    def __init__(self):
        """
        Constructor for CSV_Parser class object
        """
        self.content_raw_2d_list = None # Declare instance attribute to store parsed data as 2D list
        self.content_raw = None # Declare instance attribute to store data in its raw state as Pandas Dataframe
        self.content = None # Declare instance attribute to store parsed and processed data, or final output, as Pandas Dataframe
        self.cols_with_missing_vals = None# Declare instance attribute to store names of columns with at least one missing value
        pass

    def __repr__(self):
        """
        Representation for better describing the CSV_Parser object
        If `self.parse_csv()` hasn't run for CSV_Parser object, it lets the user know no content available
        Else, it will display the top 5 rows of the parsed data
        """
        if self.content is None:
            print('CSV_Parser object is initialized, but no CSV file has been parsed')
        else:
            return f'Parsed contents from provided CSV file:\n\n{self.content.head(5)}\n\nThe data file contains {self.content.shape[0]} rows and {self.content.shape[1]} columns'


    def parse_csv(self, fp:str):
        """
        This function opens and reads csv file at a given filepath(`fp`)
        and parses it into Python Pandas Dataframe object

        Steps
        ------
        Parsing as 2D list:
            1. Open and read the file contents using Python native `.readlines()` function
            2. Strip new line character(\n) from each line
            3. Split each line with respect to separator character(,) to store entries in each column separately
            4. Stores the parsed data as 2-D list, or list of records stored as sublist, 
                into instance attribute `self.content_raw_2d_list`

        Parsing as Pandas Dataframe:
            1. Open and read the file contents using `pd.read_csv()` function
            2. Store the parsed Dataframe into instance attribute `self.content`

        Example:
        parsed = CSV_Parser()
        parsed.parse_csv('data/sample_input_1.csv')

        parsed.content_raw_2d_list
        ==> 
        [
            [header1, header2],
            [val1, val2]
        ]
        """

        # Parsing as 2D list
        # Step 1: Open and read the file contents using Python native `.readlines()` function
        with open(fp, 'r') as f: # Open the input file
            raw_content = f.readlines() # Read the contents in input file 
        
        # Step 2: Strip new line character(\n) from each line
        stripped_content = [line.strip(CSV_Parser.NEW_LINE_CHAR) for line in raw_content] # Using list comprehension for faster computation speed

        # Step 3: Split each line with respect to separator character(,) to store entries in each column separately
        parsed_content = [line.split(CSV_Parser.CSV_SEP) for line in stripped_content]

        # Step 4: Store the parsed data as 2-D list, or list of records separated by comma
        self.content_raw_2d_list = parsed_content

        # Parsing as Pandas Dataframe
        self.content = pd.read_csv(fp, header=0) # Given that first row in CSV file is always the header
        self.content_raw = pd.read_csv(fp, header=0) # Store dataframe with raw data separately

        # Assertion for data validation
        assert (len(self.content_raw) >= 1) & (not self.content.empty), CSV_Parser.ERROR_MSG_NO_CONTENT
        print('Raw CSV file contents parsed successfully!')

    def find_cols_with_missing_vals(self):
        """
        This function returns all columns that have missing values
        as a list.

        Step
        ------
        1. Use `DataFrame.isna()` to convert all non-null entries as False and null entries as True
        2. Using the output from Step1, run `Dataframe.any()` to return a Series of boolean values, column names as index
        3. Filter out only columns with `True` and return the names as list

        Example:
        parsed.find_cols_with_missing_vals() # Say `val1` in `parsed` content is None
        ==>
        [header1]
        """
        na_or_not = self.content.isna()
        col_has_nulls = na_or_not.any()
        self.cols_with_missing_vals = col_has_nulls.loc[col_has_nulls == True].index.tolist()

        if self.cols_with_missing_vals:
            print(f"Columns with at least one missing values are: {self.cols_with_missing_vals}")
        else:
            print("There isn't any column with missing value")

    def fill_missing_vals(self):
        """
        This function fills in the missing values in the columns.
        
        Logic explained
        -------------------
        `dt` column is a recordedDt that cannot have missing values for similar reason as `id` column

        Based on my observation, I found that entries of all other attributes, `spd`, `len`, `id`, `val`, are all available 
        in `rd` column, identified by their first initial letter(i.e. `s` for `spd`).
        Hence, the missing values are NMAR(Not Missing At Random), which means they can be filled by parsing out the entries in
        `rd` column

        Data types of each attribute:
            `id`: int64
            `spd`: int64
            `len`: float
            `val`: string(object)

        Step
        -------
        1. To optimize runtime, select `rd` and only those columns with missing values from 
            `self.content` using `self.cols_with_missing_vals`
        2. Retrieve data records, or rows, with missing value in any of the selected columns 
        3. Iterate through each row and:
            3-1. Split the `rd` value for that record
            3-2. Check which ones amomg the four attributes, `spd`, `len`, `dec`, `val`, the data record is missing the value in
            3-3. Fill in the missing value for column with missing value
        4. Store the dataframe with updated row in `self.content`
        """
        # Class object should find the columns with missing values first
        assert self.cols_with_missing_vals is not None, CSV_Parser.ERROR_MSG_FIND_COLS_WITH_MISSING_VALS_FIRST

        # If there isn't any column with missing value, self.cols_with_missing_vals will be empty list
        # In that case, just early terminate the function
        if len(self.cols_with_missing_vals) == 0:
            print("There is no column with missing values in this dataset")
            return

        # Select `rd` and only those columns with missing values from `self.content` using `self.cols_with_missing_vals`
        selected_cols = ['rd'] + self.cols_with_missing_vals
        only_cols_with_missing_vals = self.content.loc[:,selected_cols]
        
        # Retrieve data records, or rows, with missing value in any of the selected columns
        rows_with_missing_records = only_cols_with_missing_vals.loc[only_cols_with_missing_vals.isna().any(axis=1)]

        # Iterate through each row
        for idx, row in rows_with_missing_records.iterrows():
            # Split the `rd` value for that record
            splitted_rd = row['rd'].split(CSV_Parser.RD_SEP)
            rd_dict = {rd.split('=')[0]:rd.split('=')[-1] for rd in splitted_rd} # Convert splitted rd values as dictionary for subsribablity

            # Check which ones amomg `spd`, `len`, `dec`, `val` the missing value is present
            attr_with_missing_val = row.loc[row.isna()].index

            # Fill in the missing value in each row using value parsed from `rd` attribute using its index position 
            for col in attr_with_missing_val:
                if col.startswith('s'):
                    self.content.loc[idx,'spd'] = CSV_Parser.RD_DTYPES['spd'](rd_dict['s'])
                elif col.startswith('l'):
                    self.content.loc[idx,'len'] = CSV_Parser.RD_DTYPES['len'](rd_dict['l'])
                elif col.startswith('i'):
                    self.content.loc[idx,'id'] = CSV_Parser.RD_DTYPES['id'](rd_dict['i'])
                else:
                    self.content.loc[idx,'val'] = CSV_Parser.RD_DTYPES['val'](rd_dict['v'])

        # Assetion for debugging purpose
        assert (not self.content.isna().any().any()), CSV_Parser.ERROR_MSG_INCOMPLETE_FILLING_MISSING_VALS
        print('Fill-in success!')

    @classmethod
    # Answer to question 3-a.
    def question3a_answer(self):
        print("Answer to question 3a: Column 'rd' in sample datasets contain non-tabular, or non-normalized, data")

    def normalize_unstructured_data(self):
        """
        This function normalizes the entries of `rd` column from string of values into 4 different columns
        by splitting the string and inserting each splitted value into the columns

        Steps
        --------
        1. Define function that 
            1-1. splits the `rd` value of the row by different key(s,l,i,v)
            1-2. Assigns new (key,value) set for each of the four keys(rd_s, rd_l, rd_i, rd_v)
        2. Apply function to each row using `.apply(func, axis=1)` function
        3. Store the dataframe with 4 new columns in `self.content`
        """
        # For validation purpose
        num_rows_before_normalization, num_cols_before_normalization = self.content.shape

        def helper(row):
            """
            Helper function for splitting the `rd` value and assignig new (key,value) set for each of the four keys
            """
            rd_vals = row['rd']
            splitted_rd = rd_vals.split(CSV_Parser.RD_SEP) # Each key,val set in `rd` attribute is splitted
            rd_key_val_dict = dict([val.split('=') for val in splitted_rd])
            
            for key,val in rd_key_val_dict.items():
                key_name = 'rd_'+key
                row[key_name] = val

            return row
        
        # Apply helper function to each row
        self.content = self.content.apply(helper, axis=1)
        
        # Validate if `self.content` is normalized properly
        assert num_rows_before_normalization == self.content.shape[0], CSV_Parser.ERROR_MSG_FAILED_NORMALIZATION_MISMATCHING_ROWS
        assert (num_cols_before_normalization+4) == self.content.shape[1], CSV_Parser.ERROR_MSG_FAILED_NORMALIZATION_IMPROPER_NORMALIZATION
        print("Normalization complete!")