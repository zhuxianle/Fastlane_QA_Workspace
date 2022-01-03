#!/usr/bin/env python
#coding=utf-8

import time
from selenium import webdriver


class _CustomKeywords(object):
    def custom_webdriver_browser(self, url, *args):
        """自定义的一个webdriver操作浏览器关键字，该关键字只针对在特殊情况下无法操作页面元素而使用(不具有通用性，也不够灵活)。

        """
        print url
        print args
        driver = webdriver.Firefox()
        driver.get("https://192.168.1.207:6003")
        #assert "Python" in driver.title
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_class_name("yy-login-infor-right").click()
        driver.maximize_window()
        driver.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-left"]/li[13]').click()
        time.sleep(3)
        driver.find_element_by_xpath('//div[@class="aside"]/ul/li/a').click()
        driver.switch_to.frame("iframe")
        driver.find_element_by_id("liveRoomTitle").send_keys("test")
        driver.find_element_by_id("searchBtn").click()
        time.sleep(2)
        print "yes"
        driver.find_element_by_xpath('//a[text()="下架原因"]').click()
        print "no"
        driver.close()
        driver.quit()

if __name__ == "__main__":
    app = _CustomKeywords()
    app.custom_webdriver_browser("https://192.168.1.207:6003")