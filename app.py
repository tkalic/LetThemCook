import streamlit as st
import pandas as pd
import requests
import json
import xml.etree.ElementTree as ET
from io import StringIO
import base64
import re

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
if 'shipping_condition_id' not in st.session_state:
    st.session_state.shipping_condition_id = ""
if 'order_commission' not in st.session_state:
    st.session_state.order_commission = ""

def validate_customer_id(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def validate_shipping_condition_id(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def validate_type(value):
    return value in ['P', 'Z', 'D']  # P=Produkt, Z=Zubehör, D=Dienstleistung

def validate_sku(value):
    return len(value) <= 50

def validate_name(value):
    return len(value) <= 255

def validate_quantity_unit(value):
    return len(value) <= 50

def validate_price_unit(value):
    return len(value) <= 10

def validate_commission(value):
    return len(value) <= 255

# Header
st.title("Koch LV Verarbeitung")
st.markdown("---")

# Customer ID, Shipping Condition ID, and Order Commission input
col1, col2, col3 = st.columns(3)
with col1:
    customer_id = st.text_input("Kunden-ID", value=st.session_state.customer_id)
    if customer_id and not validate_customer_id(customer_id):
        st.error("Kunden-ID muss eine ganze Zahl sein")
    st.session_state.customer_id = customer_id

with col2:
    shipping_condition_id = st.text_input("Versandbedingung-ID", value=st.session_state.shipping_condition_id)
    if shipping_condition_id and not validate_shipping_condition_id(shipping_condition_id):
        st.error("Versandbedingung-ID muss eine ganze Zahl sein")
    st.session_state.shipping_condition_id = shipping_condition_id

with col3:
    order_commission = st.text_input("Auftrags-Kommission", value=st.session_state.order_commission)
    if order_commission and not validate_commission(order_commission):
        st.error("Kommission darf maximal 255 Zeichen lang sein")
    st.session_state.order_commission = order_commission

# File upload
uploaded_file = st.file_uploader("PDF-Datei hochladen", type=['pdf'])

def process_pdf(file):
    # Simulate API call - replace with actual API endpoint
    # response = requests.post('http://your-api/upload', files={'file': file})
    # return response.json()
    
    # Example data for demonstration
    return [
        {
            "type": "P",
            "sku": "620001",
            "name": "Bürotür mit Stahl-U-Zarge (0,76 x 2,135 m)",
            "text": "Stahlzarge, verzinkt, Hörmann BaseLine...",
            "quantity": 1.00,
            "quantityUnit": "Stk",
            "price": 695.00,
            "priceUnit": "€",
            "purchasePrice": 595.00,
            "commission": "LV-POS. 1.1.10"
        },
        {
            "type": "P",
            "sku": "620002",
            "name": "Bürotür mit Holz-U-Zarge (0,86 x 2,135 m)",
            "text": "Holzzarge, lackiert, Hörmann BaseLine...",
            "quantity": 2.00,
            "quantityUnit": "Stk",
            "price": 795.00,
            "priceUnit": "€",
            "purchasePrice": 695.00,
            "commission": "LV-POS. 1.1.11"
        }
    ]

def generate_xml(data, customer_id, shipping_condition_id, order_commission):
    # Create XML structure
    root = ET.Element("offer")
    
    # Add customer, shipping condition, and order commission
    customer = ET.SubElement(root, "customerId")
    customer.text = customer_id
    
    shipping = ET.SubElement(root, "shippingConditionId")
    shipping.text = shipping_condition_id
    
    commission = ET.SubElement(root, "commission")
    commission.text = order_commission
    
    # Add items
    items = ET.SubElement(root, "items")
    
    for item in data:
        item_element = ET.SubElement(items, "item")
        for key, value in item.items():
            element = ET.SubElement(item_element, key)
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
            "type": st.column_config.SelectboxColumn(
                "Typ",
                width="small",
                options=["P", "Z", "D"],
                help="P=Produkt, Z=Zubehör, D=Dienstleistung"
            ),
            "sku": st.column_config.TextColumn(
                "SKU",
                width="medium",
                max_chars=50
            ),
            "name": st.column_config.TextColumn(
                "Name",
                width="large",
                max_chars=255
            ),
            "text": st.column_config.TextColumn(
                "Beschreibung",
                width="large",
                max_chars=1000
            ),
            "quantity": st.column_config.NumberColumn(
                "Menge",
                width="small",
                format="%.2f",
                step=0.01
            ),
            "quantityUnit": st.column_config.TextColumn(
                "Einheit",
                width="small",
                max_chars=50
            ),
            "price": st.column_config.NumberColumn(
                "Preis",
                width="medium",
                format="%.2f",
                step=0.01
            ),
            "priceUnit": st.column_config.TextColumn(
                "Preis-Einheit",
                width="small",
                max_chars=10
            ),
            "purchasePrice": st.column_config.NumberColumn(
                "Einkaufspreis",
                width="medium",
                format="%.2f",
                step=0.01
            ),
            "commission": st.column_config.TextColumn(
                "Kommission",
                width="medium",
                max_chars=255
            )
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
            if not customer_id or not shipping_condition_id:
                st.error("Bitte geben Sie eine Kunden-ID und Versandbedingung-ID ein.")
            elif not validate_customer_id(customer_id):
                st.error("Kunden-ID muss eine ganze Zahl sein")
            elif not validate_shipping_condition_id(shipping_condition_id):
                st.error("Versandbedingung-ID muss eine ganze Zahl sein")
            else:
                xml_content = generate_xml(
                    st.session_state.data,
                    customer_id,
                    shipping_condition_id,
                    order_commission
                )
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