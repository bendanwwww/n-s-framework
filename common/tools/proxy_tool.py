import requests

tunnel = "r518.kdlfps.com:18866"

username = "f2578615222"
password = "6z4ama40"

proxy_http = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
proxy_https = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
proxies = {
    "http": proxy_http,
    "https": proxy_https
}

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_unv_aid=2ac5017694ae41fcc26dfa9bde97eeca; __td_signed=true; _ga=GA1.1.946796567.1725169859; _im_vid=01J6P25ZVZ5SMB9D6K4AKXJMKV; _pubcid=9aafa188-cbb5-4448-9991-6d85e20e0492; _pubcid_cst=zix7LPQsHA%3D%3D; ks2=t4xexuda4vzw; sasieno=0; lineheight=0; fontsize=0; novellayout=1; fix_menu_bar=1; _im_vid=01J6P25ZVZ5SMB9D6K4AKXJMKV; _im_vid=01J6P25ZVZ5SMB9D6K4AKXJMKV; _flux_dataharbor=1; __pmguid_=a058e59d-a594-4035-b7aa-3764fe9f4e09; __mguid_=10f9287d669d343325qui800ly5jpqs7; adr_id=5WNBA2vv4t971ja3lj9MtlKclVoPXiXtqV2AlkgpZjsVWptA; nlist1=19eed.1-1d0t5.2; _yjsu_yjad=1725181715.5909c44c-ae67-4c59-aa23-8cd689e2b2df; _unv_id=01J6HVNGNS8SADJEC96RVJGS00; _ga_2YQV7PZTL9=GS1.1.1725257298.5.1.1725259322.0.0.0; cto_bundle=9d-e1l9RJTJGdXQlMkZ5RGdZTldqOWglMkZFaWpHYk5scFFpVVVKWWclMkJ2YnpjUmlPVjVjVE5xWGdPSXBza28lMkZ6Wm9lMVUlMkJpRTFJMHhwTTVRcjc3T09LV2ZBNGdDWiUyRkk4TnRmWWxhckVmNkwyRjVtZXdGUUd2c3FKRXJEc0pkNXRnNzVpSkplSXhZWTJQRkxWZlFNTEt0ak5zdzJDSUVFcVN1RGhBdDkxQXhONFI3U0RrTWQ5dDloTkdlU2dPMEV0MDkwS2ZwalFaNA; cto_bidid=YrKBt19PYUlUQTVCQmRpbyUyRjVNMThPU3JkNGk5d0pvTnQ5Tjl2T3VWYklYaHh4N2REZEE2aVYlMkZnYyUyQjNwVzdzZHVhajBtQnZRSEhLWDB6OERJWWc1aHhrZFRaa05QTHoySHpMTlNvWVdaaExYTTk2Qms3OEdjZzMzeW8lMkZPaUhEZ2RYWTZyWWZNekFpJTJGZENJZEMxS09WQWc2czVBJTNEJTNE; _ga_1TH9CF4FPC=GS1.1.1725254792.7.1.1725260417.0.0.0; __gads=ID=057fdd661442b3ea:T=1725170375:RT=1725260417:S=ALNI_MaNNnQFHGVsAdGfqXp2Ys7tbZadgw; __gpi=UID=00000ee44d280bfd:T=1725170375:RT=1725260417:S=ALNI_MbrTE7NFjPa0yQrFDHK2va-kStm0g; __eoi=ID=7771f53c73aa71c8:T=1725170375:RT=1725260417:S=AA-AfjaRk9BV_ngFXLoUSMkQHTj9; _td=06de911a-ca6a-4890-8e03-1c8b10bd8063',
        'Host': 'yomou.syosetu.com',
        'Referer': 'https://yomou.syosetu.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        }
# response = requests.get('https://yomou.syosetu.com/search.php?&type=er&order_former=search&word=&order=new&notnizi=1&p=1', headers=headers, proxies=proxies)
# print(response) 
    