import requests
import os


def url_download(download_url, filename=None):
    """
    下载文件到指定目录
    :param download_url: 文件下载的url
    :param filename: 要存放的目录及文件名，例如：./test.grib2
    :return:
    """
    down_res = requests.get(download_url)
    with open(filename, 'wb') as file:
        file.write(down_res.content)


def retrieve(base_url, params):
    """
    获取下载url
    :param base_url: 接口url
    :param params: 数据参数
    :return:
    """
    base_url = base_url + '?' + '&'.join([f"{key}={value}" for key, value in params.items()])

    ds = requests.get(base_url)

    ds_json = ds.json()

    if ds_json['code'] == '200':
        for da in ds_json['data']:
            file_name = os.path.join(params['outputPath'], da['V_FILE_NAME'])
            url_download(da['D_STORAGE_SITE'], filename=file_name)
            print('已下载：', file_name)
    else:
        print(ds_json)
