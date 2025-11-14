import streamlit as st
import pandas as pd

# -----------------------------------
# PAGE SETTINGS
# -----------------------------------
st.set_page_config(
    page_title="123 Pollachi AC - SIR 2002 Search",
    layout="wide"
)

# Mobile-friendly padding + FIX FOR LAST COLUMN VISIBILITY
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; padding-left: 0.5rem; padding-right: 0.5rem; }
        input[type="text"] { font-size: 1.1rem; }
        button[kind="secondary"] { width: 100%; }

        /* FIX: Make DataFrame scrollable */
        .stDataFrame {
            overflow-x: auto !important;
        }

        /* FIX: Ensure long Tamil text (LAST COLUMN) wraps instead of cutting */
        .dataframe td, .dataframe th {
            white-space: normal !important;
            word-break: break-word !important;
            max-width: 300px !important;
            line-height: 1.3rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------
# PAGE TITLES
# -----------------------------------
st.title("🗳️ 123 பொள்ளாச்சி சட்டமன்ற தொகுதி (Pollachi Assembly Constituency)")
st.subheader("🔍 வாக்காளர் விவரம் - 2002 (Voter Details - 2002)")

# -----------------------------------
# LOAD DATA
# -----------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("old_data.xlsx")

    # Convert to uppercase for consistent exact-match search
    df["FM_NAME_V2"] = df["FM_NAME_V2"].astype(str).upper().str.strip()
    df["RLN_FM_NM_V2"] = df["RLN_FM_NM_V2"].astype(str).upper().str.strip()

    return df

df = load_data()
if df.empty:
    st.stop()

# -----------------------------------
# INPUT SECTION
# -----------------------------------
st.markdown("### 📝 விவரங்களை உள்ளிடவும் (Enter Details)")

voter_name = st.text_input(
    "வாக்காளர் பெயர் (Voter's Name) – தமிழ் மட்டும் (Tamil Only)",
    placeholder="உதா: ராமு (Example: Ramu)"
)

relation_name = st.text_input(
    "தந்தை / கணவர் பெயர் (Father's / Husband's Name) – தமிழ் மட்டும் (Tamil Only)",
    placeholder="உதா: முருகேசன் (Example: Murugesan)"
)

# -----------------------------------
# SEARCH OPERATION (Exact Match)
# -----------------------------------
if st.button("🔍 தேடு (Search)"):

    if not voter_name or not relation_name:
        st.warning("⚠️ வாக்காளர் பெயர் மற்றும் தந்தை/கணவர் பெயரை இரண்டையும் உள்ளிடவும்.")
        st.stop()

    name = voter_name.upper().strip()
    rname = relation_name.upper().strip()

    # Exact match search (This version displays last column properly)
    result = df[
        (df["FM_NAME_V2"] == name) &
        (df["RLN_FM_NM_V2"] == rname)
    ]

    # -----------------------------------
    # RESULTS
    # -----------------------------------
    if not result.empty:
        st.success(f"✔ {len(result)} பதிவுகள் கிடைத்தன (record(s) found).")
        st.dataframe(result, use_container_width=True)
    else:
        st.error("❌ பொருந்தும் பதிவுகள் இல்லை (No matching records found).")
