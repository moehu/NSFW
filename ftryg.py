#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import time
import re
import os
import sys
import html

from requests.adapters import HTTPAdapter


aimurl = 'https://dl.ixxcc.com/NSFW'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
    'Authorization': 'Basic c2hhcmU6cjE4cjE4'
}


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)


def finaldl(header, url, path, s):
    t = 0
    verify = v_status(s, url, header, t)
    resposed = verify
    # print(resposed)
    Is = resposed.find(" directories")
    Is1 = resposed.find(" directory")
    if Is or Is1 != -1:
        drie = re.findall(r'<span class="meta-item"><b>(.*?)</b> directories</span>', resposed)
        drie1 = re.findall(r'<span class="meta-item"><b>(.*?)</b> directory</span>', resposed)
        if len(drie) != 0:
            drie[0] = int(drie[0])
        else:
            drie.append(0)
        if len(drie1) != 0:
            drie1[0] = int(drie1[0])
        else:
            drie1.append(0)
        try:
            mkdir(path + '/' + re.findall(r'<title>(.*?)</title>', resposed)[0])
            path = path + '/' + re.findall(r'<title>(.*?)</title>', resposed)[0]
            files = re.findall(r'<a href="./(.*?)">', resposed)
            namea = re.findall(r'<span class="name">(.*?)</span>', resposed)
            # print(files)
            # print(len(files))
            for k in range(len(files)):
                urlf = url + files[k]
                fold = os.path.exists(path + '/' + namea[k])
                if not fold:
                    print('正在下载：' + namea[k])
                    print('........')
                    t = 0
                    content = dlv_status(s, urlf, header, t)
                    f = open(path + '/' + namea[k], "wb")
                    f.write(content)
                    f.flush()
                    f.close()
                else:
                    print(namea[k] + '文件已下载！')
        except:
            print('下载出错！')


def jge(resposed, url, path, s):
    Is = resposed.find(" directories")
    Is1 = resposed.find(" directory")
    if Is or Is1 != -1:
        drie = re.findall(r'<span class="meta-item"><b>(.*?)</b> directories</span>', resposed)
        drie1 = re.findall(r'<span class="meta-item"><b>(.*?)</b> directory</span>', resposed)
        if len(drie) != 0:
            drie[0] = int(drie[0])
        else:
            drie.append(0)
        if len(drie1) != 0:
            drie1[0] = int(drie1[0])
        else:
            drie1.append(0)
        if int(drie[0]) or int(drie1[0]) > 0:
            mkdir(path + '/' + re.findall(r'<title>(.*?)</title>', resposed)[0])
            path = path + '/' + re.findall(r'<title>(.*?)</title>', resposed)[0]
            file = re.findall(r'<span class="meta-item"><b>(.*?)</b> files</span>', resposed)
            file1 = re.findall(r'<span class="meta-item"><b>(.*?)</b> file</span>', resposed)
            files = re.findall(r'<a href="./(.*?)">', resposed)
            name = re.findall(r'<span class="name">(.*?)</span>', resposed)
            if len(file) != 0:
                file[0] = int(file[0])
            else:
                file.append(0)
            if len(file1) != 0:
                file1[0] = int(file1[0])
            else:
                file1.append(0)
            if int(file[0]) > 0:
                for l in range(int(file[0])):
                    l = -(l + 1)
                    fold = os.path.exists(path + '/' + name[l])
                    if not fold:
                        print('正在下载：' + name[l])
                        print('........')
                        urlf = url + files[l]
                        t = 0
                        content = dlv_status(s, urlf, header, t)
                        # namea = urlf.split('/')[-1]
                        f = open(path + '/' + name[l], "wb")
                        f.write(content)
                        f.flush()
                        f.close()
                    else:
                        print(name[l] + '文件已下载！')
                for k in range(len(files) - int(file[0])):
                    print('正在打开：' + name[k])
                    urld = url + '/' + files[k]
                    t=0
                    verify = v_status(s, urld, header, t)
                    resposed = verify
                    jge(resposed, urld, path, s)
            elif int(file1[0]) > 0:
                for l in range(int(file1[0])):
                    l = -(l + 1)
                    fold = os.path.exists(path + '/' + name[l])
                    if not fold:
                        print('正在下载：' + name[l])
                        print('........')
                        urlf = url + files[l]
                        t = 0
                        content = dlv_status(s, urlf, header, t)
                        # namea = urlf.split('/')[-1]
                        f = open(path + '/' + name[l], "wb")
                        f.write(content)
                        f.flush()
                        f.close()
                    else:
                        print(name[l] + '文件已下载！')
                for k in range(len(files) - int(file1[0])):
                    print('正在打开：' + name[k])
                    urld = url + '/' + files[k]
                    t=0
                    verify = v_status(s, urld, header, t)
                    resposed = verify
                    jge(resposed, urld, path, s)
            else:
                for k in range(len(files)):
                    print('正在打开：' + name[k])
                    urld = url + '/' + files[k]
                    t=0
                    verify = v_status(s, urld, header, t)
                    resposed = verify
                    jge(resposed, urld, path, s)
        else:
            finaldl(header, url, path, s)

