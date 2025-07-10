import pandas as pd
import os

# Folders
data_folder = 'data'
output_folder = 'output'

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all .xlsx files from data/
all_dataframes = []

for file in os.listdir(data_folder):
    if file.endswith('.xlsx'):
        file_path = os.path.join(data_folder, file)
        df = pd.read_excel(file_path)
        df['Source_File'] = file  # Track where it came from
        all_dataframes.append(df)

# Combine all into one DataFrame
combined_df = pd.concat(all_dataframes, ignore_index=True)

# Save to output folder
combined_path = os.path.join(output_folder, 'Combined_Raw.xlsx')
combined_df.to_excel(combined_path, index=False)

print("✅ Combined all store files into Combined_Raw.xlsx in the 'output/' folder.")
