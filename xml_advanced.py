import xml.etree.ElementTree as ET


def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = ET.iterparse(filename, ('start', 'end'))
    next(doc)
    tag_stack = []
    elem_stack = []

    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass


def get_xml_data(filename, path, condition_attribute, searched_attribute):
    countries = parse_and_remove(filename, path)
    governmental_systems = [country.attrib[searched_attribute].strip().lower() for country in countries if len(country.attrib[condition_attribute].split()) > 1] # make a list of governments for countries, where 'length'(number of words) > 1
    governmental_systems = sorted(set(governmental_systems)) # sort and exclude duplicates from the list of governments
    print(', '.join(governmental_systems)) # display the list in 1 line, comma separated


get_xml_data ('mondial-3.0.xml', 'country', 'name', 'government')

