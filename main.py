import base64
import json
import random
import re
import execjs
import requests

YmToken = 'your token'


class fuckYiDun:
    def __init__(self):
        with open(r'captcha.js', 'r', encoding="UTF-8") as f:
            js_code = f.read()
        self.context = execjs.compile(js_code)

    def verify_captcha(self, imgUrl, extra):
        b = base64.b64encode(requests.get(url=imgUrl, verify=False).content).decode()  ## 图片二进制流base64字符串

        url = "http://api.jfbym.com/api/YmServer/customApi"
        data = {
            "token": f"{YmToken}",
            "type": "30109",
            "image": b,
            'extra': extra,
        }
        _headers = {
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, headers=_headers, json=data, verify=False)
        response_json = json.loads(response.text)
        match str(response_json['code']):
            case "10000":
                pos = re.split(',', response_json['data']['data'])
                # print(response.text)
                return {'x': pos[0], 'y': pos[1]}
            case "10007":  # 图片未识别成功
                return {'x': 0, 'y': 0}
            case default:
                return {'x': 0, 'y': 0}

    def get_captcha(self):
        url = "https://c.dun.163.com/api/v3/get"

        params = {
            'referer': "https://passport.zhihuishu.com/login",
            'zoneId': "CN31",
            'dt': "b5DXwG/a9aZBQ0FABRfU39Q3G7Ufu2nt",
            'acToken': "9ca17ae2e6ffcda170e2e6eeb8bc33b7b6f794ed4a97b08aa6c85a878f9a82db60af9af9a3b35f88919aade52af0feaec3b92a8698bc96f35c9cf18393ee5b928b9ea6d44a908d988ad57f8a9cbcb3d0489887ee9e",
            'id': "4da3050565514a35a50541b0e1f54538",
            'fp': f"{self.context.call('get_fp')}",
            'https': "true",
            'type': "undefined",
            'version': "2.27.2",
            'dpr': "1",
            'dev': "1",
            'cb': f"{self.context.call('get_cb')}",
            'ipv6': "false",
            'runEnv': "10",
            'group': "",
            'scene': "",
            'lang': "zh-CN",
            'sdkVersion': "undefined",
            'iv': "4",
            'width': "320",
            'audio': "false",
            'sizeType': "10",
            'smsVersion': "v3",
            'token': "",
            'callback': "__JSONP_d96qd9m_0"
        }

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': "\"Windows\"",
            'sec-ch-ua': "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            'sec-ch-ua-mobile': "?0",
            'Sec-Fetch-Site': "cross-site",
            'Sec-Fetch-Mode': "no-cors",
            'Sec-Fetch-Dest': "script",
            'Referer': "https://passport.zhihuishu.com/",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Cookie': "NTES_P_UTID=Chbh7P5iLKaEPs2QDF75JV7xup37cAVb|1713068720"
        }

        response = requests.get(url, params=params, headers=headers, verify=False)
        json_str = re.search(r'\{.*\}', response.text).group()

        data = json.loads(json_str).get('data', '')
        return {'imgUrl': data.get('bg', '')[0], 'extra':
            data.get('front', ''), 'token': data.get('token', '')}

    def get_vaildate(self):
        data = self.get_captcha()
        pos = self.verify_captcha(data['imgUrl'], data['extra'])
        params_data = self.context.call('get_data', f'{data['token']}', f'{pos['x']}', f'{pos['y']}',
                                        f'{random.randint(1000, 4000)}')

        url = "https://c.dun.163.com/api/v3/check"

        params = {
            'referer': "https://passport.zhihuishu.com/login",
            'zoneId': "CN31",
            'dt': "/Ga8LfObxzJFQhFFQEfGC1kSTYlcKDuC",
            'id': "4da3050565514a35a50541b0e1f54538",
            'token': f"{data['token']}",
            'acToken': "undefined",
            'data': f"{params_data}",
            'width': "320",
            'type': "11",
            'version': "2.27.2",
            'cb': f"{self.context.call('get_cb')}",
            'extraData': "",
            'bf': "0",
            'runEnv': "10",
            'sdkVersion': "undefined",
            'iv': "4",
            'callback': "__JSONP_wtj5sop_2"
        }

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': "\"Windows\"",
            'sec-ch-ua': "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            'sec-ch-ua-mobile': "?0",
            'Sec-Fetch-Site': "cross-site",
            'Sec-Fetch-Mode': "no-cors",
            'Sec-Fetch-Dest': "script",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Cookie': "NTES_P_UTID=Chbh7P5iLKaEPs2QDF75JV7xup37cAVb|1713068720"
        }

        response = requests.get(url, params=params, headers=headers, verify=False)
        json_str = re.search(r'\{.*\}', response.text).group()
        data = json.loads(json_str).get('data', '')
        try:
            validate = data['validate']
            if validate == '':
                return f'验证失败'
            return validate
        except Exception as e:
            return f'验证发生错误: {Exception}'


if __name__ == "__main__":
    fucker = fuckYiDun()
    print(fucker.get_vaildate())
