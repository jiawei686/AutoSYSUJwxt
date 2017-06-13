#coding:utf-8
import requests
from lxml import etree

class BaseHandler(object):
    """用于登陆教务系统，并提供一个Session
    所有在教务系统中实现子功能类类都应该继承这个类
    """

    session = requests.Session()
    have_login = False

    def login(self, username, password):
        self.username = username
        self.password = password
        url = 'https://cas.sysu.edu.cn/cas/login?service=http://uems.sysu.edu.cn/jwxt/casLogin'
        open_response = self.session.get(url)
        html = etree.HTML(open_response.text)
        data = {}
        for each in html.xpath('//input'):
            data[each.get('name')] = each.get('value')
        data['username'] = self.username
        data['password'] = self.password
        login_response = self.session.post(url=url, data=data)
        if login_response.text.find(u'面正在加载, 请稍候') != -1:
            print 'login success.'
        else:
            print 'login failure.'

