def taiwan_sale(infos):

    price = infos['pay']
    case_no = infos['no']
    case_name = infos['tit']
    road = infos['add']
    city = infos['city']
    district = infos['area']
    addr = city+district+road

    building_pings = infos['pin']
    landing_pings = infos['landpin']

    num_of_living = infos['liv']
    num_of_bed = infos['bed']
    num_of_bath = infos['bat']

    layout = u'%s房%s廳%s衛' % (num_of_bed, num_of_living, num_of_bath)

    lat = infos['x']
    lng = infos['y']

    url = infos['CaseURL']

    items = {
        'CaseNo': case_no,
        'CaseURL': url,
        'CaseName': case_name,
        'Address': addr,
        'City': city,
        'Zip': district,
        'Road': road,
        'Living': num_of_living,
        'Bed': num_of_bed,
        'Bath': num_of_bath,
        'Layout': layout,
        'BuildingPing': building_pings,
        'Latitude': lat,
        'Longtitude': lng,
        'Price': price
        'RorS': u'出售'
    }

    return items

def taiwan_rent(infos):
    pass
