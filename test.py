import requests
import xml.etree.ElementTree as ET

url = 'https://www.nbkr.kg/XML/daily.xml'

response = requests.get(url)

# tree = ET.parse(response.text)
tree = ET.fromstring(response.text)

# print(tree[0].tag)
usd_str = [x[1].text for x in tree if x.attrib.get('ISOCode') == 'USD'][0]
print(float(usd_str.replace(',', '.')))
# for i in tree:
#     print(i[1].text, i.attrib.get('ISOCode'))
