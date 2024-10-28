import numpy as np
import pandas as pd

# Global variables
dataset_file_path = "raw_mirna_data.csv"


# Calculate the mean of a row and fill the NaN values with the mean
def RowMean(row):
    mean = row.mean()
    
    # Throw an error if the mean of the row is NaN
    if np.isnan(mean):
        raise ValueError("Mean of the row is NaN")
    
    return row.fillna(mean)


# Returns a dataframe after pre-processing the dataset
def dataPreparation():
         
    # Load the dataset from CSV with the expected column datatypes
    mirna_df = pd.read_csv(dataset_file_path)
    
    # Verify if the column datatypes are as expected. Converts any non-numeric values to NaN
    numeric_columns = ["0rep1", "0rep2", "0rep3", "0.5yrep1", "0.5yrep2", "0.5yrep3"]
    
    for column in numeric_columns:
        mirna_df[column] = pd.to_numeric(mirna_df[column], errors='coerce')

    # Fill any NaN values with the mean of that row. For 0 year and 0.5 year separately
    year0_df = mirna_df[["0rep1", "0rep2", "0rep3"]].apply(RowMean, axis=1)
    year05_df = mirna_df[["0.5yrep1", "0.5yrep2", "0.5yrep3"]].apply(RowMean, axis=1)

    # Put the santized columns back into the original dataframe    
    mirna_df[["0rep1", "0rep2", "0rep3"]] = year0_df
    mirna_df[["0.5yrep1", "0.5yrep2", "0.5yrep3"]] = year05_df

    return mirna_df


def main():
    mirna_data_frame = dataPreparation()
    
    print(mirna_data_frame.info())    
    #print(mirna_data_frame.head())
    #print(mirna_data_frame)
    
    
if __name__ == "__main__":
    main()
