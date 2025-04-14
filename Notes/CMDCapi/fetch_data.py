import CMDCapi
import copy
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

url = 'https://ai.data.cma.cn/aiApi/searchGlobalGround/fileDownloadList'

base_params = {
    'elementLayer': 'hour:tem',
    'statName': '亚洲',
    'year': None,
    'userId': 'FlxX%2FRFQabYjmQ40GyiLa9DC3AyZJL4gTX00yqWI7FP%2Bhbk4rbfeFA%3D%3D',
    'productId': '5',
    'outputPath': './',
    'moid': '1.2.156.416.CMA.D3-S.202504.GT30I'
}


def task(year):
    params = copy.deepcopy(base_params)
    params['year'] = str(year)
    try:
        CMDCapi.retrieve(base_url=url, params=params)
        return f"✅ {year} done"
    except Exception as e:
        return f"❌ {year} failed: {e}"


years = list(range(2000, 2024))

with ThreadPoolExecutor(max_workers=6) as executor:
    futures = [executor.submit(task, year) for year in years]
    for f in tqdm(as_completed(futures), total=len(futures), desc="Downloading by year"):
        result = f.result()
        print(result)
