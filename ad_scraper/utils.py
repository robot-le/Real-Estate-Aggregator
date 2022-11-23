import requests
import xml.etree.ElementTree as ET


def get_usd_rate():
    response = requests.get('https://www.nbkr.kg/XML/daily.xml')
    tree = ET.fromstring(response.text)
    usd_str = [x[1].text for x in tree if x.attrib.get('ISOCode') == 'USD'][0]
    usd_rate = float(usd_str.replace(',', '.'))
    return usd_rate
