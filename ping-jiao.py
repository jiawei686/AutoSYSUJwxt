#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python verson: 2.7
# @Author: JinJin Lin
# @Email: jinjin.lin@outlook.com
# @License: MIT
# @Date:   2015-12-02 16:16:31
# @Modified By: Eden Chan
# @Last Modified time: 2017-06-09 01:20:22
# All copyright reserved
#

import os
import json
from StringIO import StringIO

import demjson
import getpass

from base import BaseHandler


class PingJiao(BaseHandler):
    """评教模块"""

    def __init__(self, year, term):
        self.year = year
        self.term = term

    def run(self):
        print u'获取课程中...'
        courseList = self.getCourse()
        if len(courseList) == 0:
            print u'没有需要评教的课程'
            return
        print u'共获取到', len(courseList), u'门未评教的课程,开始评教...'
        self.evaluaCourses(courseList)

    def evaluaCourses(self, courseList):
        for course in courseList:
            print u'系统正在评', course['kcmc'], '课程,请等待....'
            self.evaluaCourse(course)
            print '---------------------------------------'
        print u'所有课程评教完成 !'

    def evaluaCourse(self, course):
        questionList = self.getQuesList(course['khtxbh'])
        ansList = self.ansQue(questionList)
        bjid = self.getBJID(course)
        postdata = {
            'header':{
                "code": -100,
                "message": {"title": "", "detail": ""}
            },
            'body':{
                'dataStores':{
                    'itemStore':{
                        'rowSet':{
                            "primary": ansList,
                            "filter":[],
                            "delete":[]
                        },
                        'name':"itemStore",
                        'pageNumber':1,
                        'pageSize':2147483647,
                        'recordCount':14,
                        'rowSetName':"pojo_com.neusoft.education.sysu.pj.xspj.entity.DtjglyEntity"
                    }
                },
                'parameters':{
                    "args": ["ds_itemStore_all", bjid],
                    "responseParam": "bj"
                }
            }
        }
        headers = {
            'Accept': '*/*',
            'ajaxRequest': 'true',
            'render': 'unieap',
            '__clientType': 'unieap',
            'workitemid': 'null',
            'resourceid': 'null',
            'Content-Type': 'multipart/form-data',
            'Referer': 'http://uems.sysu.edu.cn/jwxt/forward.action?path=/sysu/wspj/xspj/jxb_pj',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)',
            'Host': 'uems.sysu.edu.cn',
            'Content-Length': '1410',
            'Connection': 'Keep-Alive',
            'Pragma': 'no-cache'
        }
        req = self.session.post("http://uems.sysu.edu.cn/jwxt/xspjaction/xspjaction.action?method=saveWjxxbyly", headers=headers, json=postdata)
        if req.status_code == 200:
            data = demjson.decode(req.content.decode('utf-8'))
            if data['body']['parameters']['bj'] == 'OK':
                print u'评教', course['kcmc'], u'课程, 成功!'
            else:
                print 'Fail'
        else:
            print 'Fail'

    def ansQue(self, questionList):
        ansList = []
        for que in questionList:
            wtid = que['resourceId']
            jg = self.getJg(wtid)
            ansList.append({'wtid':wtid, 'jg':str(jg), 'gxbh':'', 'resource_id':'', '_t':"1"})
            if que['title'].find(u'：') != -1:
                title = que['title'].encode("utf-8")  
                ansList[len(ansList)-1]['jg'] = unicode(raw_input(title), "utf-8")
        return ansList

    def getQuesList(self, courseID):
        postdata = {
            "header":{
                "code": -100,
                "message": {"title": "", "detail": ""}
            },
            "body":{
                "dataStores":{
                    "wjStroe":{
                        "rowSet":{"primary":[],"filter":[],"delete":[]},
                        "name":"wjStroe",
                        "pageNumber":1,
                        "pageSize":2147483647,
                        "recordCount":0,
                        "rowSetName":"pojo_com.neusoft.education.sysu.pj.xspj.model.WjlyModel",
                        "order":" XSSX ASC "
                    }
                },
                "parameters":{"args": [courseID]}
            }
        }
        headers = {
            'Accept': '*/*',
            'ajaxRequest': 'true',
            'render': 'unieap',
            '__clientType': 'unieap',
            'workitemid': 'null',
            'resourceid': 'null',
            'Content-Type': 'multipart/form-data',
            'Referer': 'http://uems.sysu.edu.cn/jwxt/forward.action?path=/sysu/wspj/xspj/jxb_pj',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)',
            'Host': 'uems.sysu.edu.cn',
            'Content-Length': "325",
            'Connection': 'Keep-Alive',
            'Pragma': 'no-cache' 
        }
        req = self.session.post("http://uems.sysu.edu.cn/jwxt/xspjaction/xspjaction.action?method=getWjxx", headers=headers, json=postdata)
        return self._parseToQueList(req.content.decode("utf-8"))

    def getJg(self, resourceId):
        headers = {
            'Accept': '*/*',
            'ajaxRequest': 'true',
            'render': 'unieap',
            '__clientType': 'unieap',
            'workitemid': 'null',
            'resourceid': 'null',
            'Content-Type': 'multipart/form-data',
            'Referer': 'http://uems.sysu.edu.cn/jwxt/forward.action?path=/sysu/wspj/xspj/jxb_pj',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)',
            'Host': 'uems.sysu.edu.cn',
            'Content-Length': "315",
            'Connection': 'Keep-Alive',
            'Pragma': 'no-cache' 
        }
        postdata = {
            "header":{
                "code": -100,
                "message": {"title": "", "detail": ""}
            },
            "body":{
                "dataStores":{
                    "qzStroe":{
                        "rowSet":{"primary":[],"filter":[],"delete":[]},
                        "name":"wjStroe",
                        "pageNumber":1,
                        "pageSize":2147483647,
                        "recordCount":0,
                        "rowSetName":"pojo_com.neusoft.education.sysu.pj.xspj.model.QzModel",
                        "order":" XSSX ASC "
                    }
                },
                "parameters":{"args": [resourceId]}
            }
        }
        req = self.session.post("http://uems.sysu.edu.cn/jwxt/xspjaction/xspjaction.action?method=getQzlist", headers=headers, json=postdata)
        reqJson = demjson.decode(req.text)
        try:
            jg = reqJson['body']['dataStores']['qzStroe']['rowSet']['primary'][0]['resourceid']
        except:
            jg = ''
        return jg

    def getCourse(self):
        postdata = {
            "header": {
                "code": -100,
                "message": {"title": "", "detail": ""}
            },
            "body": {
                "dataStores":{
                    "pj1Stroe":{
                        "rowSet":{
                            "primary":[],
                            "filter":[],
                            "delete":[]
                        },
                        "name":"pj1Stroe",
                        "pageNumber":1,
                        "pageSize":50,
                        "recordCount":0,
                        "rowSetName":"pojo_com.neusoft.education.sysu.pj.xspj.model.PjsyfwModel"}
                },
                "parameters":{"args": []}
            }
        }
        headers = {
            "Accept": "*/*",
            "ajaxRequest": "true",
            "render": "unieap",
            "__clientType": "unieap",
            "workitemid": "null",
            "resourceid": "null",
            "Content-Type": "multipart/form-data",
            "Referer": "http://uems.sysu.edu.cn/jwxt/forward.action?path=/sysu/wspj/xspj/xspj_list&xnd="+self.year+"&xq="+self.term,
            "Accept-Language": "en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)",
            "Host": "uems.sysu.edu.cn", "Content-Length": "290",
            "Connection": "Keep-Alive",
            "Pragma": "no-cache",
        }
        req = self.session.post("http://uems.sysu.edu.cn/jwxt/xspjaction/xspjaction.action?method=getXspjlist", headers=headers, json=postdata)
        return self._parseToCourseList(req.content.decode("utf-8"))

    def getBJID(self, course):
        postdata = {
            'header':{
                "code": -100, 
                "message": {"title": "", "detail": ""}
            },
            'body':{
                'dataStores':{},
                'parameters':{
                    "args": [course['jsbh'], course['kch'], course['khlx'], course['jxbh'], course['khtxbh'], course['pjlx']], 
                    "responseParam": "bjid"
                }
            }
        }
        headers = { 
            'Accept': '*/*',
            'ajaxRequest': 'true',
            'render': 'unieap',
            '__clientType': 'unieap',
            'workitemid': 'null',
            'resourceid': 'null',
            'Content-Type': 'multipart/form-data',
            'Referer': 'http://uems.sysu.edu.cn/jwxt/forward.action?path=/sysu/wspj/xspj/jxb_pj',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)',
            'Host': 'uems.sysu.edu.cn',
            'Content-Length': '196',
            'Connection': 'Keep-Alive',
            'Pragma': 'no-cache'
        }
        req = self.session.post("http://uems.sysu.edu.cn/jwxt/xspjaction/xspjaction.action?method=getPjsyfwbzj", headers=headers, json=postdata)
        data = demjson.decode(req.content.decode('utf-8'))
        return data['body']['parameters']['bjid']

    def _parseToCourseList(self, reqJson):
        reqJson = demjson.decode(reqJson)
        courseList = reqJson['body']['dataStores']['pj1Stroe']['rowSet']['primary']
        return courseList

    def _parseToQueList(self, reqJson):
        reqJson = demjson.decode(reqJson)
        questionList = reqJson['body']['dataStores']['wjStroe']['rowSet']['primary']
        return questionList

