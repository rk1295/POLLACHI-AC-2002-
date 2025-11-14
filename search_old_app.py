import streamlit as st
import pandas as pd

st.set_page_config(page_title="Old Data Search", layout="wide")
st.title("🔍 Old Voter Data Search (By Name & Relation Name)")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("old_data.xlsx")

    # Convert to uppercase for consistent search
    df["FM_NAME_V2"] = df["FM_NAME_V2"].astype(str).str.upper().str.strip()
    df["RLN_FM_NM_V2"] = df["RLN_FM_NM_V2"].astype(str).str.upper().str.strip()

    return df

df = load_data()

# ---------------------------
# SEARCH FIELDS
# ---------------------------
name_input = st.text_input("Enter NAME (FM_NAME_V2)")
rname_input = st.text_input("Enter RELATION NAME (RLN_FM_NM_V2)")

if st.button("Search"):

    if not name_input or not rname_input:
        st.warning("⚠️ Please enter BOTH Name and Relation Name to search.")
        st.stop()

    name = name_input.upper().strip()
    rname = rname_input.upper().strip()

    # Exact match search
    result = df[
        (df["FM_NAME_V2"] == name) &
        (df["RLN_FM_NM_V2"] == rname)
    ]

    if not result.empty:
        st.success(f"✔ {len(result)} record(s) found.")
        st.dataframe(result, use_container_width=True)
    else:
        st.error("❌ No matching record found.")
