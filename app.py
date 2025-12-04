import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="DA Gap Analysis", layout="wide")

st.title("📊 DA Analysis Dashboard")
st.markdown("Upload your Excel sheet to calculate incomplete DA-sets and analyze gaps.")

# 2. File Uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Load the data
    try:
        df = pd.read_excel(uploaded_file)
        
        # --- DATA CLEANING & LOGIC ---
        # Ensure column names match your Excel sheet exactly. 
        # Based on your image, I am assuming these names:
        # 'Region', 'DA-Pre', 'DA-Post'
        
        # Calculate the Gap manually to be safe
        df['Calculated_Gap'] = df['DA-Pre'] - df['DA-Post']

        # LOGIC: Identify "Incomplete DA-sets"
        # You said: "if DA-pre and DA-post is equal, there is no incomplete DA-set"
        # Therefore, Incomplete means Gap is NOT 0.
        incomplete_da_df = df[df['Calculated_Gap'] != 0].copy()

        # Calculate metrics
        total_regions = len(df)
        incomplete_regions_count = len(incomplete_da_df)
        
        # Average Incomplete Gap (Average of only the ones that have a gap)
        avg_incomplete_gap = incomplete_da_df['Calculated_Gap'].mean()

        # --- DASHBOARD LAYOUT ---
        
        # 3. Key Metrics Row
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Total Regions", total_regions)
        col2.metric("Regions with Incomplete DA", incomplete_regions_count)
        col3.metric("Avg Gap (Incomplete Sets Only)", f"{avg_incomplete_gap:.2f}")

        st.divider()

        # 4. Detailed Data View
        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.subheader("Data Preview")
            # Highlight rows where gap is high
            st.dataframe(df.style.highlight_max(axis=0, subset=['Calculated_Gap']))

        with col_right:
            st.subheader("Gap Analysis by Region")
            # Create a Bar Chart
            fig = px.bar(
                df, 
                x='Region', 
                y='Calculated_Gap',
                color='Calculated_Gap',
                title="DA Pre-to-Post Gap per Region",
                labels={'Calculated_Gap': 'Gap Size'},
                color_continuous_scale='Redor' # Red indicates higher gap
            )
            st.plotly_chart(fig, use_container_width=True)

        # 5. Download Report
        st.subheader("Export Analysis")
        
        # Convert filtered data to CSV for download
        csv = incomplete_da_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Incomplete DA Report (CSV)",
            data=csv,
            file_name='incomplete_da_report.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"Error processing file: {e}. Please ensure your Excel headers match: Region, DA-Pre, DA-Post")

else:
    st.info("Awaiting file upload. Please upload the Excel sheet provided.")