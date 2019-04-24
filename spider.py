import aiohttp
import asyncio
import json
from lxml import etree


# 建立发送请求中心函数
loop=asyncio.get_event_loop()  #这个是循环队列
async def main(url, method, params=None, data=None, json=None, headers=None, cookies=None, proxy=None, timeout=None):
    async with aiohttp.ClientSession() as s:
        async with s.request(url=url,method=method,params=params,data=data,json=json,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout) as resp:
            reque.append(Zjresponse(await resp.read(),resp))
            # reque.append(resp)

#为了减少代码冗余，都用request发送
def requests(urls,method,params=None,data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None):
    '''
    调用main实现异步发送
    :param urls: 可能是一个，可能是多个，为了减少代码冗余
    :return: 返回main添加过的中reque
    '''
    global reque
    reque=[]
    tasks=[]
    for url in urls:
        #调用main 并将多个main执行放在一个列表里执行
        tasks.append(asyncio.ensure_future(main(url=url, method=method, params=params, data=data, json=json, headers=headers, cookies=cookies, proxy=proxy, timeout=timeout)))
    #Run 多个url 用下边这样
    loop.run_until_complete(asyncio.wait(tasks))
    return reque


#发送一个get
def get(url,data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None):
    return requests(urls=[url],method='GET',data=data,json=json,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout)[0]

#发送多个Get
def gets(urls,data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None):
    return requests(urls=urls,method='GET',data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None)

#发送一个POST
def post(url,data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None):
    return requests(urls=[url],method='POST',data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None)[0]

#格式化header工具
def format_headers(str):
    head={}
    for s in str.split('\n'):  #切割成一行一个元素的列表
        h2 = s.strip()   #去空格
        if h2:
            headerList = h2.split(':')
            if len(headerList)==1:
                head[headerList[0]]=''
            elif len(headerList)==2:
                head[headerList[0]]=headerList[1]
            elif len(headerList)==3:
                head[headerList[0]]=headerList[1]+headerList[2]
    return head

#格式化cookie工具
def formatt_cookie(str):
    cook={}
    for c in str.split(';'):
        c1=c.strip()
        if c1:
            cookieList=c1.split('=')
            cook[cookieList[0]]=cookieList[1]
    return cook


#根据json解析出你想要的key
def getvalues_from_json(json,relist,key):
    #是字典
    v=''
    if isinstance(json,dict):
        if key in json.keys():  #第一层的jsonkey是否有目标key
            v=json.get(key) #两种取法
            # v=json[key]
        else:
            for k in json.values():
                getvalues_from_json(k,relist,key)

    elif isinstance(json, list):
        for l in json:
            getvalues_from_json(l,relist,key)

    if v:
        relist.append(v)

    return relist #就像类似递归的，不结束会一直调用

class Zjresponse(object):
    def __init__(self,content,res):
        self.content=content   #二进制的响应 用aiohttp读出来的响应就是二进制
        self.res=res

    #     获取的节点就一个
    def get_one_node(self,str):
        try:
            # html = etree.HTML(self.content)
            return etree.HTML(self.content).xpath(str)[0]
        except:
            return None
    # 获取的节点有多个
    def get_more_node(self,str):
        # html=etree.HTML(self.content)
        return etree.HTML(self.content).xpath(str)

    # 从json中获取一个value
    def get_one_value(self,key):
        return getvalues_from_json(json.loads(self.text()),[],key)[0]
    #从json中获取多个value
    def get_more_values(self,key):
        return getvalues_from_json(json.loads(self.text()),[],key)

    # 二进制直接存的那种
    def save_content(self,path):
        with open(path,'wb') as f:
            f.write(self.content)

    # 给二进制进行编码，返回想要格式的文本
    def text(self,encoding=None):  #可以优化，传入编码格式可以生效
        try:
            return self.content.decode('utf-8')
        except:
            return self.content.decode('gbk')

    @property
    def byte(self):
        return self.content


    @property
    def cookies(self):
        return self.res.cookies

    @property
    def headers(self):
        return self.res.headers

    @property
    def url(self):
        return self.res.url














