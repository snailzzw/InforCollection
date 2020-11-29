"""自动翻译(百度)"""

from InforCollection.headers.UserAgents import get_headers
import requests
import json
import re
import execjs


class AutoTranslation:

    def __init__(self):
        """
        query ：需要翻译的内容
        url ：翻译接口
        lang ：输入语言

       """
        self.query = input('>')
        self.url = 'https://fanyi.baidu.com/v2transapi'

    @staticmethod
    def get_lang(query):
        url = 'https://fanyi.baidu.com/langdetect'
        headers = {
            'User-Agent': get_headers(),
            'Cookie': 'BAIDUID=7FD0412FAAD4330FF200A81055995783:FG=1; BAIDUID_BFESS=7FD0412FAAD4330FF200A81055995783:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1606117276; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1606117443; __yjsv5_shitong=1.0_7_342e47f274f0b0479c666c81efa3d18ca4a9_300_1606117442884_221.194.139.117_3a134ef6; yjs_js_security_passport=d791e604171c2b5814dd935b42190b97de9e5cf9_1606117444_js',
            'origin': 'https://fanyi.baidu.com',
            'referer': 'https://fanyi.baidu.com/'
        }
        data = {
            'query': query,
        }
        response = requests.post(url=url, data=data, headers=headers)
        content = json.loads(response.content.decode('utf-8'))
        return content["lan"]

    @staticmethod
    def get_data(query):
        """

        获取sign和token
        """
        url = 'https://fanyi.baidu.com/'
        headers = {
            'User-Agent': get_headers(),
            'Cookie': 'BAIDUID=7FD0412FAAD4330FF200A81055995783:FG=1; BAIDUID_BFESS=7FD0412FAAD4330FF200A81055995783:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1606117276; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1606117443; __yjsv5_shitong=1.0_7_342e47f274f0b0479c666c81efa3d18ca4a9_300_1606117442884_221.194.139.117_3a134ef6; yjs_js_security_passport=d791e604171c2b5814dd935b42190b97de9e5cf9_1606117444_js',
        }
        content = requests.get(url=url, headers=headers).content.decode('utf-8')
        # 全局搜索token和gtk
        token = re.findall(r"token: '(.*?)'", content)[0]
        gtk = re.findall(r"<script>window.bdstoken = '';window.gtk = '(.*?)';</script>", content)[0]
        with open("./baidu.js", "r", encoding='utf-8') as f:
            js = f.read()
        js = js.replace('u = null !== i ? i : (i = window[l] || "") || "";', 'u= "%s"' % gtk)
        cxt = execjs.compile(js)
        # 调用方法
        sign = cxt.call("e", query)
        return sign, token

    def run(self):
        lang = self.get_lang(self.query)
        sign, token = self.get_data(self.query)
        # 如果输入是中文
        if lang == "zh":
            data = {
                'from': 'zh',
                'to': 'en',
                'query': self.query,
                'simple_means_flag': '3',
                'sign': sign,
                'token': token,
                'domain': 'common',
            }
        else:
            data = {
                'from': 'en',
                'to': 'zh',
                'query': self.query,
                'simple_means_flag': '3',
                'sign': sign,
                'token': token,
                'domain': 'common',
            }
        headers = {
            "authority": "fanyi.baidu.com",
            "method": "POST",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "BAIDUID=7FD0412FAAD4330FF200A81055995783:FG=1; BAIDUID_BFESS=7FD0412FAAD4330FF200A81055995783:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1606117276; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1606117443; __yjsv5_shitong=1.0_7_342e47f274f0b0479c666c81efa3d18ca4a9_300_1606117442884_221.194.139.117_3a134ef6; yjs_js_security_passport=d791e604171c2b5814dd935b42190b97de9e5cf9_1606117444_js",
            "origin": "https://fanyi.baidu.com",
            "referer": "https://fanyi.baidu.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": get_headers(),
            "x-requested-with": "XMLHttpRequest",
        }
        response = requests.post(url=self.url, data=data, headers=headers)
        content = response.content.decode('utf-8')
        content = json.loads(content)
        print('翻译结果：', content["trans_result"]["data"][0]["dst"])


if __name__ == '__main__':
    while True:
        auto_translation = AutoTranslation()
        auto_translation.run()
        choice = input('是否继续(y/n)')
        if choice == 'n':
            break