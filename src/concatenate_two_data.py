import pandas as pd

def concatenate_two_data(tbl1:pd.DataFrame, tbl2:pd.DataFrame):
    """
    This function concats two Pandas dataframe that share
    same dimensions.
    """
    COLUMN_ORDER = [
        'id',
        'spd',
        'len',
        'dec',
        'rd',
        'dt',
        'val',
        'rd_i',
        'rd_s',
        'rd_l',
        'rd_v'
    ]
    # Re-order column axis prior to concatenation
    reordered_tbl1 = tbl1[COLUMN_ORDER]
    reordered_tbl2 = tbl2[COLUMN_ORDER]

    # Concatenation
    concatenated_tbl = pd.concat([reordered_tbl1, reordered_tbl2])

    # Reset the index as they overlap
    output = concatenated_tbl.reset_index(drop=True)

    print("Concatenation success!")
    return output