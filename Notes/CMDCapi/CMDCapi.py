import requests
import os
from tqdm import tqdm


def url_download(download_url, filename=None):
    """
    下载文件到指定目录，并带有 tqdm 进度条显示
    :param download_url: 文件下载的url
    :param filename: 要存放的目录及文件名
    :return:
    """
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        with open(filename, 'wb') as f, tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc=os.path.basename(filename)
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))


def retrieve(base_url, params):
    """
    获取下载url并调用下载
    :param base_url: 接口url
    :param params: 数据参数
    :return:
    """
    query_url = base_url + '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
    ds = requests.get(query_url)
    ds_json = ds.json()

    if ds_json['code'] == '200':
        data_list = ds_json['data']
        print(f"共 {len(data_list)} 个文件待下载")
        for idx, da in enumerate(data_list):
            file_name = os.path.join(params['outputPath'], da['V_FILE_NAME'])
            file_url = da['D_STORAGE_SITE']
            print(f"[{idx + 1}/{len(data_list)}] 下载：{file_name}")
            url_download(file_url, filename=file_name)
    else:
        print('请求失败，响应：', ds_json)
