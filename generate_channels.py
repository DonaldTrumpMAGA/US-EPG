import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom

m3u_url = 'https://iptv-org.github.io/iptv/index.m3u'

def fetch_m3u_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_tvg_ids(m3u_data):
    tvg_ids = []
    lines = m3u_data.splitlines()
    for line in lines:
        if line.startswith('#EXTINF'):
            parts = line.split(',')
            if len(parts) > 1:
                attrs = parts[0].split()
                for attr in attrs:
                    if attr.startswith('tvg-id='):
                        tvg_id = attr.split('=')[1].strip('"')
                        if tvg_id:
                            if tvg_id.endswith('.us'):
                                tvg_ids.append(tvg_id)
    return tvg_ids

def create_xml(tvg_ids, xml_file_path):
    root = ET.Element('channels')
    for tvg_id in tvg_ids:
        channel = ET.SubElement(root, 'channel')
        channel.set('site', 'tvpassport.com')
        channel.set('lang', 'en')
        channel.set('xmltv_id', tvg_id)
        channel.set('site_id', 'CH_K')
        channel.text = tvg_id

    tree = ET.ElementTree(root)
    with open(xml_file_path, 'wb') as file:
        tree.write(file, encoding='utf-8', xml_declaration=True)

    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_str = file.read()
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent='  ')
    with open(xml_file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml_str)

def main():
    m3u_data = fetch_m3u_data(m3u_url)
    tvg_ids = extract_tvg_ids(m3u_data)
    create_xml(tvg_ids, 'updated_channels.xml')

if __name__ == '__main__':
    main()
