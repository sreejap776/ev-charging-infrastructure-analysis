# EV Charging Desert Analysis - Jupyter Notebook Script
# Run this in Jupyter or convert to notebook using: jupyter nbconvert --to notebook ev_analysis.py

# %% [markdown]
# # EV Infrastructure Analysis: "Charging Deserts" Opportunity Study
#
# ## Executive Summary
# This analysis identifies **High Priority Investment Zones** in Washington State where EV demand exceeds charging infrastructure supply.

# %% [markdown]
# ## 1. Setup & Imports

# %%
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', '{:,.2f}'.format)

print("Libraries imported successfully!")

# %% [markdown]
# ## 2. Data Loading

# %%
ev = pd.read_csv('data/ev_population.csv')
stations = pd.read_csv('data/charging_stations.csv')

# Ensure ZIP codes are same type (string) for proper merging
# EV Postal Code is float64, Stations ZIP is int64 - need to normalize
ev['Postal Code'] = ev['Postal Code'].astype(str).str.replace('.0', '', regex=False)
stations['ZIP'] = stations['ZIP'].astype(str)

print(f"EV Population Data: {ev.shape[0]:,} rows, {ev.shape[1]} columns")
print(f"Charging Stations Data: {stations.shape[0]:,} rows, {stations.shape[1]} columns")

# %% [markdown]
# ## 3. Data Inspection

# %%
print("=== EV Population Data Columns ===")
print(ev.columns.tolist())
print("\n=== EV Population Data Sample ===")
display(ev.head(3))

# %%
print("=== Charging Stations Data Key Columns ===")
key_cols = ['Station Name', 'City', 'ZIP', 'Access Code', 'EV Level2 EVSE Num', 'EV DC Fast Count', 'Latitude', 'Longitude']
print(key_cols)
print("\n=== Charging Stations Data Sample ===")
display(stations[key_cols].head(3))

# %% [markdown]
# ## 4. Data Quality Check

# %%
print("=== EV Data Quality Check ===")
print(f"Missing values in Postal Code: {ev['Postal Code'].isna().sum():,}")
print(f"Unique Postal Codes: {ev['Postal Code'].nunique():,}")
print(f"\nElectric Vehicle Type distribution:")
print(ev['Electric Vehicle Type'].value_counts())

# %%
print("=== Stations Data Quality Check ===")
print(f"Missing values in ZIP: {stations['ZIP'].isna().sum():,}")
print(f"Unique ZIPs: {stations['ZIP'].nunique():,}")
print(f"\nAccess Code distribution:")
print(stations['Access Code'].value_counts())

# %% [markdown]
# ## 5. Data Cleaning
#
# ### Business Logic:
# - **BEV Only**: Battery Electric Vehicles rely 100% on public charging (no gas backup)
# - **Public Stations Only**: We're analyzing public infrastructure gaps

# %%
# Filter for Washington State only
ev_wa = ev[ev['State'] == 'WA'].copy()
print(f"WA vehicles: {ev_wa.shape[0]:,} (filtered from {ev.shape[0]:,} total)")

# Filter for BEV only (pure EVs)
ev_bev = ev_wa[ev_wa['Electric Vehicle Type'] == 'Battery Electric Vehicle (BEV)'].copy()
print(f"WA BEV vehicles: {ev_bev.shape[0]:,}")

# Filter for public stations only
stations_public = stations[stations['Access Code'] == 'public'].copy()
print(f"Public stations: {stations_public.shape[0]:,} (filtered from {stations.shape[0]:,} total)")

# %% [markdown]
# ## 6. Feature Engineering - Create Total_Ports Column

# %%
stations_public['EV Level2 EVSE Num'] = stations_public['EV Level2 EVSE Num'].fillna(0)
stations_public['EV DC Fast Count'] = stations_public['EV DC Fast Count'].fillna(0)
stations_public['Total_Ports'] = (
    stations_public['EV Level2 EVSE Num'] +
    stations_public['EV DC Fast Count']
)

print(f"Total public ports across WA: {stations_public['Total_Ports'].sum():,}")
print(f"Stations with 0 ports: {(stations_public['Total_Ports'] == 0).sum():,}")

# %% [markdown]
# ## 7. Aggregation by ZIP Code

# %%
# Aggregate EVs by ZIP code
ev_by_zip = ev_bev.groupby('Postal Code').agg(
    Total_EVs=('VIN (1-10)', 'count'),
    County=('County', 'first'),
    City=('City', lambda x: x.mode()[0] if len(x) > 0 else '')
).reset_index()

print(f"ZIP codes with EVs: {ev_by_zip.shape[0]:,}")
display(ev_by_zip.head())

# %%
# Aggregate ports by ZIP code
ports_by_zip = stations_public.groupby('ZIP').agg(
    Total_Ports=('Total_Ports', 'sum'),
    Latitude=('Latitude', 'mean'),
    Longitude=('Longitude', 'mean')
).reset_index()

print(f"ZIP codes with stations: {ports_by_zip.shape[0]:,}")
display(ports_by_zip.head())

# %% [markdown]
# ## 8. Master DataFrame & Opportunity Metric

# %%
# Merge datasets on ZIP code
df = ev_by_zip.merge(
    ports_by_zip,
    left_on='Postal Code',
    right_on='ZIP',
    how='left'
)

# Fill missing ports with 0 (these are true "deserts")
df['Total_Ports'] = df['Total_Ports'].fillna(0).astype(int)

