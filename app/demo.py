# -*- codeing=utf-8-*-
# @Time: 2021/8/29 20:48
# @AUthor: BaBa
# @File: demo.py
# @software: PyCharm
import bs4
import re
import requests
import execjs


def main2(id):

    import warnings
    warnings.filterwarnings("ignore")
    url = "https://www1.szu.edu.cn/board/view.asp?id=" + str(id)
    return dataFilter(url)


def dataFilter(url):
    html = askURL(url)
    soup = bs4.BeautifulSoup(html, "html.parser")

    parasStr = ""
    paras_parent = soup.find_all(attrs={'valign':'top'})[3]
    paras = paras_parent.table
    for para in paras:
        parasStr += str(para)

    return parasStr


def askURL(url):

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}
    session1 = requests.Session()
    session1.get("https://www1.szu.edu.cn/", headers=headers,verify=False)

    # 获取加密的password 开始
    crypt = session1.get("https://authserver.szu.edu.cn/authserver/custom/js/encrypt.js", headers=headers,verify=False).text
    encrypt = execjs.compile(crypt)  # 获取js加密代码
    # print(encrypt)
    res = session1.get("https://authserver.szu.edu.cn/authserver/login", headers=headers,verify=False)  # 请求登录界面

    bs = bs4.BeautifulSoup(res.content, "html.parser")
    bs = bs.find_all('input', {'type': "hidden"})  # 寻找登录界面中需要的数据
    dist = {}
    for i in bs:
        try:
            dist[re.search('(?<=name=").*?(?=")', str(i)).group()] = re.search('(?<=value=").*?(?=")', str(i)).group()
        except:
            dist[re.search('(?<=id=").*?(?=")', str(i)).group()] = re.search('(?<=value=").*?(?=")', str(i)).group()

    username = '334834'
    password = 'xiao1999'
    enPassword = encrypt.call("encryptAES", password, dist["pwdDefaultEncryptSalt"])  # 利用js代码加密
    # print(enPassword)
    # 获取加密过的password 结束

    # 登录时需要POST的数据
    data = {
        "username": username,
        "password": enPassword,
        "lt": dist["lt"],
        "dllt": dist["dllt"],
        "execution": dist["execution"],
        "_eventId": dist["_eventId"],
        "rmShown": dist["rmShown"]
    }

    login_url = "https://authserver.szu.edu.cn/authserver/login?service=http%3A%2F%2Fwww1%2Eszu%2Eedu%2Ecn%2Fmanage%2Fcaslogin%2Easp%3Frurl%3D%2F"
    session1.post(login_url, headers=headers, data=data,verify=False)

    # askRes2 = session1.get("https://www1.szu.edu.cn/board/infolist.asp", headers=headers, verify=False)

    askRes = session1.get(url, headers=headers,verify=False)
    askRes.encoding = 'gbk'
    # print(askRes.text)
    return askRes.text
if __name__=="__main__":

    print(main2(456180))
