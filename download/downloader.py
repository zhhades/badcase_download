from concurrent.futures import wait, ThreadPoolExecutor

import requests


class Downloader():
    def __init__(self, url, num, name):
        self.url = url
        self.num = num
        self.name = name
        r = requests.head(self.url)
        self.size = int(r.headers['Content-Length'])

    def down(self, start, end):
        headers = {'Range': 'bytes={}-{}'.format(start, end)}
        r = requests.get(self.url, headers=headers, stream=True)
        # 写入文件对应位置
        with open(self.name, "rb+") as f:
            f.seek(start)
            f.write(r.content)

    def run(self):
        f = open(self.name, "wb")
        f.truncate(self.size)
        f.close()
        futures = []
        part = self.size // self.num
        pool = ThreadPoolExecutor(max_workers=self.num)
        for i in range(self.num):
            start = part * i
            if i == self.num - 1:
                end = self.size
            else:
                end = start + part - 1
            # 扔进线程池
            futures.append(pool.submit(self.down, start, end))
        wait(futures)


if __name__ == '__main__':
    down = Downloader("http://10.199.1.210:8080/v5/resources/data?uri=weed://3684,0fd7ff79e4e4a4_meta&downloadFilename=200811101117.tar.gz",
                      int(4), "test.tar.gz")
    down.run()
