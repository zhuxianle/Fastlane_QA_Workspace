# -*- coding: utf-8 -*-

import os
from appium.webdriver.common.touch_action import TouchAction
from AppiumLibrary.locators import ElementFinder
from keywordgroup import KeywordGroup


class _TouchKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, element lookups
    def zoom(self, locator, percent="200%", steps=1):
        """
        Zooms in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.zoom(element=element, percent=percent, steps=steps)

    def pinch(self, locator, percent="200%", steps=1):
        """
        Pinch in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.pinch(element=element, percent=percent, steps=steps)

    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        Swipe from one point to another point, for an optional duration.
        """
        driver = self._current_application()
        driver.swipe(start_x, start_y, end_x, end_y, duration)

    # new add  ----------------------------------------------------------------
    def flick(self, start_x, start_y, end_x, end_y):
        """
        按住A点后快速滑动至B点。注意与 swipe 关键字的区别。

        参数:
         - start_x:  开始点的X坐标
         - start_y:  开始点的Y坐标
         - end_x:  结束点的X坐标
         - end_y:  结束点的Y坐标

        例如:
            | Flick | ${start_x} | ${start_y} | ${end_x} | ${end_y} |
        """
        driver = self._current_application()
        driver.flick(start_x, start_y, end_x, end_y)

    def execute_javascript(self, script, *args):
        """
        在当前窗口/框架中同步执行 javascript 代码。

        例如：执行滚动条的js代码

        IE浏览器下：document.documentElement.scrollTop

        Chrome浏览器下：document.body.scrollTop
        """
        driver = self._current_application()
        driver.execute_script(script)

    def execute_javascript_by_argv(self, code, *argv):
        """在原来的基础上新增个传参的参数"""
        js = self._get_javascript_to_execute(''.join(code))
        return self._current_application().execute_script(js, *argv)
    # new add  ----------------------------------------------------------------

    def scroll(self, start_locator, end_locator):
        """
        Scrolls from one element to another
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        el1 = self._element_find(start_locator, True, True)
        el2 = self._element_find(end_locator, True, True)
        driver = self._current_application()
        driver.scroll(el1, el2)
        
    def scroll_to(self, locator):
        """Scrolls to element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scrollTo", {"element": element.id})
        
    def long_press(self, locator):
        """ Long press the element """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        long_press = TouchAction(driver).long_press(element)
        long_press.perform()

    def tap(self, locator):
        """ Tap on element """
        driver = self._current_application()
        el = self._element_find(locator, True, True)
        action = TouchAction(driver)
        action.tap(el).perform()
        
    def click_a_point(self, x=0, y=0):
        """ 点击坐标点(带松开操作)"""
        self._info("Clicking on a point (%s,%s)." % (x,y))
        driver = self._current_application()
        action = TouchAction(driver)
        try:
            action.press(x=float(x), y=float(y)).release().perform()
        except:
            assert False, "Can't click on a point at (%s,%s)" % (x,y)

    # Private

    def _get_javascript_to_execute(self, code):
        codepath = code.replace('/', os.sep)
        if not (os.path.isabs(codepath) and os.path.isfile(codepath)):
            self._info("Executing Asynchronous JavaScript:\n%s" % code)
            return code
        self._html('Reading JavaScript from file <a href="file://%s">%s</a>.'
                   % (codepath.replace(os.sep, '/'), codepath))
        codefile = open(codepath)
        try:
            self._info("Executing Asynchronous JavaScript from js file ... ...\n")
            return codefile.read().strip()
        finally:
            codefile.close()