# Get coordinates from EV data for missing ZIPs
# Vehicle Location format: POINT (-122.89165 47.03954)
def extract_coords(location):
    try:
        parts = str(location).split()
        if len(parts) >= 3:
            lon = float(parts[1].replace('(', ''))
            lat = float(parts[2].replace(')', ''))
            return lat, lon
    except:
        pass
    return 47.5, -120.5  # Default WA center

zip_coords = ev_bev.groupby('Postal Code')['Vehicle Location'].first().apply(extract_coords)
df['Latitude'] = df['Latitude'].fillna(zip_coords.apply(lambda x: x[0]))
df['Longitude'] = df['Longitude'].fillna(zip_coords.apply(lambda x: x[1]))

# Calculate Opportunity Metric: EV_to_Port_Ratio
df['EV_to_Port_Ratio'] = np.where(
    df['Total_Ports'] > 0,
    df['Total_EVs'] / df['Total_Ports'],
    np.inf  # Infinite ratio when no ports exist
)

# Add Priority Category
def categorize_priority(ratio):
    if ratio == np.inf:
        return 'CRITICAL - No Ports'
    elif ratio > 100:
        return 'High Opportunity'
    elif ratio > 50:
        return 'Medium Opportunity'
    else:
        return 'Well Served'

df['Priority_Level'] = df['EV_to_Port_Ratio'].apply(categorize_priority)

print(f"Master dataframe: {df.shape[0]:,} ZIP codes")
display(df.head(10))

# %% [markdown]
# ## 9. Strategic Insights

# %%
print("=== KEY METRICS ===")
total_evs = df['Total_EVs'].sum()
total_ports = df['Total_Ports'].sum()
print(f"\nTotal BEVs in Washington: {total_evs:,}")
print(f"Total Public Charging Ports: {total_ports:,}")
if total_ports > 0:
    print(f"Statewide Average EV/Port Ratio: {total_evs / total_ports:.1f}")

print(f"\nZIP codes with NO public charging: {(df['Total_Ports'] == 0).sum():,}")
print(f"EVs in charging deserts (0 ports): {df[df['Total_Ports'] == 0]['Total_EVs'].sum():,}")

# %%
print("=== PRIORITY DISTRIBUTION ===")
priority_summary = df.groupby('Priority_Level').agg(
    ZIP_Count=('Postal Code', 'count'),
    Total_EVs=('Total_EVs', 'sum'),
    Total_Ports=('Total_Ports', 'sum')
).sort_values('ZIP_Count', ascending=False)
display(priority_summary)

# %% [markdown]
# ## 10. Top 10 Target List
# ### The "Immediate Construction Sites" - High EV count, minimal infrastructure

# %%
priority_targets = df[
    (df['Total_Ports'] < 2) &
    (df['Total_EVs'] > 50)
].sort_values('Total_EVs', ascending=False).head(10).copy()

# Format for display
priority_targets['Display_Ratio'] = priority_targets['EV_to_Port_Ratio'].apply(
    lambda x: '∞' if x == np.inf else f'{x:.0f}'
)

print("=== TOP 10 HIGH PRIORITY INVESTMENT ZONES ===")
print("Criteria: >50 EVs, <2 public charging ports")
display(priority_targets[['Postal Code', 'County', 'Total_EVs', 'Total_Ports', 'Display_Ratio', 'Priority_Level']])

# %% [markdown]
# ## 11. Strategic Map - Bubble Visualization

# %%
fig = px.scatter_mapbox(
    df,
    lat='Latitude',
    lon='Longitude',
    size='Total_EVs',
    color='EV_to_Port_Ratio',
    color_continuous_scale='RdYlGn_r',
    size_max=50,
    opacity=0.7,
    mapbox_style='carto-positron',
    center={'lat': 47.5, 'lon': -120.5},
    zoom=6,
    title='Washington State: EV Charging Desert Analysis (Red = High Opportunity)',
    hover_data={
        'Postal Code': True,
        'County': True,
        'Total_EVs': True,
        'Total_Ports': True,
        'EV_to_Port_Ratio': ':.1f'
    }
)

fig.update_layout(
    coloraxis_colorbar=dict(title="EV/Port Ratio", thickness=20),
    height=700
)

fig.show()

# %% [markdown]
# ## 12. Export Results

# %%
# Save map
fig.write_html('output/charging_desert_map.html')
print("Map saved to: output/charging_desert_map.html")

# Export Top 50 targets
top_targets = df[df['Total_EVs'] > 20].sort_values('EV_to_Port_Ratio', ascending=False).head(50)
top_targets[['Postal Code', 'County', 'City', 'Total_EVs', 'Total_Ports', 'EV_to_Port_Ratio', 'Priority_Level']].to_csv(
    'output/top_50_investment_zones.csv', index=False
)
print("Top 50 targets exported to: output/top_50_investment_zones.csv")

# %% [markdown]
# ## 13. Business Recommendations

# %%
print("""
╔════════════════════════════════════════════════════════════════╗
║              BUSINESS RECOMMENDATIONS - 2026 ROLLOUT           ║
╚════════════════════════════════════════════════════════════════╝

IMMEDIATE ACTION ITEMS:
────────────────────────────────────────────────────────────────

PRIORITY 1 - Install DC Fast Chargers in Top 10 Target ZIPs
   • These ZIPs have >50 EVs each and <2 public ports
   • Quick win: High demand, low competition

PRIORITY 2 - Deploy Level 2 Networks in Critical Desert ZIPs
   • Focus on ZIPs with >100 EVs first
   • Partner with retailers for site placement

PRIORITY 3 - Urban Corridor Strategy
   • Focus on counties with highest EV density
   • Consider workplace charging programs

╚════════════════════════════════════════════════════════════════╝
""")
