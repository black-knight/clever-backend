import urllib.request
import MySQLdb
from xml.dom import minidom

webservice_url = 'http://services.clever.dk/poi.1.5.xml'

cached_poi_dict = {}

def initialize():
    setup_database()
    update_poi()



def setup_database():
    global db
    global db_cursor
    db = MySQLdb.connect(host="mysql.server",
                         user="trollsahead",
                         passwd="Test1234",
                         db="trollsahead$clever")
    db_cursor = db.cursor()



def fetch_poi():
    cacheable_item_dict = {}
    connector_variants_dict = {}
    locations_dict = {}

    print('Fetching poi from %s...' % webservice_url)
    with urllib.request.urlopen(webservice_url) as url:
        dom = minidom.parseString(url.read().decode("utf-8"))
    print('Poi''s fetched!')

    # poi
    poi = dom.childNodes[0]

    # CacheableItems
    cacheable_items = poi.getElementsByTagName('CacheableItems')[0]
    for cacheable_item in cacheable_items.getElementsByTagName('item'):
        name = node_value(cacheable_item, 'itemName')
        url = node_value(cacheable_item, 'url')
        cacheable_item_dict[name] = url

    # ConnctorVariants
    connector_variants = poi.getElementsByTagName('ConnctorVariants')[0]
    for connector_item in connector_variants.getElementsByTagName('Con'):
        variant = node_value(connector_item, 'Variant')
        icon = node_value(connector_item, 'icon')
        name = node_value(connector_item, 'name')
        capacity = node_value(connector_item, 'capacity')
        filter_type = node_value(connector_item, 'Filter')
        connector_variants_dict[variant] = {'icon': icon,
                                            'name': name,
                                            'capacity': capacity,
                                            'filter': filter_type}

    # Locations
    location_items = poi.getElementsByTagName('locations')[0]
    for location_item in location_items.getElementsByTagName('location'):
        location_id = node_value(location_item, 'id')
        latitude = node_value(location_item, 'latitude')
        longitude = node_value(location_item, 'longitude')
        name = node_value(location_item, 'poiName')
        street_name = node_value(location_item, 'stretName')
        house_number = node_value(location_item, 'houseNumber')
        city = node_value(location_item, 'city')
        postal_code = node_value(location_item, 'postalCode')
        phone = node_value(location_item, 'phoneName')
        icon = node_value(location_item, 'icon')
        picture_url = node_value(location_item, 'picture')
        minimap_url = node_value(location_item, 'minimap')
        description = node_value(location_item, 'description')
        access_info = node_value(location_item, 'accessInfo')
        payment = node_value(location_item, 'payment')
        pay_button_text = node_value(location_item, 'payButton')
        pay_link = node_value(location_item, 'payLink')
        connector_list = []
        for connector in location_item.getElementsByTagName('connectors'):
            variant = node_value(connector, 'variant')
            connector_count = node_value(connector, 'connectorCount')
            available = node_value(connector, 'available')
            occupied = node_value(connector, 'occupied')
            error = node_value(connector, 'error')
            connector_list.append({'variant': variant,
                                   'connectorCount': connector_count,
                                   'available': available,
                                   'occupied': occupied,
                                   'error': error})
        locations_dict[location_id] = {'latitude': latitude,
                                       'longitude': longitude,
                                       'name': name,
                                       'streetName': street_name,
                                       'houseNumber': house_number,
                                       'city': city,
                                       'postalCode': postal_code,
                                       'phone': phone,
                                       'icon': icon,
                                       'pictureUrl': picture_url,
                                       'minimapUrl': minimap_url,
                                       'description': description,
                                       'accessInfo': access_info,
                                       'payment': payment,
                                       'payButtonText': pay_button_text,
                                       'payLink': pay_link,
                                       'connectors': connector_list}


    global cached_poi_dict
    cached_poi_dict = {'cacheableItems': cacheable_item_dict,
                       'connectorVariants': connector_variants_dict,
                       'locations': locations_dict}

def update_poi():
    fetch_poi()
    return get_cached_poi()

def get_cached_poi():
    global cached_poi_dict
    return cached_poi_dict



def node_value(item, key):
    children = item.getElementsByTagName(key)
    if children is not None and len(children) > 0 and children[0].childNodes is not None and len(children[0].childNodes) > 0:
        return children[0].childNodes[0].nodeValue
    else:
        return ''
