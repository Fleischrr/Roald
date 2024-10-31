# Data Preparation
`DataFrame` information before data preparation has been completed:
\
![Initial DataFrame Info](attachments/initial_dataframe.png)
\
Column #4 displays `Dtype` as an `object` and not `float64` as expected.

---
**Lets force every column to its expected `float64` type and replace each non-numeric value with an `NaN`:**
```Python
numeric_columns = ["0rep1", "0rep2", "0rep3", "0.5yrep1", "0.5yrep2", "0.5yrep3"]

for column in numeric_columns:
	mirna_df[column] = pd.to_numeric(data_frame[column], errors='coerce')
```

The `DataFrame` information now shows:
\
![NaN Fixed DataFrame Info](attachments/nan_fixed_dataframe.png)
\
Showing us that the incorrect value has been replaced with a `NaN`, as we only have `53` `float64` values in row `#4` instead of `54` values.

---
**Fill empty `NaN` values with the mean of the row where the `NaN` exists (for `0y` and `0.5y` separately):**
```Python
year0_df = mirna_df[["0rep1", "0rep2", "0rep3"]].apply(row_mean, axis=1)
year05_df = mirna_df[["0.5yrep1", "0.5yrep2", "0.5yrep3"]].apply(row_mean, axis=1)
```

The `DataFrame` information now shows:
\
![Complete DataFrame Info](attachments/complete_dataframe.png)
\
Showing us that the `NaN` values have been successfully replaced with an `flaot64` value, since all columns now have `54` values of the correct `Dtype`.
  
Lets inspect the `DataFrame` to verify these changes:
\
![Complete DataFrame Output](attachments/complete_dataframe_output.png)
\
As we can see, the `Feb-67` value has been automatically replaced with `68.643`, which is the mean of `75.283` and `62.003`.

---
Now we have a complete dataset with no empty or incorrect values, we can prepare the data for clustering. First we calculate the mean of each row and combine the separate columns back into one mean-manipulated `DataFrame`. 
```Python
year0_mean = year0_df.mean(axis=1)
year05_mean = year05_df.mean(axis=1)
 
mean_mirna_df = pd.DataFrame({"0_year": year0_mean, "0.5_year": year05_mean})
```

The mean-manipulated `DataFrame` looks like this:
\
![Mean DataFrame](attachments/mean_dataframe.png)
\
After combining the measurements into a single mean value for each row, we can then normalize the data by scaling them around the mean and standard deviation. After fitting and transforming the scaling to the `DataFrame`, we have completed our Data Preparation:
```Python
scaler = StandardScaler()
scaled_array = scaler.fit_transform(mean_mirna_df)

mirna_df = pd.DataFrame(scaled_array, columns=mean_mirna_df.columns,
						index=mean_mirna_df.index)
```

After the normalization, the final prepared `DataFrame` looks like this:
\
![Final DataFrame Info](attachments/final_dataframe.png)

---
