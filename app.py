import streamlit as st
import pandas as pd
import requests
import json
import xml.etree.ElementTree as ET
from io import StringIO
import base64

# Page configuration
st.set_page_config(
    page_title="Koch LV Verarbeitung",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: rgba(59,130,246,0.5);
        color: white;
    }
    .stTextInput>div>div>input {
        border-color: rgba(59,130,246,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'original_data' not in st.session_state:
    st.session_state.original_data = None
if 'customer_id' not in st.session_state:
    st.session_state.customer_id = ""

# Header
st.title("Koch LV Verarbeitung")
st.markdown("---")

# Customer ID input
customer_id = st.text_input("Kunden-ID", value=st.session_state.customer_id)
st.session_state.customer_id = customer_id

# File upload
uploaded_file = st.file_uploader("PDF-Datei hochladen", type=['pdf'])

def process_pdf(file):
    # Simulate API call - replace with actual API endpoint
    # response = requests.post('http://your-api/upload', files={'file': file})
    # return response.json()
    
    # Example data for demonstration
    return [
        {
            "sku": "620001",
            "name": "Bürotür mit Stahl-U-Zarge (0,76 x 2,135 m)",
            "text": "Stahlzarge, verzinkt, Hörmann BaseLine...",
            "quantity": 1,
            "quantityUnit": "Stk",
            "price": 695.00,
            "priceUnit": "€",
            "commission": "LV-POS. 1.1.10"
        },
        {
            "sku": "620002",
            "name": "Bürotür mit Holz-U-Zarge (0,86 x 2,135 m)",
            "text": "Holzzarge, lackiert, Hörmann BaseLine...",
            "quantity": 2,
            "quantityUnit": "Stk",
            "price": 795.00,
            "priceUnit": "€",
            "commission": "LV-POS. 1.1.11"
        }
    ]

def generate_xml(data, customer_id):
    # Create XML structure
    root = ET.Element("offer")
    customer = ET.SubElement(root, "customer")
    customer.text = customer_id
    
    positions = ET.SubElement(root, "positions")
    
    for item in data:
        position = ET.SubElement(positions, "position")
        for key, value in item.items():
            if key != "commission":  # Skip commission in XML
                element = ET.SubElement(position, key)
                element.text = str(value)
    
    # Convert to string
    tree = ET.ElementTree(root)
    xml_str = StringIO()
    tree.write(xml_str, encoding='unicode', xml_declaration=True)
    return xml_str.getvalue()

def get_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/xml;base64,{b64}" download="{filename}">XML herunterladen</a>'

# Process uploaded file
if uploaded_file is not None:
    if st.session_state.data is None:
        st.session_state.data = process_pdf(uploaded_file)
        st.session_state.original_data = st.session_state.data.copy()

# Display and edit data
if st.session_state.data is not None:
    # Convert data to DataFrame
    df = pd.DataFrame(st.session_state.data)
    
    # Create editable dataframe
    edited_df = st.data_editor(
        df,
        column_config={
            "sku": st.column_config.TextColumn("SKU", width="medium"),
            "name": st.column_config.TextColumn("Name", width="large"),
            "text": st.column_config.TextColumn("Beschreibung", width="large", max_chars=500),
            "quantity": st.column_config.NumberColumn("Menge", width="small"),
            "quantityUnit": st.column_config.TextColumn("Einheit", width="small"),
            "price": st.column_config.NumberColumn("Preis", width="medium", format="%.2f"),
            "priceUnit": st.column_config.TextColumn("Preis-Einheit", width="small"),
            "commission": st.column_config.TextColumn("Kommission", width="medium")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Update session state with edited data
    st.session_state.data = edited_df.to_dict('records')
    
    # Buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("PDF hochladen"):
            st.session_state.data = None
            st.session_state.original_data = None
            st.experimental_rerun()
    
    with col2:
        if st.button("Zurücksetzen"):
            st.session_state.data = st.session_state.original_data.copy()
            st.experimental_rerun()
    
    with col3:
        if st.button("XML generieren"):
            if not customer_id:
                st.error("Bitte geben Sie eine Kunden-ID ein.")
            else:
                xml_content = generate_xml(st.session_state.data, customer_id)
                st.session_state.xml_content = xml_content
                st.success("XML wurde generiert!")
    
    with col4:
        if 'xml_content' in st.session_state:
            st.markdown(get_download_link(st.session_state.xml_content, "angebot.xml"), unsafe_allow_html=True)
    
    # Preview section
    with st.expander("Vorschau"):
        tab1, tab2 = st.tabs(["JSON", "XML"])
        
        with tab1:
            st.json(st.session_state.data)
        
        with tab2:
            if 'xml_content' in st.session_state:
                st.code(st.session_state.xml_content, language="xml")
            else:
                st.info("Generieren Sie zuerst das XML.") 