if __name__ == "__main__":
    debug = True
    os.system("cls")
    print '============================================================================'
    print '                                                                            '
    print '                Welcome, SYSU OneKey Teacher Evaluation  V1.1               '
    print '                      '+u'中山大学一键评教，默认评最高分'
    print '                                                                            '
    print '                                                 Design By: JinJin Lin      '
    print '                                                 jinjin.lin@outlook.com     '
    print '                                                Github.com/linjinjin123     '
    print '                                                                            '
    print '                                                 Modified By: Eden Chan     '
    print '                                                 xiaomi388@gmail.com     '
    print '                                                Github.com/xiaomi388     ' 
    print '                                                                            '
    print '                                                               2017.6.10    '
    print '                                                                            '
    print '============================================================================'
    if debug == True:
        year = '2016-2017'
        term = '2'
        username = ''
        password = ''
    else:
        year = raw_input('Please input year(The format is 2016-2017)\n')
        term = raw_input('Please input the number of semester: \n1.first \n2.second \n3.third\n')
        if pingjiao.have_login == False:
            username = raw_input('Please input your NetID:')
            password = getpass.getpass('Please input your Password:')    
    pingjiao = PingJiao(year, term)
    pingjiao.login(username, password)
    pingjiao.run()
    print u'程序运行结束，是否成功请登陆教务系统查看'
    raw_input(u'Enter any key to quit')

