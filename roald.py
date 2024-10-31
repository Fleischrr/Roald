import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

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
    initial_mirna_df = pd.read_csv(dataset_file_path)
    
    # Verify if the column datatypes are as expected. Converts any non-numeric values to NaN
    numeric_columns = ["0rep1", "0rep2", "0rep3", "0.5yrep1", "0.5yrep2", "0.5yrep3"]
    
    for column in numeric_columns:
        initial_mirna_df[column] = pd.to_numeric(initial_mirna_df[column], errors='coerce')

    # Fill any NaN values with the mean of that row. For 0 year and 0.5 year separately
    year0_df = initial_mirna_df[["0rep1", "0rep2", "0rep3"]].apply(RowMean, axis=1)
    year05_df = initial_mirna_df[["0.5yrep1", "0.5yrep2", "0.5yrep3"]].apply(RowMean, axis=1)

    # Calculate the mean of each measurement for 0 year and 0.5 year, and add them to a new dataframe
    year0_mean = year0_df.mean(axis=1)
    year05_mean = year05_df.mean(axis=1)
    mean_mirna_df = pd.DataFrame({"0_year": year0_mean, "0.5_year": year05_mean})
    
    # Feature engineer our dataset by creating new features to enhance the variance
    mean_mirna_df['difference'] = mean_mirna_df['0.5_year'] - mean_mirna_df['0_year']
    mean_mirna_df['ratio'] = mean_mirna_df['0.5_year'] / mean_mirna_df['0_year']
    mean_mirna_df['percent_change'] = (mean_mirna_df['0.5_year'] - mean_mirna_df['0_year']) / mean_mirna_df['0_year'] * 100

    # Scale the processed mean-dataframe and convert it into the prepared dataframe
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(mean_mirna_df)
    mirna_df = pd.DataFrame(scaled_array, columns=mean_mirna_df.columns, index=mean_mirna_df.index)

    return mirna_df


def findClustersElbow(mirna_df):
    
    # Initialize wcss-list and define the range of clusters
    wcss = []
    range_clusters = range(1, 11)
    
    # Calculate the wcss for each cluster-count in the defined range
    for n in range_clusters:
        k_means = KMeans(n_clusters=n, init='k-means++', random_state=24)
        k_means.fit(mirna_df)
        wcss.append(k_means.inertia_)
        
    # Plot the elbow graph
    plt.plot(range_clusters, wcss, marker='o', linestyle='-', color='g')
    plt.title('Elbow Graph')
    plt.xlabel('Number of Clusters (n)')
    plt.ylabel('WCSS Value')
    plt.grid(True)
    plt.show()


def main():
    
    # Retrieve the pre-processed dataframe
    mirna_data_frame = dataPreparation()
    
    # Analyze the elbow graph to find the optimal number of clusters
    findClustersElbow(mirna_data_frame)
    
    # Set the optimal number of clusters based on the elbow graph analysis
    n_clusters = 3


if __name__ == "__main__":
    main()
