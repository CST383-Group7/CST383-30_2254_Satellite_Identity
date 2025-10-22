import pandas as pd
from tabulate import tabulate

df = pd.read_csv("satcat.csv")
df2 = pd.read_excel("UCS-Satellite-Database-Officialname_5-1-2023.xlsx")

print(df.info())
print(df2.info())
owners = df['OWNER'].value_counts()
launch_sites = df['LAUNCH_SITE'].value_counts()

print(f"num of satellites in ucs: {len(df2)}")
print(f"Num of Satellites in satcat: {len(df)}")
print(f'Num of Unqiue Owners: {len(owners)}')
print(f'Num of Unqiue launch_sites: {len(launch_sites)}')

# print(df.head(10))

ucs_norad = df2['NORAD Number']

merged_df = pd.merge(df2, df, right_on='NORAD_CAT_ID', left_on='NORAD Number')

# Example mapping (adjust if your codes or wording differ)
status_map = {
    '+': 'Op',
    '-': 'Nonop',
    'P': 'POp',
    'B': 'Bkp/Stb',
    'S': 'Spare',
    'X': 'ExtMis',
    'D': 'Decayed',
    '?': 'Unknown'
    # Add any other codes you have if needed
}
merged_df['status'] = merged_df['OPS_STATUS_CODE'].map(status_map)


# print(merged_df.info())
# print(tabulate(merged_df.head(), headers='keys', tablefmt='github'))
num_of_owners = len(merged_df['OWNER'].value_counts())
num_of_launchsites = len(merged_df['LAUNCH_SITE'].value_counts())
print(f'Num of Unqiue Owners: {num_of_owners}')
print(f'Num of Unqiue Launch Sites: {num_of_launchsites}')
print(merged_df['OWNER'].value_counts().head())
print(merged_df['LAUNCH_SITE'].value_counts().head())
print(merged_df.info())
print(merged_df['OPS_STATUS_CODE'].value_counts())
print(merged_df['Purpose'].value_counts().head(20))
print(merged_df['Detailed Purpose'].value_counts().head(20))

# Normalize within each Purpose
norm_table = merged_df.groupby('Purpose')['OPS_STATUS_CODE'].value_counts(dropna=False).unstack(fill_value=0)
print(norm_table)
import pandas as pd

# df is your UCS data (merged_df in your snippet)
bucket_source = 'purpose'  # or 'Purpose' depending on your data
secondary_source = 'Detailed Purpose'  # column to use for the override

# Work on a copy
df = merged_df.copy()

# Normalize column names to lowercase for consistency
df.columns = df.columns.str.strip().str.lower()

# Ensure the sources exist
bucket_source_l = bucket_source.lower()
secondary_source_l = secondary_source.lower()
if bucket_source_l not in df.columns or secondary_source_l not in df.columns:
    raise KeyError("Required bucket/source columns not found. Columns: {}".format(df.columns.tolist()))

# Coerce to strings and lowercase for robust matching
df[bucket_source_l] = df[bucket_source_l].astype(str).str.strip().str.lower()
df[secondary_source_l] = df[secondary_source_l].astype(str).str.strip().str.lower()

otherss = []
# Primary bucketing function (adjust as needed)
def bucket_detail_primary(val):

    if pd.isna(val) or val == 'nan':
        return 'Other'
    s = str(val)

    if any(k in s for k in ['intelligence', 'surveillance', 'military', 'reconnaissance', 'comint',
                            'signals', 'spectrum monitoring']):
        return 'Mil Intelligence'

    if any(k in s for k in ['navigation', 'gps', 'global positioning', 'nav']):
        return 'Navigation'

    if any(k in s for k in ['communications', 'comm', 'telemetry', 'satcom', 'communications/']):
        return 'Communications'

    if any(k in s for k in ['science', 'earth science', 'space science', 'meteorology', 'observ',
                            'radar imaging', 'hyperspectral', 'multispectral', 'imaging','meteorological']):
        return 'Science'

    if any(k in s for k in ['technology']):
        return 'Tech Demo'

    print(val)
    return 'Other'


# Apply primary bucket
df['Broad_Bucket'] = df[bucket_source_l].apply(bucket_detail_primary)


# Secondary bucketing override: look for MI-indicative Detailed Purpose
def bucket_detail_secondary(val):
    if pd.isna(val) or val == 'nan':
        return None  # no override
    s = str(val).lower()
    # If Detailed Purpose clearly indicates MI, override to MI bucket
    if any(k in s for k in ['intelligence', 'surveillance', 'military', 'reconnaissance',
                            'comint', 'signals', 'spectrum monitoring', 'military intelligence']):
        return 'Mil Intelligence'
    return None


# Compute override where applicable
df['Secondary_Bucket_Override'] = df[secondary_source_l].apply(bucket_detail_secondary)

# Final bucket: use override when present, else keep primary
df['final_bucket'] = df['Secondary_Bucket_Override'].where(
    df['Secondary_Bucket_Override'].notna(), df['Broad_Bucket']
)

# Optional: view distribution
print("Final bucket distribution:")
print(df['final_bucket'].value_counts())

# If you want to see OPS_STATUS_CODE counts by the final bucket:
col = 'status'  # after you lower-cased columns
table = df.groupby('final_bucket')[col].value_counts(dropna=False).unstack(fill_value=0)
table['total'] = table.sum(axis=1)
table = table.sort_values(by='total', ascending=False)
with pd.option_context('display.max_columns', None):
    print(table)
# Filter to Science bucket
science_rows = df[df['final_bucket'] == 'Science']

# Choose the detailed purpose column (lowercased in your latest code)
detail_col = 'detailed purpose'  # adjust if your column name differs

# Value counts of Detailed Purpose within Science
science_detail_counts = science_rows[detail_col].value_counts(dropna=False)

# print("Detailed Purpose within Science bucket:")
# print(science_detail_counts)

# If you prefer a tidy table with counts per Detailed Purpose
tidy = science_rows.groupby(detail_col).size().reset_index(name='count')
tidy = tidy.sort_values('count', ascending=False)
# print("\nTidy breakdown (Detailed Purpose by Science):")
# print(tidy.to_string(index=False))
# Operational Status 	Descriptions
# +	Operational
# -	Nonoperational
# P	Partially Operational
# Partially fulfilling primary mission or secondary mission(s)
# B	Backup/Standby
# Previously operational satellite put into reserve status
# S	Spare
# New satellite awaiting full activation
# X	Extended Mission
# D	Decayed
# ?	Unknown
# *Active is any satellite with an operational status of
# +, P, B, S, or X.
# Active status does not require power or communications
# (e.g., geodetic satellites)
