import requests
import json
from headers.UserAgents import get_headers

def get_boundary(uid):
    """获取poi边界geo"""

    url = 'https://map.baidu.com/?reqflag=pcmap&from=webmap&da_par=direct&pcevaname=pc4.1&' \
          'qt=ext&uid={}&' \
          'ext_ver=new&' \
          'tn=B_NORMAL_MAP&nn=0&auth=fw9wVDQUyKS7%3DQ5eWeb5A21KZOG0NadNuxHNBxBBLBHtxjhNwzWWvy1uVt1GgvPUDZYOYIZuEt2gz4yYxGccZcuVtPWv3GuxNt%3DkVJ0IUvhgMZSguxzBEHLNRTVtlEeLZNz1%40Db17dDFC8zv7u%40ZPuxtfvSulnDjnCENTHEHH%40NXBvzXX3M%40J2mmiJ4Y&l=19'.format(uid)

    headers = {'User-Agent': get_headers()}
    result = requests.get(url,headers=headers).content.decode('utf-8')
    json_data = json.loads(result)
    content = json_data['content']

    if not "geo" in content:
        return None
    geo = content['geo']
    i = 0
    strsss = ''
    for jj in str(geo).split('|')[2].split('-')[1].split(','):
        jj = str(jj).strip(';')
        if i % 2 == 0:
            strsss = strsss + str(jj) + ','
        else:
            strsss = strsss + str(jj) + ';'
        i = i + 1
    return strsss.strip(";")

def transform_coordinate_batch(geo_list):
    """
    坐标转换(百米坐标转化为百度坐标)

    """
    ak = ''
    coord_list = list()
    for geo in geo_list:
        url = 'http://api.map.baidu.com/geoconv/v1/?' \
              'coords={}&' \
              'from=6&to=5&ak={}'.format(geo,ak)
        headers = {'User-Agent': get_headers()}
        result = requests.get(url, headers=headers).content.decode('utf-8')
        json_data = json.loads(result)
        coord = ''
        if json_data['status'] == 0:
            coords_infor = json_data['result']
            if len(coords_infor) > 0:
                for coord_infor in coords_infor:
                    lng = coord_infor['x']
                    lat = coord_infor['y']
                    coord = str(lng) + "," + str(lat)
                    coord_list.append(coord)
    return coord_list


def main():
    uid = '74c933fb399fbf5e9f82ea84'
    geo_list = get_boundary(uid).split(';')
    coord_list = transform_coordinate_batch(geo_list)
    for coord in coord_list:
        print(coord)


if __name__ == '__main__':
    main()