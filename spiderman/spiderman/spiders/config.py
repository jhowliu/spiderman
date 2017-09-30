# -*- coding=utf-8 -*-

S_TAIWAN_API='http://www.twhg.com.tw/api/SearchList.php?io5='
S_TAIWAN_HOST='http://www.twhg.com.tw'
R_TAIWAN_API='http://rent.twhg.com.tw/searchList.php'
R_TAIWAN_HOST='http://rent.twhg.com.tw'

R_591_HOST='https://rent.591.com.tw'
S_591_HOST='https://sale.591.com.tw'

# use for post
TAIWAN_FORMDATA= {
    'S_Taiwan': {
        'city': u'台北市',
        'usIde': '9',
        'nowpag': '2',
        'paydumeyes': '1',
        'obj' : 'Preset',
    },
    'R_Taiwan': {
        'rCountyCity': u'台北市'
    }
}

TAIWAN_HOUSE_HEADERS = {
    'Referer': 'http://www.twhg.com.tw/object_list-A.php',
    'Origin' : 'http://www.twhg.com.tw'
}

CITIES = [
    (0,  '台北市'),
    (1,  '基隆市'),
    (2,  '新北市'),
    (3,  '宜蘭縣'),
    (4,  '新竹市'),
    (5,  '新竹縣'),
    (6,  '桃園市'),
    (7,  '苗栗縣'),
    (8,  '台中市'),
    (9,  '彰化縣'),
    (10, '南投縣'),
    (11, '嘉義市'),
    (12, '嘉義縣'),
    (13, '雲林縣'),
    (14, '台南市'),
    (15, '高雄市'),
    (16, '澎湖縣'),
    (17, '金門縣'),
    (18, '屏東縣'),
    (19, '台東縣'),
    (20, '花蓮縣')
]

