#coding=utf-8

import robot
import os, errno
import tempfile
from robot.libraries.BuiltIn import BuiltIn
from Selenium2Library import utils
from keywordgroup import KeywordGroup
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont


class _ScreenshotKeywords(KeywordGroup):

    def __init__(self):
        self._screenshot_index = 0
        self._screenshot_path_stack = []
        self.screenshot_root_directory = None

    # Public

    def set_screenshot_directory(self, path, persist=False):
        """Sets the root output directory for captured screenshots.

        ``path`` argument specifies the absolute path where the screenshots should
        be written to. If the specified ``path`` does not exist, it will be created.
        Setting ``persist`` specifies that the given ``path`` should
        be used for the rest of the test execution, otherwise the path will be restored
        at the end of the currently executing scope.
        """
        path = os.path.abspath(path)
        self._create_directory(path)
        if persist is False:
            self._screenshot_path_stack.append(self.screenshot_root_directory)
            # Restore after current scope ends
            utils.events.on('scope_end', 'current', self._restore_screenshot_directory)

        self.screenshot_root_directory = path

    def capture_page_screenshot(self, filename=None):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot is saved into file
        `selenium-screenshot-<counter>.png` under the directory where
        the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format. If an absolute or relative path is given
        but the path does not exist it will be created.

        `css` can be used to modify how the screenshot is taken. By default
        the bakground color is changed to avoid possible problems with
        background leaking when the page layout is somehow broken.
        """
        path, link = self._get_screenshot_paths(filename)
        self._create_directory(path)

        if hasattr(self._current_browser(), 'get_screenshot_as_file'):
          if not self._current_browser().get_screenshot_as_file(path):
              raise RuntimeError('Failed to save screenshot ' + filename)
        else:
          if not self._current_browser().save_screenshot(path):
            raise RuntimeError('Failed to save screenshot ' + filename)

        # Image is shown on its own row and thus prev row is closed on purpose
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))

    def capture_element_screenshot(self, locator):
        """关键字功能： 1、获取当前元素的截图。截图保存至系统临时目录

                       2、根据当前元素截图，解析识别其内容并返回该字符串(暂不实现)
        """
        PATH = lambda p: os.path.abspath(p)
        TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")

        element = self._element_find(locator, True, True)
        #先截取整个屏幕，存储至系统临时目录下
        self._current_browser().get_screenshot_as_file(TEMP_FILE)

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

        # img = newImage.filter(ImageFilter.MedianFilter())
        # enhancer = ImageEnhance.Contrast(img)
        # img = enhancer.enhance(4)
        # img = img.convert('1')
        # img.load()
        # vcode = image_to_string(img)
        #
        # return vcode

    # Private
    def _create_directory(self, path):
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(target_dir):
                    pass
                else:
                    raise

    def _get_screenshot_directory(self):

        # Use screenshot root directory if set
        if self.screenshot_root_directory is not None:
            return self.screenshot_root_directory

        # Otherwise use RF's log directory
        return self._get_log_dir()

    # should only be called by set_screenshot_directory
    def _restore_screenshot_directory(self):
        self.screenshot_root_directory = self._screenshot_path_stack.pop()

    def _get_screenshot_paths(self, filename):
        case_tags = self._get_case_tag()
        if not filename:
            self._screenshot_index += 1
            # pid = os.getpid()
            # filename = 'selenium-%s-screenshot-%d.png' % (pid, self._screenshot_index)
            if case_tags:
                filename = '%s_selenium-screenshot-%d.png' % (case_tags[0], self._screenshot_index)
            else:
                filename = 'selenium-screenshot-%d.png' % (self._screenshot_index)
        else:
            filename = filename.replace('/', os.sep)

        screenshotDir = self._get_screenshot_directory()
        logDir = self._get_log_dir()
        path = os.path.join(screenshotDir, filename)
        link = robot.utils.get_link_path(path, logDir)
        return path, link

    def _get_case_tag(self):
        variables = BuiltIn().get_variables()
        return variables['@{TEST TAGS}']

if __name__ == "__main__":
    s = _ScreenshotKeywords()
    s.capture_element_screenshot("id=search1")
