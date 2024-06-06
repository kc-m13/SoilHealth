import requests
from bs4 import BeautifulSoup
import json

# Define the URL
url = 'https://www.soilhealth.dac.gov.in/piechart'

# Fetch the webpage
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Parse the webpage content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the script tag containing the data (assuming the data is in a <script> tag)
script_tags = soup.find_all('script')

# We need to identify the correct script tag that contains the data
# Inspecting manually, we find the right tag (this may change, so always check the latest HTML structure)
data_script = None
for script in script_tags:
    if 'var stateWiseMacronutrientData' in script.text:
        data_script = script
        break

# Extract the JavaScript object
if data_script:
    # Locate the starting position of the data object
    data_start = data_script.text.find('var stateWiseMacronutrientData = ') + len('var stateWiseMacronutrientData = ')
    data_end = data_script.text.find(';', data_start)
    
    # Extract the JSON-like data
    json_data = data_script.text[data_start:data_end].strip()
    
    # Parse the JSON data
    macronutrient_data = json.loads(json_data)

    # Output the data
    print(json.dumps(macronutrient_data, indent=4))

else:
    print("Data script not found.")
