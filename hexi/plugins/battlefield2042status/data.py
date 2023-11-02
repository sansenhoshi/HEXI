import asyncio
import json

import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry

from .bf2042 import bf_2042_gen_pic, bf2042_weapon


async def query_data(player, platform, query_type):
    url = f"https://api.gametools.network/bf2042/stats/?raw=false&format_values=true&name={player}&platform={platform}"
    headers = {
        'accept': 'application/json'
    }
    mes = (False, "没有获取到数据呢")
    retry_options = ExponentialRetry(attempts=2, exceptions=(aiohttp.ClientError,))
    async with RetryClient(retry_options=retry_options) as session:
        try:
            async with session.get(url, headers=headers, timeout=15) as response:
                rest = await response.text()
                rest = str_filter(rest)
                if response.status == 200:
                    result = json.loads(rest)
                    if query_type == 0:
                        img = await bf_2042_gen_pic(result, platform)
                        mes = (True, img)
                    elif query_type == 1:
                        img = await bf2042_weapon(result, platform)
                        mes = (True, img)
                else:
                    mes = (False, "请求错误")
        except asyncio.TimeoutError as e:
            if e:
                mes = (False, f"请求超时：{e}")
            mes = (False, f"请求超时：玩家数据请求超时")
        except aiohttp.ClientError as e:
            if e:
                mes = (False, f"请求异常：{e}")
            mes = (False, f"请求异常：玩家数据请求异常")
    return mes


obj_filter = {
    "AH-64GX Apache Warchief": "Apache Warchief",
    "GOL Sniper Magnum": "GOL Magnum",
    "AH-6J Little Bird": "Little Bird",
    "Sd. Kfz 251 Halftrack": "251 Halftrack",
    "9K22 Tunguska-M": "Tunguska-M"
}


def str_filter(obj_str):
    # 遍历字典，替换字符串中的键为对应的值
    for key in obj_filter:
        obj_str = obj_str.replace(key, obj_filter[key])
    return obj_str
