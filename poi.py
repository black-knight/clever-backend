import threading
import urllib.request
from xml.dom import minidom

webservice_url = 'http://services.clever.dk/poi.1.5.xml'

cached_poi_dict = {}

def nodeValue(item, key):
    children = item.getElementsByTagName(key)
    if children is not None and len(children) > 0 and children[0].childNodes is not None and len(children[0].childNodes) > 0:
        return children[0].childNodes[0].nodeValue
    else:
        return ''

def fetch_poi():
    try:
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
            name = nodeValue(cacheable_item, 'itemName')
            url = nodeValue(cacheable_item, 'url')
            cacheable_item_dict[name] = url

        # ConnctorVariants
        connector_variants = poi.getElementsByTagName('ConnctorVariants')[0]
        for connector_item in connector_variants.getElementsByTagName('Con'):
            variant = nodeValue(connector_item, 'Variant')
            icon = nodeValue(connector_item, 'icon')
            name = nodeValue(connector_item, 'name')
            capacity = nodeValue(connector_item, 'capacity')
            filter_type = nodeValue(connector_item, 'Filter')
            connector_variants_dict[variant] = {'icon': icon,
                                                'name': name,
                                                'capacity': capacity,
                                                'filter': filter_type}

        # Locations
        location_items = poi.getElementsByTagName('locations')[0]
        for location_item in location_items.getElementsByTagName('location'):
            location_id = nodeValue(location_item, 'id')
            latitude = nodeValue(location_item, 'latitude')
            longitude = nodeValue(location_item, 'longitude')
            name = nodeValue(location_item, 'poiName')
            street_name = nodeValue(location_item, 'stretName')
            house_number = nodeValue(location_item, 'houseNumber')
            city = nodeValue(location_item, 'city')
            postal_code = nodeValue(location_item, 'postalCode')
            phone = nodeValue(location_item, 'phoneName')
            icon = nodeValue(location_item, 'icon')
            picture_url = nodeValue(location_item, 'picture')
            minimap_url = nodeValue(location_item, 'minimap')
            description = nodeValue(location_item, 'description')
            access_info = nodeValue(location_item, 'accessInfo')
            payment = nodeValue(location_item, 'payment')
            pay_button_text = nodeValue(location_item, 'payButton')
            pay_link = nodeValue(location_item, 'payLink')
            connector_list = []
            for connector in location_item.getElementsByTagName('connectors'):
                variant = nodeValue(connector, 'variant')
                connector_count = nodeValue(connector, 'connectorCount')
                available = nodeValue(connector, 'available')
                occupied = nodeValue(connector, 'occupied')
                error = nodeValue(connector, 'error')
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

    finally:
        threading.Timer(30, fetch_poi).start()

def start_poi_fetching_thread():
    fetch_poi()

def get_cached_poi():
    global cached_poi_dict
    return cached_poi_dict