def dlv_status(s, url, header, t):
    getfiles = s.get(url, headers=header, timeout=10)
    scode = getfiles.status_code
    if scode != 200:
        time.sleep(30)
        t += 1
        if t > 10:
            print('get失败')
            return getfiles.content
        dlv_status(s, url, header, t)
    else:
        return getfiles.content

def v_status(s, url, header, t):
    get = s.get(url, headers=header, timeout=20)
    scode = get.status_code
    if scode != 200:
        time.sleep(30)
        t += 1
        if t >10:
            print('get失败')
            return 'get失败'
        v_status(s, url, header, t)
    else:
        return html.unescape(get.text)

def run(header, url):
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    t = 0
    verify = v_status(s, url, header, t)
    resposed = verify
    path = re.findall(r'<title>(.*?)</title>', resposed)[0]
    # print(resposed)
    Is = resposed.find(" directories")
    Is1 = resposed.find(" directory")
    try:
        if Is or Is1 != -1:
            drie = re.findall(r'<span class="meta-item"><b>(.*?)</b> directories</span>', resposed)
            drie1 = re.findall(r'<span class="meta-item"><b>(.*?)</b> directory</span>', resposed)
            if len(drie) != 0:
                drie[0] = int(drie[0])
            else:
                drie.append(0)

            if len(drie1) != 0:
                drie1[0] = int(drie1[0])
            else:
                drie1.append(0)

            if int(drie[0]) or int(drie1[0]) > 0:
                mkdir(path)
                links = re.findall(r'<a href="./(.*?)">', resposed)
                name = re.findall(r'<span class="name">(.*?)</span>', resposed)
                file = re.findall(r'<span class="meta-item"><b>(.*?)</b> files</span>', resposed)
                file1 = re.findall(r'<span class="meta-item"><b>(.*?)</b> file</span>', resposed)
                if len(file) != 0:
                    file[0] = int(file[0])
                else:
                    file.append(0)
                if len(file1) != 0:
                    file1[0] = int(file1[0])
                else:
                    file1.append(0)

                for k in range(len(links)):
                    print('正在打开：' + name[k])
                    urld = url + '/' + links[k]
                    getdires = s.get(urld, headers=header, timeout=10)
                    resposed = html.unescape(getdires.text)
                    jge(resposed, urld, path, s)
            else:
                finaldl(header, url, path, s)
    except KeyboardInterrupt:
        print('Keyboard Interrupt!')

        sys.exit()


if __name__ == '__main__':

    frist = time.time()
    try:
        run(header, aimurl)
    except KeyboardInterrupt:
        print('Keyboard Interrupt!')

        sys.exit()

    final = time.time()
    print('运行时间' + str(round(final - frist, 4)) + 's')
