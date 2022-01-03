#! /url/bin/python
# -*- coding: UTF-8 -*-


try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    from requests_ntlm import HttpNtlmAuth
    import simplejson
    import jsonschema
    import os
    import json
    from urllib import urlencode
    import robot
    from robot.api import logger
    from robot.libraries.BuiltIn import BuiltIn
    from robot.utils.asserts import assert_true, assert_equal
except ImportError:
    print u"关键字库缺少必要的python依赖库，请安装："
    print u"requests、simplejson、requests_ntlm、jsonschema"
    raise SystemExit


class RestKeywords:
    def __init__(self):
        self.schema_location = None
        self._cache = robot.utils.ConnectionCache(u'未创建Sessions')
        self.builtin = BuiltIn()

    def _utf8_urlencode(self, data):
        if isinstance(data, unicode):
            return data.encode('utf-8')

        if not isinstance(data, dict):
            return data

        utf8_data = {}
        for k, v in data.iteritems():
            utf8_data[k] = unicode(v).encode('utf-8')

        return urlencode(utf8_data)

    def _create_session(self, alias, url, headers, cookies,
                        auth, timeout, proxies, verify):
        """ Create Session: 创建一个连接server的HTTP会话

        `url` 服务器基本的URL地址

        `alias` Robot Framework 对当前创建的HTTP会话指定的别名

        `headers` 默认的headers字典

        `auth` 对于HTTP基本身份验证词典的用户名和密码

        `timeout` 连接超时

        `proxies` 代理服务器URL

        `verify` 如果请求验证证书，该值设置为True
        """

        self.builtin.log(u'创建Session：%s' % alias, 'DEBUG')
        session = requests.Session()
        session.headers.update(headers)
        session.auth = auth if auth else session.auth
        session.proxies = proxies if proxies else session.proxies

        session.verify = self.builtin.convert_to_boolean(verify)

        # 通过传递进入说请求
        # cant pass these into the Session anymore
        self.timeout = timeout
        self.cookies = cookies
        self.verify = verify

        # cant use hooks:(
        session.url = url

        self._cache.register(session, alias=alias)

        return session

    def create_session(self, alias, url, headers={}, cookies=None,
                       auth=None, timeout=None, proxies=None, verify=False):
        """ Create Session: 创建一个连接server的HTTP会话

        `url` 服务器基本的URL地址

        `alias` Robot Framework 对当前创建的HTTP会话指定的别名

        `headers` 默认的headers字典

        `auth` 对于HTTP基本身份验证词典的['DOMAIN', '用户名', '密码']

        `timeout` 连接超时

        `proxies` 代理服务器URL

        `verify` 如果请求验证证书，该值设置为True
        """

        auth = requests.auth.HTTPBasicAuth(*auth) if auth else None

        return self._create_session(alias, url, headers, cookies, auth,
                                    timeout, proxies, verify)

    def create_ntln_session(self, alias, url, headers={}, cookies=None,
                       auth=None, timeout=None, proxies=None, verify=False):
        """ Create Session: 创建一个连接server的HTTP会话

        `url` 服务器基本的URL地址

        `alias` Robot Framework 对当前创建的HTTP会话指定的别名

        `headers` 默认的headers字典

        `auth` 对于HTTP基本身份验证词典的['DOMAIN', '用户名', '密码']

        `timeout` 连接超时

        `proxies` 代理服务器URL

        `verify` 如果请求验证证书，该值设置为True
        """
        if not HttpNtlmAuth:
            raise AssertionError(u'未加载Reuqest HTLM模块')
        elif len(auth) != 3:
            raise AssertionError(u'验证参数数量不正确 '
                                 u'- 预期3个参数, 实际{}'.format(len(auth)))
        else:
            ntlm_auth = HttpNtlmAuth('{}\\{}'.format(auth[0], auth[1]), auth[2])

            return self._create_session(alias, url, headers, cookies,
                                        ntlm_auth, timeout, proxies, verify)

    def delete_all_sessions(self):
        """删除所有Session对象"""

        self._cache.empty_cache()

    def to_json(self, content, pretty_print=False):
        """将字符串转换为一个JSON对象或字典.
        `content`字符串的内容转换成JSON
        `pretty_print`如果被定义，将content输出打印JSON格式
        """
        if pretty_print:
            json_ = self._json_pretty_print(content)
        else:
            json_ = simplejson.loads(content)
        return json_

    def get_request(self, alias, uri, headers=None, params={}, allow_redirects=None):
        """ 使用指定别名中找到的会话对象发送GET请求

        `uri` 向该uri发送GET 请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        """
        # 根据alias获取Session对象
        session = self._cache.switch(alias)
        # 对参数进行encode编码转换
        params = self._utf8_urlencode(params)
        # 判断是否允许重定向
        redir = True if allow_redirects is None else allow_redirects
        response = self._get_request(session, uri, headers, params, redir)

        return response

    def get(self, alias, uri, headers=None, params={}, allow_redirects=None):
        """ * * *   警告 - 建议使用get request   * * *
        使用指定别名中找到的会话对象发送GET请求

        `uri` 向该uri发送GET 请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        """
        print u"警告强烈反对当前使用GET方法提交请求"
        session = self._cache.switch(alias)
        params = self._utf8_urlencode(params)
        redir = True if allow_redirects is None else allow_redirects
        response = self._get_request(session, uri, headers, params, redir)

        return response

    def post_request(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None):
        """ 使用指定别名中找到的会话对象发送POST请求

        `uri` 向该uri发送POST 请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        `data` 将原Body内容POST的数据或二进制数据转换为键值字典，并以urlencoded编码形式发送

        `files` 包含数据文件的文件名的字典才能POST到服务器

        """
        # 根据alias获取Session对象
        session = self._cache.switch(alias)
        # 对data进行encode编码转换
        data = self._utf8_urlencode(data)
        # 判断是否允许重定向
        redir = True if allow_redirects is None else allow_redirects
        response = self._post_request(session, uri, data, headers, files, redir)

        return response

    def post(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None):
        """ * * *   警告 - 建议使用post request   * * *
        使用指定别名中找到的会话对象发送POST请求

        `uri` 向该uri发送POST 请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        `data` 将原Body内容POST的数据或二进制数据转换为键值字典，并以urlencoded编码形式发送

        `files` 包含数据文件的文件名的字典才能POST到服务器

        """
        print u"警告强烈反对当前使用POST方法提交请求"
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._post_request(session, uri, data, headers, files, redir)

        return response

    def patch_request(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None):
        """ 使用指定别名中找到的会话对象发送PATCH请求

        `uri` 向该uri发送PATCH请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        `data` 将原Body内容PATCH的数据或二进制数据转换为键值字典，并以urlencoded编码形式发送

        `files` 包含数据文件的文件名的字典才能PATCH到服务器

        """
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._patch_request(session, uri, data, headers, files, redir)
        return response

    def patch(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None):
        """ * * *   警告 - 建议使用patch request   * * *
        使用指定别名中找到的会话对象发送PATCH请求

        `uri` 向该uri发送PATCH请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        `data` 将原Body内容PATCH的数据或二进制数据转换为键值字典，并以urlencoded编码形式发送

        `files` 包含数据文件的文件名的字典才能PATCH到服务器

        """
        print u"警告强烈反对当前使用PATCH方法提交请求"
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._patch_request(session, uri, data, headers, files, redir)

        return response

    def put_request(self, alias, uri, data=None, headers=None, allow_redirects=None):
        """使用指定别名中找到的会话对象发送PUT请求

        `uri` 向该uri发送PUT请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        `data` 将原Body内容PUT的数据或二进制数据转换为键值字典，并以urlencoded编码形式发送

        """
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._put_request(session, uri, data, headers, redir)

        return response

    def put(self, alias, uri, data=None, headers=None, allow_redirects=None):
        """* * *   警告 - 建议使用put request   * * *
        使用指定别名中找到的会话对象发送PUT请求

        `uri` 向该uri发送PUT请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        `data` 将原Body内容PUT的数据或二进制数据转换为键值字典，并以urlencoded编码形式发送

        """
        print u"警告强烈反对当前使用put方法提交请求"
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._put_request(session, uri, data, headers, redir)

        return response

    def delete_request(self, alias, uri, data=(), headers=None, allow_redirects=None):
        """ 使用指定别名中找到的会话对象发送DELETE请求

        `uri` 向该uri发送DELETE请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        `data` 将原Body内容DELETE的数据或二进制数据转换为键值字典，并以urlencoded编码形式发送

        """
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._delete_request(session, uri, data, headers, redir)

        return response

    def delete(self, alias, uri, data=(), headers=None, allow_redirects=None):
        """* * *   警告 - 建议使用delete request   * * *
        使用指定别名中找到的会话对象发送DELETE请求

        `uri` 向该uri发送DELETE请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        `data` 将原Body内容DELETE的数据或二进制数据转换为键值字典，并以urlencoded编码形式发送

        """
        print u"警告强烈反对当前使用delete方法提交请求"
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._delete_request(session, uri, data, headers, redir)

        return response

    def head_request(self, alias, uri, headers=None, allow_redirects=None):
        """ 使用指定别名中找到的会话对象发送HEAD请求

        `uri` 向该uri发送HEAD请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        """
        session = self._cache.switch(alias)
        redir = False if allow_redirects is None else allow_redirects
        response = self._head_request(session, uri, headers, redir)

        return response

    def head(self, alias, uri, headers=None, allow_redirects=None):
        """* * *   警告 - 建议使用head request   * * *
        使用指定别名中找到的会话对象发送HEAD请求

        `uri` 向该uri发送HEAD请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        """
        print u"警告强烈反对当前使用head方法提交请求"
        session = self._cache.switch(alias)
        redir = False if allow_redirects is None else allow_redirects
        response = self._head_request(session, uri, headers, redir)

        return response

    def options_request(self, alias, uri, headers=None, allow_redirects=None):
        """ 使用指定别名中找到的会话对象发送OPTIONS请求

        `uri` 向该uri发送OPTIONS请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        """
        session = self._cache.switch(alias)
        redir = True if allow_redirects is None else allow_redirects
        response = self._options_request(session, uri, headers, redir)

        return response

    def options(self, alias, uri, headers=None, allow_redirects=None):
        """* * *   警告 - 建议使用options request   * * *
        使用指定别名中找到的会话对象发送OPTIONS请求

        `uri` 向该uri发送OPTIONS请求

        `alias` 将用于识别在高速缓存中的Session 对象

        `headers` 请求以字典格式的报头

        """
        print u"警告强烈反对当前使用options方法提交请求"
        session = self._cache.switch(alias)
        redir = True if allow_redirects is None else allow_redirects
        response = self._options_request(session, uri, headers, redir)

        return response

    def decode(self, coustom_str):
        """
        将字符串转换成 utf-8编码。
        """
        #return coustom_str.decode("utf-8")
        #return coustom_str.encode('ascii', 'xmlcharrefreplace')
        return coustom_str.decode("utf-8")

    def convert_to_json(self, content):
        """
        用来在robot 中将字典转换成json字符串,并输出打印JSON格式。（针对 POST请求的处理）
        """
        return simplejson.dumps(content, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

    def set_jsonschema_path(self, schema_location=None):
        self.schema_location = schema_location
        if not self.schema_location.endswith('/'):
            self.schema_location = '{}'.format(self.schema_location.encode("utf-8"))

        print u"json模板目录设置成功！"

    def validate_json(self, schema_filename, sample):
        """针对给定的模式验证服务端响应的JSON结果.(必须先使用Set Jsonschema Path关键字设定 json模板保存目录)

        schema_filename：json模板文件名

        sample： 待验证的示例json对象（记住：是json对象，不是json字符串。这里其实是服务端的响应）
        """
        connect_path = '{}\{}'.format(self.schema_location, schema_filename).decode("utf-8")
        json_content = open(connect_path).read()
        schema = json.loads(json_content)
        resolver = jsonschema.RefResolver('file:/{}'.format(self.schema_location), schema)

        try:
            jsonschema.validate(sample, schema, resolver=resolver)
            print u"【%s】:接口返回值的基本结果验证成功！" % schema_filename

        except jsonschema.ValidationError as e:
            print u"【%s】:接口返回值的基本结果验证失败！原因：【json模板文件中定义 %s 的类型为 %s ,而实际接口返回值为 %s 】" % (schema_filename, e.relative_schema_path,
                                                                              e.validator_value, e.instance)
            raise jsonschema.ValidationError('Validation error for schema {}: {}'.format(schema_filename, e.message))

    def validate_json_by_condition(self, schema_filename, sample, *output):
        """针对给定的模式验证服务端响应的JSON结果.(必须先使用Set Jsonschema Path关键字设定 json模板保存目录)

        schema_filename：json模板文件名 （必须为list列表）

        sample： 待验证的示例json对象（记住：是json对象，不是json字符串。这里其实是服务端的响应）

        output: 提供的待校验的输入参数的真假值 (必须为bool类型)。
        """
        assert_true(len(output) <= 3, u"Sorry!暂时最多只支持【三个】输入参数的验证！")
        assert_true(type(schema_filename) == list, u"第一个参数必须为列表list类型！")

        for par in output:
            assert_true(type(par) == bool, u"提供的待验证的输入参数必须为bool类型！")

        if len(output) == 0:
            """
            真
            """
            print u"【真】"
            self.validate_json(schema_filename[0], sample)

        elif len(output) == 1:
            """真
               假
            """
            if output[0]:
                print u"【真】"
                self.validate_json(schema_filename[0], sample)
            else:
                print u"【假】"
                self.validate_json(schema_filename[1], sample)

        elif len(output) == 2:
            """真-真
               真-假
               假-真
               假-假
            """
            if output[0] and output[1]:
                print u"【真--真】"
                self.validate_json(schema_filename[0], sample)
            elif output[0] and not output[1]:
                print u"【真--假】"
                self.validate_json(schema_filename[1], sample)
            elif not output[0] and output[1]:
                print u"【假--真】"
                self.validate_json(schema_filename[2], sample)
            elif not output[0] and not output[1]:
                print u"【假--假】"
                self.validate_json(schema_filename[3], sample)

        elif len(output) == 3:
            """ 真	真	真
                真	假	真
                真	真	假
                真	假	假
                假	真	真
                假	假	真
                假	真	假
                假	假	假
            """
            if output[0] and output[1] and output[2]:
                print u"【真--真--真】"
                self.validate_json(schema_filename[0], sample)
            elif output[0] and not output[1] and output[2]:
                print u"【真--假--真】"
                self.validate_json(schema_filename[1], sample)
            elif output[0] and output[1] and not output[2]:
                print u"【真--真--假】"
                self.validate_json(schema_filename[2], sample)
            elif output[0] and not output[1] and not output[2]:
                print u"【真--假--假】"
                self.validate_json(schema_filename[3], sample)
            elif not output[0] and output[1] and output[2]:
                print u"【假--真--真】"
                self.validate_json(schema_filename[4], sample)
            elif not output[0] and not output[1] and output[2]:
                print u"【假--假--真】"
                self.validate_json(schema_filename[5], sample)
            elif not output[0] and output[1] and not output[2]:
                print u"【假--真--假】"
                self.validate_json(schema_filename[6], sample)
            elif not output[0] and not output[1] and not output[2]:
                print u"【假--假--假】"
                self.validate_json(schema_filename[7], sample)
        else:
            return u"Sorry!暂时最多只支持三个输入参数的验证！提供的参数有误，请检查... ... 提示：responsedata：表示实际结果 results：表示预期结果！"

    def _get_request(self, session, uri, headers, params, allow_redirects):
        resp = session.get(self._get_url(session, uri),
                           headers=headers,
                           params=params,
                           cookies=self.cookies, timeout=self.timeout,
                           allow_redirects=allow_redirects)
        # 存储最后响应对象
        session.last_resp = resp
        #self.builtin.log("GET 响应: %s DEBUG" % resp.content.decode("utf-8"))
        print u"GET 响应:%s DEBUG" % resp.content.decode("utf-8")
        return resp

    def _post_request(self, session, uri, data, headers, files, allow_redirects):
        resp = session.post(self._get_url(session, uri),
                            data=data, headers=headers,
                            files=files,
                            cookies=self.cookies, timeout=self.timeout,
                            allow_redirects=allow_redirects)

        # 存储最后响应对象
        session.last_resp = resp
        #self.builtin.log("POST 响应: %s DEBUG" % resp.content)
        print u"POST 响应: %s DEBUG" % resp.content.decode("utf-8")
        return resp

    def _patch_request(self, session, uri, data, headers, files, allow_redirects):
        resp = session.patch(self._get_url(session, uri),
                             data=data, headers=headers,
                             files=files,
                             cookies=self.cookies, timeout=self.timeout,
                             allow_redirects=allow_redirects)
        # 存储最后响应对象
        session.last_resp = resp
        #self.builtin.log("PATCH 响应: %s DEBUG" % resp.content)
        print u"PATCH 响应: %s DEBUG" % resp.content.decode("utf-8")
        return resp

    def _put_request(self, session, uri, data, headers, allow_redirects):
        resp = session.put(self._get_url(session, uri),
                           data=data, headers=headers,
                           cookies=self.cookies, timeout=self.timeout,
                           allow_redirects=allow_redirects)

        #self.builtin.log("PUT 响应: %s DEBUG" % resp.content)
        print u"PUT 响应: %s DEBUG" % resp.content.decode("utf-8")
        # 存储最后响应对象
        session.last_resp =resp
        return resp

    def _delete_request(self, session, uri, data, headers, allow_redirects):
        resp = session.delete(self._get_url(session, uri), data=data,
                              headers=headers, cookies=self.cookies,
                              timeout=self.timeout,
                              allow_redirects=allow_redirects)

        # 存储最后响应对象
        session.last_resp = resp
        #self.builtin.log("DELETE 响应: %s DEBUG" % resp.content)
        print u"DELETE 响应: %s DEBUG" % resp.content.decode("utf-8")
        return resp

    def _head_request(self, session, uri, headers, allow_redirects):
        resp = session.head(self._get_url(session, uri), headers=headers,
                            cookies=self.cookies, timeout=self.timeout,
                            allow_redirects=allow_redirects)

        # 存储最后响应对象
        session.last_resp = resp
        #self.builtin.log("HEAD 响应: %s DEBUG" % resp.content)
        print u"HEAD 响应: %s DEBUG" % resp.content.decode("utf-8")
        return resp

    def _options_request(self, session, uri, headers, allow_redirects):
        resp = session.head(self._get_url(session, uri), headers=headers,
                            cookies=self.cookies, timeout=self.timeout,
                            allow_redirects=allow_redirects)

        # 存储最后响应对象
        session.last_resp = resp
        #self.builtin.log("OPTIONS 响应: %s DEBUG" % resp.content)
        print u"OPTIONS 响应: %s DEBUG" % resp.content.decode("utf-8")
        return resp

    def _get_url(self, session, uri):
        """根据Helper 模块获取完整URL"""
        url = session.url
        if uri:
            slash = '' if uri.startswith('/') else '/'
            url = "%s%s%s" % (session.url, slash, uri)

        return url

    def _json_pretty_print(self, content):
        """ 转换为JSON 对象
        'content' 将content转换为JSON object
        """
        temp = simplejson.loads(content)
        return simplejson.dumps(temp, sort_keys=True, indent=4, separators=(',', ': '))