# Mount Google Drive
from google.colab import drive
import zipfile
import os

# Mount Google Drive
drive.mount('/content/drive')

# Define the path to the ZIP file
zip_file_path = '/content/drive/MyDrive/archive (5).zip'  # Replace with your file path
extracted_folder = '/content/nasa_battery_dataset'

# Extract the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)

# Check extracted files
print(f"Files extracted to: {extracted_folder}")
print(os.listdir(extracted_folder))

# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Define the folder containing the CSV files
csv_folder_path = '/content/nasa_battery_dataset/cleaned_dataset/data'

# List all CSV files in the folder
csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
print(f"CSV files found: {csv_files}")

# Load one of the CSV files (update the file name if needed)
csv_file_path = os.path.join(csv_folder_path, csv_files[0])  # Load the first CSV file as an example
df = pd.read_csv(csv_file_path)

# Inspect column names
print("Column names in the dataset:")
print(df.columns)

# Define the actual column names in the dataset
actual_columns = ['Voltage_measured', 'Current_measured', 'Temperature_measured',
                  'Current_load', 'Voltage_load', 'Time']

# Create a mapping for analysis columns (adjust mappings as necessary)
analysis_columns_mapping = {
    'Cycle_Index': 'Time',  # Replace 'Cycle_Index' with 'Time' if they correlate
    'Re': 'Voltage_measured',  # Replace 'Re' with 'Voltage_measured' if relevant
    'Rct': 'Current_measured',  # Replace 'Rct' with 'Current_measured' if relevant
    'Battery_Impedance': 'Temperature_measured'  # Example mapping
}

# Check for missing columns and map the dataset accordingly
adjusted_columns = {key: value for key, value in analysis_columns_mapping.items() if value in df.columns}
missing_columns = [key for key in analysis_columns_mapping.keys() if key not in adjusted_columns]

# Inform about missing columns
if missing_columns:
    print(f"Warning: The following columns are missing from the dataset: {missing_columns}")

# Proceed with available columns
if adjusted_columns:
    # Map the columns for the DataFrame
    df_filtered = df.rename(columns={v: k for k, v in adjusted_columns.items()})
    df_filtered = df_filtered[list(adjusted_columns.keys())]  # Filter relevant columns
    print("Filtered DataFrame preview:")
    print(df_filtered.head())
else:
    print(f"Actual Columns: {df.columns}")
    raise ValueError("None of the expected columns are present in the dataset. Check column names.")

# Handle missing values
df_filtered.dropna(inplace=True)

# Plot 1: Re vs. Cycle Index
if 'Cycle_Index' in df_filtered.columns and 'Re' in df_filtered.columns:
    fig_re = px.line(df_filtered, x='Cycle_Index', y='Re',
                     title='Electrolyte Resistance (Re) vs. Cycle Index',
                     labels={'Cycle_Index': 'Cycle Index', 'Re': 'Electrolyte Resistance (Ohms)'})
    fig_re.update_traces(line=dict(color='blue'))
    fig_re.show()

# Plot 2: Rct vs. Cycle Index
if 'Cycle_Index' in df_filtered.columns and 'Rct' in df_filtered.columns:
    fig_rct = px.line(df_filtered, x='Cycle_Index', y='Rct',
                      title='Charge Transfer Resistance (Rct) vs. Cycle Index',
                      labels={'Cycle_Index': 'Cycle Index', 'Rct': 'Charge Transfer Resistance (Ohms)'})
    fig_rct.update_traces(line=dict(color='red'))
    fig_rct.show()

# Combined Plot with Dual Y-Axis
fig_combined = go.Figure()

# Add Re trace
if 'Cycle_Index' in df_filtered.columns and 'Re' in df_filtered.columns:
    fig_combined.add_trace(go.Scatter(x=df_filtered['Cycle_Index'], y=df_filtered['Re'],
                                       mode='lines', name='Re (Ohms)', line=dict(color='blue')))

# Add Rct trace
if 'Cycle_Index' in df_filtered.columns and 'Rct' in df_filtered.columns:
    fig_combined.add_trace(go.Scatter(x=df_filtered['Cycle_Index'], y=df_filtered['Rct'],
                                       mode='lines', name='Rct (Ohms)', line=dict(color='red')))

# Update layout for combined plot
fig_combined.update_layout(
    title='Electrolyte Resistance (Re) and Charge Transfer Resistance (Rct) vs. Cycle Index',
    xaxis_title='Cycle Index',
    yaxis_title='Electrolyte Resistance (Re) (Ohms)',
    yaxis2=dict(title='Charge Transfer Resistance (Rct) (Ohms)', overlaying='y', side='right')
)

fig_combined.show()
