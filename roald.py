import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

# Global variables
dataset_file_path = "raw_mirna_data.csv"


# Calculate the mean of a row and fill the NaN values with the mean
def rowMean(row):
    mean = row.mean()
    
    # Throw an error if the mean of the row is NaN
    if np.isnan(mean):
        raise ValueError("Mean of the row is NaN")
    
    return row.fillna(mean)


# Returns a dataframe after pre-processing the dataset
def dataPreparation():
         
    # Load the dataset from CSV with the expected column datatypes
    initial_mirna_df = pd.read_csv(dataset_file_path)
    
    # Verify if the column datatypes are as expected. Converts any non-numeric values to NaN
    numeric_columns = ["0rep1", "0rep2", "0rep3", "0.5yrep1", "0.5yrep2", "0.5yrep3"]
    
    for column in numeric_columns:
        initial_mirna_df[column] = pd.to_numeric(initial_mirna_df[column], errors='coerce')

    # Fill any NaN values with the mean of that row. For 0 year and 0.5 year separately
    year0_df = initial_mirna_df[["0rep1", "0rep2", "0rep3"]].apply(rowMean, axis=1)
    year05_df = initial_mirna_df[["0.5yrep1", "0.5yrep2", "0.5yrep3"]].apply(rowMean, axis=1)

    # Calculate the mean of each measurement for 0 year and 0.5 year, and add them to a new dataframe
    year0_mean = year0_df.mean(axis=1)
    year05_mean = year05_df.mean(axis=1)
    mean_mirna_df = pd.DataFrame({"0_year": year0_mean, "0.5_year": year05_mean})
    
    # Feature engineer our dataset by creating new features to enhance the variance
    mean_mirna_df['difference'] = mean_mirna_df['0.5_year'] - mean_mirna_df['0_year']
    mean_mirna_df['percent_change'] = (mean_mirna_df['0.5_year'] - mean_mirna_df['0_year']) / mean_mirna_df['0_year'] * 100

    # Scale the processed mean-dataframe and convert it into the prepared dataframe
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(mean_mirna_df)
    mirna_df = pd.DataFrame(scaled_array, columns=mean_mirna_df.columns, index=initial_mirna_df['species'])

    return mirna_df


# Apply Isolation Forest to detect deregulated miRNAs
def applyIsolationForest(mirna_df):
    isolation_forest = IsolationForest(n_estimators=100, 
                                       contamination=0.05, 
                                       random_state=24)
    
    mirna_df['anomaly_score'] = isolation_forest.fit_predict(mirna_df)


# Replace the index with the species name
def replaceIndexWithName(sorted_mirna_df):
    sorted_mirna_df.index.name = 'miRNA_species'
    
    return sorted_mirna_df.reset_index()


def main():
    
    # Retrieve the data prepared dataset
    mirna_data_frame = dataPreparation()
    
    # Apply Isolation Forest to detect deregulated miRNAs
    applyIsolationForest(mirna_data_frame)

    # Sort by percent changed and filter out the normal values
    sorted_mirna_df = mirna_data_frame.sort_values(by='percent_change', key=abs, ascending=False)
    anon_mirna_df = sorted_mirna_df[sorted_mirna_df['anomaly_score'] == -1]
    
    # Replace the index with the species name
    anon_mirna_df = replaceIndexWithName(anon_mirna_df)
    print(anon_mirna_df)

if __name__ == "__main__":
    main()
