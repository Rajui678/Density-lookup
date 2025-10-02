import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Density Lookup",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    .result-box {
        background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%);
        padding: 2rem;
        border-radius: 0.75rem;
        border: 2px solid #3b82f6;
        margin: 1rem 0;
    }
    .result-value {
        font-size: 3rem;
        font-weight: bold;
        color: #2563eb;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #f9fafb;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    # Try multiple possible locations
    possible_paths = [
        'Transformed_Density.csv',
        '../Transformed_Density.csv',
        'c:/Users/Ankit Raj/Documents/Project/Transformed_Density.csv'
    ]
    
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            # Clean column names
            df.columns = df.columns.str.strip()
            return df
        except FileNotFoundError:
            continue
    
    raise FileNotFoundError("Could not find Transformed_Density.csv in any expected location")

try:
    df = load_data()
    
    # Title
    st.title("🔬 Density Lookup")
    st.markdown("Find Corresponding Density from Measured Density and Observed Temperature")
    st.markdown("---")
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Parameters")
        
        # Get data ranges
        md_min = df['Measured Density'].min()
        md_max = df['Measured Density'].max()
        temp_min = df['Observed Temperature'].min()
        temp_max = df['Observed Temperature'].max()
        
        # Input fields
        measured_density = st.number_input(
            "Measured Density",
            min_value=float(md_min),
            max_value=float(md_max),
            value=float(md_min),
            step=0.0001,
            format="%.4f",
            help=f"Range: {md_min:.4f} - {md_max:.4f}"
        )
        
        observed_temp = st.number_input(
            "Observed Temperature",
            min_value=float(temp_min),
            max_value=float(temp_max),
            value=float(temp_min),
            step=0.01,
            format="%.2f",
            help=f"Range: {temp_min:.2f} - {temp_max:.2f}"
        )
        
        # Find button
        find_button = st.button("🔍 Find Density", use_container_width=True)
    
    with col2:
        st.subheader("Results")
        
        if find_button:
            # Search for matching rows
            tolerance_density = 0.001
            tolerance_temp = 0.01
            
            matches = df[
                (abs(df['Measured Density'] - measured_density) < tolerance_density) &
                (abs(df['Observed Temperature'] - observed_temp) < tolerance_temp)
            ]
            
            if len(matches) > 0:
                result = matches.iloc[0]
                corresponding_density = result['Corresponding Density']
                
                # Display result in a styled box
                st.markdown(f"""
                    <div class="result-box">
                        <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">Corresponding Density</p>
                        <div class="result-value">{corresponding_density}</div>
                        <p style="color: #10b981; font-size: 0.875rem; margin-top: 0.5rem;">✓ Found in dataset</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Show input values
                st.markdown("""
                    <div class="info-box">
                        <p style="font-weight: 600; color: #374151; margin-bottom: 0.5rem;">Input Values:</p>
                    </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Measured Density", f"{result['Measured Density']:.4f}")
                with col_b:
                    st.metric("Observed Temperature", f"{result['Observed Temperature']:.2f}")
                
                st.metric("Corresponding Density", f"{corresponding_density:.4f}", 
                         delta=None, delta_color="off")
                
            else:
                st.error("❌ No matching values found in the dataset. Please check your inputs.")
        else:
            st.info("Enter values and click 'Find Density' to see results")
    
    # Dataset information
    st.markdown("---")
    st.subheader("📊 Dataset Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Data Points", f"{len(df):,}")
    
    with col2:
        st.metric("Measured Density Range", 
                 f"{df['Measured Density'].min():.2f} - {df['Measured Density'].max():.2f}")
    
    with col3:
        st.metric("Temperature Range", 
                 f"{df['Observed Temperature'].min():.2f} - {df['Observed Temperature'].max():.2f}")
    
    # Show sample data
    with st.expander("View Sample Data"):
        st.dataframe(df.head(10), use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ Error: 'Transformed_Density.csv' file not found. Please ensure the file is in the same directory as this script.")
except Exception as e:
    st.error(f"⚠️ Error loading data: {str(e)}")
