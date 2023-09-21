import asyncio
import pprint
import time
import json
import random
import re
import fake_useragent
from httpx import AsyncClient
from httpx_socks import AsyncProxyTransport
import logging

logging.basicConfig(level=logging.DEBUG)

def load_proxy_socks4():
    with open("proxy_files/socks4_proxies.txt", "rt", encoding='utf-8') as f:
        proxy_data = f.read()
        proxy_list = proxy_data.split("\n")
        return proxy_list

def store_proxy_socks4(proxy_list):
    with open("proxy_files/socks4_proxies_final.json", "wt", encoding='utf-8') as f:
        json.dump(proxy_list, f, indent=4, ensure_ascii=False)

def load_proxy_socks5():
    with open("proxy_files/socks5_proxies.txt", "rt", encoding='utf-8') as f:
        proxy_data = f.read()
        proxy_list = proxy_data.split("\n")
        return proxy_list

def store_proxy_socks5(proxy_list):
    with open("proxy_files/socks5_proxies_final.json", "wt", encoding='utf-8') as f:
        json.dump(proxy_list, f, indent=4, ensure_ascii=False)

def processing_socks4():
    result = []
    final = []
    data = load_proxy_socks4()
    for i in data:
        port = re.search(r':(\d+)', i)
        ip = re.search(r'(\d.+):', i)
        if ip:
            # 매치된 숫자를 가져옴
            ip_number = ip.group(1)
            #print("추출된 ip 번호:", ip_number)
        if port:
            # 매치된 숫자를 가져옴
            port_number = port.group(1)
            #print("추출된 포트 번호:", port_number)
        result.append({"protocol": "socks4",
                      "ip": ip_number,
                      "port": port_number})

    asyncio.run(async_proxy_test(data=result, result=final))
    store_proxy_socks4(final)

def processing_socks5():
    result = []
    final = []
    data = load_proxy_socks4()
    for i in data:
        port = re.search(r':(\d+)', i)
        ip = re.search(r'(\d.+):', i)
        if ip:
            # 매치된 숫자를 가져옴
            ip_number = ip.group(1)
            #print("추출된 ip 번호:", ip_number)
        if port:
            # 매치된 숫자를 가져옴
            port_number = port.group(1)
            #print("추출된 포트 번호:", port_number)
        result.append({"protocol": "socks5",
                      "ip": ip_number,
                      "port": port_number})
    asyncio.run(async_proxy_test(data=result, result=final))
    store_proxy_socks5(final)


async def async_proxy_test(data, result):
    start = time.time()
    random.shuffle(data)
    await asyncio.gather(
        *[proxy_test(result, proxy_data=proxy_data) for proxy_data in data],
    )
    pprint.pprint(result)
    end = time.time()
    print(f"실행 시간: {end - start}")
    return result

async def proxy_test(result:list, proxy_data: dict):
    ip = proxy_data["ip"]
    port = proxy_data["port"]
    protocol = proxy_data["protocol"]

    #proxy = {
    #    "all://": "{}://{}:{}".format(protocol,ip, port)
    #}
    proxy = f"{protocol}://{ip}:{port}"

    headers = {'User-Agent': fake_useragent.FakeUserAgent().random}
    test_url = 'https://api.myip.com/'

    transport = AsyncProxyTransport.from_url(proxy, verify=False)

    try:
        async with AsyncClient(transport=transport) as client:
            res = await client.get(test_url, headers=headers, timeout=10)
            logging.debug(res.json())
            print(res.json())
            #print(json.dumps(proxy, indent=4, ensure_ascii=False, escape_forward_slashes=False))
            #print(json.dumps(res.json(), indent=4, ensure_ascii=False, escape_forward_slashes=False))
    except Exception as e:
        print(e)
    else:
        result.append({
            "ip": ip,
            "port": port,
            "protocol": protocol
        })
    return result


if __name__ == '__main__':
    processing_socks4()
    processing_socks5()