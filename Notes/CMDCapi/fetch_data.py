import CMDCapi

url = 'https://ai.data.cma.cn/aiApi/searchGlobalGround/fileDownloadList'

params = {
    'elementLayer': 'hour:tem',
    'statName': '亚洲',
    'year': None,
    'userId': 'FlxX%2FRFQabYjmQ40GyiLa9DC3AyZJL4gTX00yqWI7FP%2Bhbk4rbfeFA%3D%3D',
    'productId': '5',
    'outputPath': './',
    'moid': '1.2.156.416.CMA.D3-S.202504.GT30I'
}

for i in range (2000, 2024):
    params['year'] = i
    print(f'Downloading data of year {i}')
    CMDCapi.retrieve(base_url=url, params=params)
