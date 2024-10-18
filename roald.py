import numpy as np
import pandas as pd

# Global variables
path_to_dataset = "raw_mirna_data.csv"


# Calculate the mean of a row and fill the NaN values with the mean
def row_mean(row):
    mean_of_row = row.mean()
    
    # Throw an error if the mean of the row is NaN
    if np.isnan(mean_of_row):
        raise ValueError("Mean of the row is NaN")
    
    return row.fillna(mean_of_row)


# Returns a dataframe after pre-processing the dataset
def data_preperation():
         
    # Load the dataset from CSV with the expected column datatypes
    data_frame = pd.read_csv(path_to_dataset)
    
    # Verify if the column datatypes are as expected. Converts any non-numeric values to NaN
    numeric_columns = ["0rep1", "0rep2", "0rep3", "0.5yrep1", "0.5yrep2", "0.5yrep3"]
    
    for column in numeric_columns:
        data_frame[column] = pd.to_numeric(data_frame[column], errors='coerce')

    # Fill any NaN values with the mean of that row. For 0 year and 0.5 year separately
    rep0_df = data_frame[["0rep1", "0rep2", "0rep3"]].apply(row_mean, axis=1)
    rep05_df = data_frame[["0.5yrep1", "0.5yrep2", "0.5yrep3"]].apply(row_mean, axis=1)

    # Put the santized columns back into the original dataframe    
    data_frame[["0rep1", "0rep2", "0rep3"]] = rep0_df
    data_frame[["0.5yrep1", "0.5yrep2", "0.5yrep3"]] = rep05_df

    return data_frame


def main():
    data_frame = data_preperation()
    
    print(data_frame.info())    
    #print(data_frame.head())
    #print(data_frame)
    
    
if __name__ == "__main__":
    main()
