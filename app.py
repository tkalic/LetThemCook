from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
import xml.etree.ElementTree as ET
from io import StringIO, BytesIO
import base64
import re

app = Flask(__name__)

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
            "text": "Hörmann Stahlfutterzarge VarioFix für Mauerwerk oder TRB<br/>- Drückerhöhe 1050 mm<br/>- Meterrissmarkierung<br/>- Maulweitenkante 15 mm<br/>- Stahlblech verzinkt, Materialstärke 1,5 mm<br/>- Hörmann BaseLine HPL Türblatt<br/>- Türgewicht ca. 18,1 kg/m²<br/>- Türstärke ca. 40,7 mm",
            "quantity": 1.00,
            "quantityUnit": "Stk",
            "price": 695.00,
            "priceUnit": "€",
            "purchasePrice": None,
            "commission": "LV-POS. 1.1.10"
        },
        {
            "type": "P",
            "sku": "620001",
            "name": "Tür wie Pos.10, Breite 0,885 m",
            "text": "Wie Pos. 10 jedoch b=0,885 m. Einbauort: WC Herren.",
            "quantity": 1.00,
            "quantityUnit": "Stk",
            "price": 705.00,
            "priceUnit": "€",
            "purchasePrice": None,
            "commission": "LV-POS. 1.1.20"
        }
    ]

def generate_xml(data, customer_id, shipping_condition_id, order_commission, order_type):
    # Create XML structure
    root = ET.Element("order")
    
    # Add order-level elements
    customer = ET.SubElement(root, "customerId")
    customer.text = customer_id
    
    commission = ET.SubElement(root, "commission")
    commission.text = order_commission
    
    type_elem = ET.SubElement(root, "type")
    type_elem.text = order_type
    
    shipping = ET.SubElement(root, "shippingConditionId")
    shipping.text = shipping_condition_id
    
    # Add items
    items = ET.SubElement(root, "items")
    
    for item in data:
        item_element = ET.SubElement(items, "item")
        for key, value in item.items():
            element = ET.SubElement(item_element, key)
            if value is None:
                element.text = ""
            else:
                element.text = str(value)
    
    # Convert to string with proper formatting
    tree = ET.ElementTree(root)
    xml_str = StringIO()
    tree.write(xml_str, encoding='unicode', xml_declaration=True)
    
    # Format the XML string with proper indentation
    xml_content = xml_str.getvalue()
    xml_content = xml_content.replace('><', '>\n<')
    xml_content = xml_content.replace('</item><item>', '</item>\n      <item>')
    xml_content = xml_content.replace('</items>', '\n   </items>')
    xml_content = xml_content.replace('</order>', '\n</order>')
    
    return xml_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        data = process_pdf(file)
        return jsonify(data)
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/generate-xml', methods=['POST'])
def generate_xml_endpoint():
    data = request.json
    customer_id = data.get('customerId')
    shipping_condition_id = data.get('shippingConditionId')
    order_commission = data.get('commission')
    order_type = data.get('type', 'A')
    items = data.get('items', [])
    
    if not customer_id or not shipping_condition_id:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not validate_customer_id(customer_id):
        return jsonify({'error': 'Invalid customer ID'}), 400
    
    if not validate_shipping_condition_id(shipping_condition_id):
        return jsonify({'error': 'Invalid shipping condition ID'}), 400
    
    xml_content = generate_xml(items, customer_id, shipping_condition_id, order_commission, order_type)
    
    # Create a BytesIO object to store the XML
    xml_file = BytesIO(xml_content.encode('utf-8'))
    xml_file.seek(0)
    
    return send_file(
        xml_file,
        mimetype='application/xml',
        as_attachment=True,
        download_name='angebot.xml'
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)