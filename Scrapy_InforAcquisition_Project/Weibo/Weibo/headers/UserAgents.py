
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
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/20.86 (KHTML, like Gecko) Edge/17.17714 Safari/581.10",
        "Mozilla/5.0 (X11) AppleWebKit/72.20 (KHTML, like Gecko) Firefox/33.0 Safari/510.57",
        "Mozilla/4.0 (Macintosh) AppleWebKit/61.14 (KHTML, like Gecko) Edge/16.10770 Safari/414.59",
        "Mozilla/5.0 (X11) AppleWebKit/36.69 (KHTML, like Gecko) Firefox/30.0 Safari/387.34",
        "Mozilla/5.0 (Macintosh) AppleWebKit/57.10 (KHTML, like Gecko) Chrome/68.2.1402.283 Safari/325.33",
        "Mozilla/5.0 (Macintosh) AppleWebKit/39.29 (KHTML, like Gecko) Firefox/61.0 Safari/225.34",
        "Mozilla/5.0 (Macintosh) AppleWebKit/64.63 (KHTML, like Gecko) Firefox/31.0 Safari/487.68",
        "Mozilla/4.0 (Macintosh) AppleWebKit/60.13 (KHTML, like Gecko) Firefox/66.0 Safari/532.51",
        "Mozilla/4.0 (Windows NT 6.1) AppleWebKit/83.12 (KHTML, like Gecko) Firefox/31.0 Safari/358.42",
        "Mozilla/5.0 (Macintosh) AppleWebKit/26.37 (KHTML, like Gecko) Firefox/25.0 Safari/513.42",
        "Mozilla/4.0 (Windows NT 6.1) AppleWebKit/99.3 (KHTML, like Gecko) Edge/14.14737 Safari/476.95",
        "Mozilla/4.0 (Macintosh) AppleWebKit/67.59 (KHTML, like Gecko) Firefox/27.0 Safari/545.19",
        "Mozilla/4.0 (Macintosh) AppleWebKit/93.7 (KHTML, like Gecko) Firefox/41.0 Safari/426.50",
        "Mozilla/5.0 (X11) AppleWebKit/43.39 (KHTML, like Gecko) Firefox/32.0 Safari/302.30",
        "Mozilla/5.0 (Macintosh) AppleWebKit/40.62 (KHTML, like Gecko) Chrome/62.2.4875.103 Safari/108.71",
        "Mozilla/5.0 (Macintosh) AppleWebKit/27.51 (KHTML, like Gecko) Firefox/25.0 Safari/221.99",
        "Mozilla/5.0 (Macintosh) AppleWebKit/41.87 (KHTML, like Gecko) Firefox/50.0 Safari/570.66",
        "Mozilla/4.0 (X11) AppleWebKit/96.45 (KHTML, like Gecko) Edge/16.18676 Safari/194.17",
        "Mozilla/5.0 (X11) AppleWebKit/44.34 (KHTML, like Gecko) Edge/15.10208 Safari/424.28",
        "Mozilla/4.0 (X11) AppleWebKit/40.55 (KHTML, like Gecko) Edge/17.18647 Safari/388.97",
        "Mozilla/5.0 (Macintosh) AppleWebKit/53.41 (KHTML, like Gecko) Firefox/60.0 Safari/365.43",
        "Mozilla/4.0 (X11) AppleWebKit/78.4 (KHTML, like Gecko) Firefox/66.0 Safari/157.59",
        "Mozilla/5.0 (X11) AppleWebKit/13.74 (KHTML, like Gecko) Firefox/25.0 Safari/255.38",
        "Mozilla/5.0 (Macintosh) AppleWebKit/72.81 (KHTML, like Gecko) Firefox/28.0 Safari/482.65",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/88.26 (KHTML, like Gecko) Firefox/51.0 Safari/298.29",
        "Mozilla/4.0 (Macintosh) AppleWebKit/2.18 (KHTML, like Gecko) Firefox/45.0 Safari/433.16",
        "Mozilla/4.0 (Macintosh) AppleWebKit/98.13 (KHTML, like Gecko) Firefox/42.0 Safari/102.48",
        "Mozilla/4.0 (X11) AppleWebKit/28.74 (KHTML, like Gecko) Firefox/41.0 Safari/385.88",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/32.4 (KHTML, like Gecko) Chrome/57.0.4645.472 Safari/225.84",
        "Mozilla/5.0 (Macintosh) AppleWebKit/37.13 (KHTML, like Gecko) Firefox/21.0 Safari/161.45",
        "Mozilla/5.0 (Macintosh) AppleWebKit/86.58 (KHTML, like Gecko) Chrome/64.2.3185.203 Safari/434.55",
        "Mozilla/4.0 (Windows NT 10.0) AppleWebKit/48.80 (KHTML, like Gecko) Firefox/64.0 Safari/260.57",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/95.72 (KHTML, like Gecko) Firefox/53.0 Safari/442.57",
        "Mozilla/5.0 (X11) AppleWebKit/29.92 (KHTML, like Gecko) Edge/16.17817 Safari/256.64",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/15.4 (KHTML, like Gecko) Firefox/45.0 Safari/158.32",
        "Mozilla/4.0 (Macintosh) AppleWebKit/32.83 (KHTML, like Gecko) Firefox/62.0 Safari/347.97",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/88.0 (KHTML, like Gecko) Chrome/47.0.2910.188 Safari/324.5",
        "Mozilla/4.0 (Windows NT 5.2) AppleWebKit/24.79 (KHTML, like Gecko) Edge/13.11553 Safari/531.48",
        "Mozilla/4.0 (Windows NT 6.0) AppleWebKit/26.85 (KHTML, like Gecko) Firefox/22.0 Safari/198.67",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/90.32 (KHTML, like Gecko) Firefox/33.0 Safari/548.74",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/86.87 (KHTML, like Gecko) Firefox/45.0 Safari/222.28",
        "Mozilla/5.0 (Macintosh) AppleWebKit/44.49 (KHTML, like Gecko) Firefox/37.0 Safari/167.1",
        "Mozilla/5.0 (Macintosh) AppleWebKit/88.63 (KHTML, like Gecko) Firefox/48.0 Safari/481.42",
        "Mozilla/4.0 (Windows NT 10.0) AppleWebKit/30.0 (KHTML, like Gecko) Firefox/53.0 Safari/579.70",
        "Mozilla/4.0 (X11) AppleWebKit/70.27 (KHTML, like Gecko) Firefox/52.0 Safari/448.64",
        "Mozilla/5.0 (Macintosh) AppleWebKit/45.68 (KHTML, like Gecko) Firefox/49.0 Safari/597.96",
        "Mozilla/4.0 (Macintosh) AppleWebKit/43.22 (KHTML, like Gecko) Edge/17.18394 Safari/339.96",
        "Mozilla/4.0 (Macintosh) AppleWebKit/61.84 (KHTML, like Gecko) Firefox/62.0 Safari/477.60",
        "Mozilla/4.0 (Macintosh) AppleWebKit/83.57 (KHTML, like Gecko) Firefox/34.0 Safari/180.76",
        "Mozilla/4.0 (Macintosh) AppleWebKit/92.95 (KHTML, like Gecko) Chrome/50.1.4581.337 Safari/378.24",
        "Mozilla/5.0 (Macintosh) AppleWebKit/55.64 (KHTML, like Gecko) Chrome/52.1.1744.129 Safari/320.66",
        "Mozilla/4.0 (Windows NT 6.1) AppleWebKit/63.48 (KHTML, like Gecko) Edge/15.16284 Safari/433.95",
        "Mozilla/4.0 (Macintosh) AppleWebKit/35.55 (KHTML, like Gecko) Chrome/66.2.2649.95 Safari/195.86",
        "Mozilla/4.0 (Macintosh) AppleWebKit/56.72 (KHTML, like Gecko) Edge/18.10492 Safari/238.67",
        "Mozilla/4.0 (Macintosh) AppleWebKit/45.75 (KHTML, like Gecko) Chrome/66.2.3723.420 Safari/269.95",
        "Mozilla/4.0 (Windows NT 6.1) AppleWebKit/63.84 (KHTML, like Gecko) Firefox/62.0 Safari/161.90",
        "Mozilla/5.0 (Macintosh) AppleWebKit/38.45 (KHTML, like Gecko) Firefox/65.0 Safari/424.95",
        "Mozilla/4.0 (Macintosh) AppleWebKit/59.20 (KHTML, like Gecko) Firefox/47.0 Safari/250.81",
        "Mozilla/5.0 (Macintosh) AppleWebKit/37.34 (KHTML, like Gecko) Chrome/59.1.1390.386 Safari/591.70",
        "Mozilla/5.0 (Macintosh) AppleWebKit/21.75 (KHTML, like Gecko) Firefox/61.0 Safari/164.16",
        "Mozilla/4.0 (Macintosh) AppleWebKit/40.12 (KHTML, like Gecko) Firefox/56.0 Safari/222.6",
        "Mozilla/4.0 (Macintosh) AppleWebKit/27.42 (KHTML, like Gecko) Firefox/31.0 Safari/304.98",
        "Mozilla/5.0 (X11) AppleWebKit/95.95 (KHTML, like Gecko) Firefox/22.0 Safari/182.23",
        "Mozilla/5.0 (Macintosh) AppleWebKit/69.86 (KHTML, like Gecko) Firefox/59.0 Safari/266.78",
        "Mozilla/5.0 (Macintosh) AppleWebKit/9.83 (KHTML, like Gecko) Edge/15.16570 Safari/323.35",
        "Mozilla/5.0 (Macintosh) AppleWebKit/89.45 (KHTML, like Gecko) Firefox/25.0 Safari/260.31",
        "Mozilla/4.0 (Windows NT 6.1) AppleWebKit/70.59 (KHTML, like Gecko) Chrome/67.3.4307.313 Safari/495.19",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/24.48 (KHTML, like Gecko) Chrome/63.2.4090.309 Safari/142.53",
        "Mozilla/5.0 (X11) AppleWebKit/37.92 (KHTML, like Gecko) Firefox/50.0 Safari/126.66",
        "Mozilla/5.0 (Macintosh) AppleWebKit/86.58 (KHTML, like Gecko) Chrome/72.0.3894.492 Safari/318.89",
        "Mozilla/4.0 (X11) AppleWebKit/50.62 (KHTML, like Gecko) Firefox/57.0 Safari/167.43",
        "Mozilla/4.0 (Macintosh) AppleWebKit/60.31 (KHTML, like Gecko) Chrome/57.1.1406.158 Safari/135.82",
        "Mozilla/4.0 (Macintosh) AppleWebKit/89.46 (KHTML, like Gecko) Chrome/60.3.4229.387 Safari/381.99",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/82.2 (KHTML, like Gecko) Edge/16.19550 Safari/416.16",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/19.37 (KHTML, like Gecko) Chrome/48.0.2389.292 Safari/373.44",
        "Mozilla/5.0 (Macintosh) AppleWebKit/46.79 (KHTML, like Gecko) Edge/16.12357 Safari/139.27",
        "Mozilla/4.0 (Windows NT 6.0) AppleWebKit/52.87 (KHTML, like Gecko) Edge/13.12112 Safari/284.94",
        "Mozilla/5.0 (X11) AppleWebKit/10.27 (KHTML, like Gecko) Chrome/50.1.2893.151 Safari/413.84",
        "Mozilla/5.0 (Macintosh) AppleWebKit/28.44 (KHTML, like Gecko) Chrome/49.0.4876.457 Safari/390.75",
        "Mozilla/5.0 (X11) AppleWebKit/43.47 (KHTML, like Gecko) Firefox/34.0 Safari/541.79",
        "Mozilla/4.0 (Windows NT 6.0) AppleWebKit/35.30 (KHTML, like Gecko) Edge/17.11827 Safari/383.97",
        "Mozilla/5.0 (Macintosh) AppleWebKit/82.3 (KHTML, like Gecko) Chrome/71.3.1703.360 Safari/506.57",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/97.48 (KHTML, like Gecko) Chrome/49.1.4287.441 Safari/176.75",
        "Mozilla/4.0 (Macintosh) AppleWebKit/77.87 (KHTML, like Gecko) Chrome/48.2.3810.491 Safari/177.67",
        "Mozilla/4.0 (Macintosh) AppleWebKit/39.76 (KHTML, like Gecko) Edge/15.19873 Safari/175.3",
        "Mozilla/4.0 (X11) AppleWebKit/54.61 (KHTML, like Gecko) Chrome/54.0.4660.185 Safari/304.93",
        "Mozilla/5.0 (X11) AppleWebKit/76.97 (KHTML, like Gecko) Firefox/28.0 Safari/206.39",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/40.31 (KHTML, like Gecko) Chrome/59.2.3179.122 Safari/161.33",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/1.37 (KHTML, like Gecko) Chrome/54.2.4328.286 Safari/329.83",
        "Mozilla/4.0 (Windows NT 6.0) AppleWebKit/17.11 (KHTML, like Gecko) Firefox/53.0 Safari/590.43",
        "Mozilla/5.0 (X11) AppleWebKit/76.30 (KHTML, like Gecko) Firefox/40.0 Safari/566.4",
        "Mozilla/5.0 (Macintosh) AppleWebKit/85.87 (KHTML, like Gecko) Firefox/46.0 Safari/234.25",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/96.41 (KHTML, like Gecko) Firefox/34.0 Safari/409.68",
        "Mozilla/5.0 (Macintosh) AppleWebKit/44.5 (KHTML, like Gecko) Chrome/61.1.1652.453 Safari/402.65",
        "Mozilla/4.0 (X11) AppleWebKit/81.29 (KHTML, like Gecko) Chrome/72.0.3790.80 Safari/347.64",
        "Mozilla/4.0 (X11) AppleWebKit/4.29 (KHTML, like Gecko) Chrome/60.0.4153.381 Safari/319.88",
        "Mozilla/5.0 (Macintosh) AppleWebKit/84.78 (KHTML, like Gecko) Edge/16.11452 Safari/561.71",
        "Mozilla/5.0 (X11) AppleWebKit/10.65 (KHTML, like Gecko) Firefox/54.0 Safari/145.99",
        "Mozilla/4.0 (X11) AppleWebKit/38.56 (KHTML, like Gecko) Chrome/49.1.1295.433 Safari/189.51",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/51.58 (KHTML, like Gecko) Firefox/55.0 Safari/518.45",
        "Mozilla/5.0 (X11) AppleWebKit/64.76 (KHTML, like Gecko) Firefox/26.0 Safari/133.77",
        "Mozilla/4.0 (Windows NT 6.1) AppleWebKit/3.90 (KHTML, like Gecko) Chrome/54.1.4541.276 Safari/411.65",
        "Mozilla/4.0 (Macintosh) AppleWebKit/57.6 (KHTML, like Gecko) Edge/17.15387 Safari/345.25",
        "Mozilla/4.0 (Macintosh) AppleWebKit/89.18 (KHTML, like Gecko) Edge/16.11032 Safari/184.83",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/37.49 (KHTML, like Gecko) Firefox/62.0 Safari/283.9",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/57.40 (KHTML, like Gecko) Chrome/60.1.2695.67 Safari/376.62",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/19.19 (KHTML, like Gecko) Firefox/45.0 Safari/546.10",
        "Mozilla/5.0 (Macintosh) AppleWebKit/94.100 (KHTML, like Gecko) Firefox/40.0 Safari/479.64",
        "Mozilla/4.0 (X11) AppleWebKit/97.85 (KHTML, like Gecko) Edge/17.17724 Safari/504.30",
        "Mozilla/4.0 (Macintosh) AppleWebKit/80.74 (KHTML, like Gecko) Chrome/66.3.1918.222 Safari/511.18",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/11.18 (KHTML, like Gecko) Firefox/60.0 Safari/593.44",
        "Mozilla/4.0 (Macintosh) AppleWebKit/94.33 (KHTML, like Gecko) Chrome/49.1.2478.50 Safari/355.56",
        "Mozilla/5.0 (X11) AppleWebKit/9.53 (KHTML, like Gecko) Firefox/62.0 Safari/344.46",
        "Mozilla/4.0 (X11) AppleWebKit/62.34 (KHTML, like Gecko) Firefox/59.0 Safari/344.62",
        "Mozilla/5.0 (Macintosh) AppleWebKit/69.24 (KHTML, like Gecko) Firefox/47.0 Safari/251.63",
        "Mozilla/5.0 (Macintosh) AppleWebKit/19.73 (KHTML, like Gecko) Edge/15.13128 Safari/173.94",
        "Mozilla/5.0 (Macintosh) AppleWebKit/86.81 (KHTML, like Gecko) Edge/15.17446 Safari/263.28",
        "Mozilla/4.0 (X11) AppleWebKit/30.14 (KHTML, like Gecko) Firefox/48.0 Safari/564.39",
        "Mozilla/5.0 (Macintosh) AppleWebKit/53.35 (KHTML, like Gecko) Firefox/25.0 Safari/130.97",
        "Mozilla/5.0 (Macintosh) AppleWebKit/94.50 (KHTML, like Gecko) Chrome/70.3.3143.434 Safari/334.43",
        ]
    #随机选取请求头
    UserAgent = random.choice(user_agent_list)
    return UserAgent