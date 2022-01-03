# -*- coding: utf-8 -*-

import os
from robot.libraries.BuiltIn import BuiltIn
import robot
import tempfile
from keywordgroup import KeywordGroup
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from pytesser import *


class _ScreenshotKeywords(KeywordGroup):

    def __init__(self):
        self._screenshot_index = 0

    # Public

    def capture_page_screenshot(self, filename=None):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot is saved into file
        `appium-screenshot-<counter>.png` under the directory where
        the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format.

        `css` can be used to modify how the screenshot is taken. By default
        the bakground color is changed to avoid possible problems with
        background leaking when the page layout is somehow broken.
        """
        path, link = self._get_screenshot_paths(filename)

        if hasattr(self._current_application(), 'get_screenshot_as_file'):
            self._current_application().get_screenshot_as_file(path)
        else:
            self._current_application().save_screenshot(path)

        # Image is shown on its own row and thus prev row is closed on purpose
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))

    def capture_element_screenshot(self, locator):
        """关键字功能： 1、获取当前元素的截图。截图保存至系统临时目录

                       2、根据当前元素截图，解析识别其内容并返回该字符串
        """
        PATH = lambda p: os.path.abspath(p)
        TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")
        element = self._element_find(locator, True, True)
        #先截取整个屏幕，存储至系统临时目录下
        self._current_application().get_screenshot_as_file(TEMP_FILE)

        #获取元素位置信息
        location = element.location
        size = element.size
        box = (int(location["x"]), int(location["y"]), int(location["x"]) + int(size["width"]), int(location["y"]) + int(size["height"]))

        #截取图片
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box=box)

        if newImage.mode != "RGB":
            newImage = newImage.convert("RGB")

        filename = TEMP_FILE.split(".")[0] + ".bmp"
        path, link = self._get_screenshot_paths(filename)
        newImage.save(filename)

        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))

        img = newImage.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(4)
        img = img.convert('1')
        img.load()
        vcode = image_to_string(img)

        return vcode

    def capture_page_screenshot_for_Performance_Test(self, file_path):
        """截图关键字，用于性能测试。

        参数：
        file_path：截图保存的目录
        """
        path = self._get_screenshot_paths_for_Performance_Test(file_path)

        if hasattr(self._current_application(), 'get_screenshot_as_file'):
            self._current_application().get_screenshot_as_file(path)
        else:
            self._current_application().save_screenshot(path)

    # Private

    def _get_case_name(self):
        variables = BuiltIn().get_variables()
        return variables['${TEST NAME}']

    def _get_screenshot_paths(self, filename):
        if not filename:
            self._screenshot_index += 1
            filename = 'appium-screenshot-%d.png' % self._screenshot_index
        else:
            filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link

    def _get_screenshot_paths_for_Performance_Test(self, file_path):
        #首先检查当前参数目录和其父目录是否存在，不存在就先创建
        if not os.path.exists(file_path):
            if not os.path.exists(os.path.dirname(os.path.abspath(file_path))):
                os.mkdir(os.path.dirname(os.path.abspath(file_path)))
            os.mkdir(file_path)

        case_name = self._get_case_name()
        filename = case_name + ".jpg"
        if not os.path.exists(file_path + "/" + case_name):
            os.mkdir(file_path + "/" + case_name)
        path = os.path.join(file_path + "/" + case_name, filename)

        return path
