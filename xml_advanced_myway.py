import xml.dom.minidom


def get_xml_data(file_name, tag_name, attribute_for_filtering, arribute_to_read):
    xml_doc = xml.dom.minidom.parse(file_name)
    countries = xml_doc.getElementsByTagName(tag_name)
    governments = [country.getAttribute(arribute_to_read).strip().lower() for country in countries if len(country.getAttribute(attribute_for_filtering).split()) > 1]
    governments = sorted(set(governments))
    print(', '.join(governments))
	

get_xml_data('mondial-3.0.xml', 'country', 'name', 'government')
