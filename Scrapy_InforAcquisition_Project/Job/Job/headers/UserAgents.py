
import random
import requests

def get_headers():
    user_agent_list =  [
        "Mozilla/4.0 (Macintosh) AppleWebKit/16.42 (KHTML, like Gecko) Firefox/29.0 Safari/506.92",
        "Mozilla/5.0 (Macintosh) AppleWebKit/50.77 (KHTML, like Gecko) Firefox/54.0 Safari/480.36",
        "Mozilla/5.0 (Macintosh) AppleWebKit/19.81 (KHTML, like Gecko) Firefox/34.0 Safari/226.97",
        "Mozilla/5.0 (X11) AppleWebKit/4.79 (KHTML, like Gecko) Firefox/53.0 Safari/479.8",
        "Mozilla/4.0 (Macintosh) AppleWebKit/22.16 (KHTML, like Gecko) Firefox/66.0 Safari/132.96",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/71.44 (KHTML, like Gecko) Firefox/46.0 Safari/159.80",
        "Mozilla/5.0 (X11) AppleWebKit/71.85 (KHTML, like Gecko) Firefox/42.0 Safari/518.3",
        "Mozilla/5.0 (Macintosh) AppleWebKit/7.77 (KHTML, like Gecko) Chrome/48.2.1401.285 Safari/580.84",
        "Mozilla/4.0 (Macintosh) AppleWebKit/58.86 (KHTML, like Gecko) Firefox/46.0 Safari/200.38",
        "Mozilla/5.0 (Macintosh) AppleWebKit/55.89 (KHTML, like Gecko) Chrome/65.3.4543.227 Safari/398.3",
        "Mozilla/5.0 (Macintosh) AppleWebKit/20.33 (KHTML, like Gecko) Edge/15.11953 Safari/167.92",
        "Mozilla/4.0 (X11) AppleWebKit/26.95 (KHTML, like Gecko) Firefox/59.0 Safari/573.13",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/76.12 (KHTML, like Gecko) Edge/18.11501 Safari/124.66",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/61.21 (KHTML, like Gecko) Chrome/59.2.3298.94 Safari/289.37",
        "Mozilla/4.0 (Windows NT 6.1) AppleWebKit/17.58 (KHTML, like Gecko) Edge/15.12324 Safari/508.33",
        "Mozilla/5.0 (Macintosh) AppleWebKit/70.49 (KHTML, like Gecko) Firefox/63.0 Safari/117.37",
        "Mozilla/4.0 (X11) AppleWebKit/19.95 (KHTML, like Gecko) Edge/18.19684 Safari/196.55",
        "Mozilla/5.0 (Macintosh) AppleWebKit/72.46 (KHTML, like Gecko) Edge/17.10920 Safari/578.68",
        "Mozilla/4.0 (X11) AppleWebKit/6.24 (KHTML, like Gecko) Edge/14.18128 Safari/565.70",
        "Mozilla/4.0 (Windows NT 6.0) AppleWebKit/97.51 (KHTML, like Gecko) Firefox/42.0 Safari/287.52",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/88.18 (KHTML, like Gecko) Firefox/29.0 Safari/310.29",
        "Mozilla/5.0 (Macintosh) AppleWebKit/23.37 (KHTML, like Gecko) Firefox/23.0 Safari/545.28",
        "Mozilla/4.0 (Macintosh) AppleWebKit/54.24 (KHTML, like Gecko) Firefox/32.0 Safari/499.76",
        "Mozilla/4.0 (Macintosh) AppleWebKit/4.37 (KHTML, like Gecko) Chrome/65.2.4816.347 Safari/499.37",
        ]
    #随机选取请求头
    UserAgent = random.choice(user_agent_list)
    return UserAgent