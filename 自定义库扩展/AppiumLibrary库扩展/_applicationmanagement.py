# -*- coding: utf-8 -*-

import os
import robot
from appium import webdriver
from AppiumLibrary.utils import ApplicationCache
from keywordgroup import KeywordGroup

from Selenium2Library.utils.browsercache import BrowserCache
from Selenium2Library.locators.windowmanager import WindowManager
from selenium import webdriver as pc_webdriver

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BROWSER_NAMES = {'ff': "_make_ff",
                 'firefox': "_make_ff",
                 'ie': "_make_ie",
                 'internetexplorer': "_make_ie",
                 'googlechrome': "_make_chrome",
                 'gc': "_make_chrome",
                 'chrome': "_make_chrome",
                 'opera' : "_make_opera",
                 'phantomjs' : "_make_phantomjs",
                 'htmlunit' : "_make_htmlunit",
                 'htmlunitwithjs' : "_make_htmlunitwithjs",
                 'android': "_make_android",
                 'iphone': "_make_iphone",
                 'safari': "_make_safari"
                }


class _ApplicationManagementKeywords(KeywordGroup):
    def __init__(self):
        self._cache = ApplicationCache()
        self._timeout_in_secs = float(5)

        self.window_manager = WindowManager()
        self.speed_in_secs = float(0)
        self.timeout_in_secs = float(5)
        self.implicit_wait_in_secs = float(0)

    # Public, open and close

    def close_application(self):
        """Closes the current application."""
        self._debug('Closing application with session id %s' % self._current_application().session_id)
        self._cache.close()

    def close_all_applications(self):
        """Closes all open applications.

        This keyword is meant to be used in test or suite teardown to
        make sure all the applications are closed before the test execution
        finishes.

        After this keyword, the application indices returned by `Open Application`
        are reset and start from `1`.
        """

        self._debug('Closing all applications')
        self._cache.close_all()

    def open_application(self, remote_url, alias=None, **kwargs):
        """Opens a new application to given Appium server.
        Capabilities of appium server, Android and iOS,
        Please check http://appium.io/slate/en/master/?python#appium-server-capabilities
        | *Option*            | *Man.* | *Description*     |
        | remote_url          | Yes    | Appium server url |
        | alias               | no     | alias             |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=iOS      | platformVersion=7.0            | deviceName='iPhone Simulator'           | app=your.app                         |
        | Open Application | http://localhost:4723/wd/hub | platformName=Android | platformVersion=4.2.2 | deviceName=192.168.56.101:5555 | app=${CURDIR}/demoapp/OrangeDemoApp.apk | appPackage=com.netease.qa.orangedemo | appActivity=MainActivity |
        """
        desired_caps = kwargs
        application = webdriver.Remote(str(remote_url), desired_caps)

        self._debug('Opened application with session id %s' % application.session_id)

        return self._cache.register(application, alias)

    def switch_application(self, index_or_alias):
        """Switches the active application by index or alias.

        `index_or_alias` is either application index (an integer) or alias
        (a string). Index is got as the return value of `Open Application`.

        This keyword returns the index of the previous active application,
        which can be used to switch back to that application later.

        Example:
        | ${appium1}=              | Open Application  | http://localhost:4723/wd/hub                   | alias=MyApp1 | platformName=iOS | platformVersion=7.0 | deviceName='iPhone Simulator' | app=your.app |
        | ${appium2}=              | Open Application  | http://localhost:4755/wd/hub                   | alias=MyApp2 | platformName=iOS | platformVersion=7.0 | deviceName='iPhone Simulator' | app=your.app |
        | Click Element            | sendHello         | # Executed on appium running at localhost:4755 |
        | Switch Application       | ${appium1}        | # Switch using index                           |
        | Click Element            | ackHello          | # Executed on appium running at localhost:4723 |
        | Switch Application       | MyApp2            | # Switch using alias                           |
        | Page Should Contain Text | ackHello Received | # Executed on appium running at localhost:4755 |

        """
        old_index = self._cache.current_index
        if index_or_alias is None:
            self._cache.close()
        else:
            self._cache.switch(index_or_alias)
        return old_index

    def reset_application(self):
        """ Reset application """
        driver = self._current_application()
        driver.reset()

    def remove_application(self, application_id):
        """ Removes the application that is identified with an application id

        Example:
        | Remove Application |  com.netease.qa.orangedemo |

        """
        driver = self._current_application()
        driver.remove_app(application_id)

    def get_appium_timeout(self):
        """Gets the timeout in seconds that is used by various keywords.

        See `Set Appium Timeout` for an explanation."""
        return robot.utils.secs_to_timestr(self._timeout_in_secs)

    def set_appium_timeout(self, seconds):
        """Sets the timeout in seconds used by various keywords.

        There are several `Wait ...` keywords that take timeout as an
        argument. All of these timeout arguments are optional. The timeout
        used by all of them can be set globally using this keyword.

        The previous timeout value is returned by this keyword and can
        be used to set the old value back later. The default timeout
        is 5 seconds, but it can be altered in `importing`.

        Example:
        | ${orig timeout} = | Set Appium Timeout | 15 seconds |
        | Open page that loads slowly |
        | Set Appium Timeout | ${orig timeout} |
        """
        old_timeout = self.get_appium_timeout()
        self._timeout_in_secs = robot.utils.timestr_to_secs(seconds)
        return old_timeout

    def get_source(self):
        """Returns the entire source of the current page."""
        return self._current_application().page_source

    def log_source(self, loglevel='INFO'):
        """Logs and returns the entire html source of the current page or frame.

        The `loglevel` argument defines the used log level. Valid log levels are
        `WARN`, `INFO` (default), `DEBUG`, `TRACE` and `NONE` (no logging).
        """
        source = self._current_application().page_source
        self._log(source, loglevel.upper())
        return source

    def go_back(self):
        """Goes one step backward in the browser history."""
        self._current_application().back()

    def lock(self):
        """
        Lock the device
        """
        self._current_application().lock()

    def background_app(self, seconds=5):
        """
        Puts the application in the background on the device for a certain
        duration.
        """
        self._current_application().background_app(seconds)

    def shake(self):
        """
        Shake the device
        """
        self._current_application().shake()

    def portrait(self):
        """
        Set the device orientation to PORTRAIT
        """
        self._rotate('PORTRAIT')

    def landscape(self):
        """
        Set the device orientation to LANDSCAPE
        """
        self._rotate('LANDSCAPE')

    def get_current_context(self):
        """Get current context."""
        return self._current_application().current_context

    def get_contexts(self):
        """Get available contexts."""
        print self._current_application().contexts
        return self._current_application().contexts

    def switch_to_context(self, context_name):
        """Switch to a new context"""
        self._current_application().switch_to.context(context_name)

    def go_to_url(self, url):
        """
        Opens URL in default web browser.

        Example:
        | Open Application  | http://localhost:4755/wd/hub | platformName=iOS | platformVersion=7.0 | deviceName='iPhone Simulator' | browserName=Safari |
        | Go To URL         | http://m.webapp.com          |
        """
        self._current_application().get(url)

    # Private

    def _current_application(self):
        if not self._cache.current:
            raise RuntimeError('No application is open')
        return self._cache.current

    def _get_platform(self):
        try:
            platformName = self._current_application().desired_capabilities['desired']['platformName']
        except Exception, e:
            raise Exception, e
        return platformName.lower()

    def _is_platform(self, platform):
        platformName = self._get_platform()
        return platform.lower() == platformName

    def _is_ios(self):
        return self._is_platform('ios')

    def _is_andriod(self):
        return self._is_platform('android')

    def _rotate(self, orientation):
        driver = self._current_application()
        driver.orientation = orientation

    # new add -----------------------------新添加的方法------------------------------
    def _create_remote_web_driver(self, capabilities_type, remote_url, desired_capabilities=None, profile=None):
        desired_capabilities_object = capabilities_type.copy()

        if type(desired_capabilities) in (str, unicode):
            desired_capabilities = self._parse_capabilities_string(desired_capabilities)

        desired_capabilities_object.update(desired_capabilities or {})

        return pc_webdriver.Remote(desired_capabilities=desired_capabilities_object, command_executor=str(remote_url), browser_profile=profile)

    def _generic_make_browser(self, webdriver_type, desired_cap_type, remote_url, desired_caps):
        if not remote_url:
            browser = webdriver_type()
        else:
            browser = self._create_remote_web_driver(desired_cap_type, remote_url, desired_caps)
        return browser

    def _parse_capabilities_string(self, capabilities_string):
        desired_capabilities = {}

        if not capabilities_string:
            return desired_capabilities

        for cap in capabilities_string.split(","):
            (key, value) = cap.split(":", 1)
            desired_capabilities[key.strip()] = value.strip()

        return desired_capabilities

    def _make_ff(self, remote, desired_capabilites, profile_dir):

        if not profile_dir: profile_dir = FIREFOX_PROFILE_DIR
        profile = pc_webdriver.FirefoxProfile(profile_dir)
        if remote:
            browser = self.create_remote_web_driver(pc_webdriver.DesiredCapabilities.FIREFOX, remote, desired_capabilites, profile)
        else:
            browser = pc_webdriver.Firefox(firefox_profile=profile)
        return browser

    def _make_chrome(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(pc_webdriver.Chrome, pc_webdriver.DesiredCapabilities.CHROME, remote, desired_capabilities)

    def _get_browser_creation_function(self, browser_name):
        func_name = BROWSER_NAMES.get(browser_name.lower().replace(' ', ''))

        return getattr(self, func_name) if func_name else None

    def _make_browser(self, browser_name, desired_capabilities=None, profile_dir=None, remote=None):
        creation_func = self._get_browser_creation_function(browser_name)

        if not creation_func:
            raise ValueError(browser_name + " is not a supported browser.")

        browser = creation_func(remote, desired_capabilities, profile_dir)
        browser.set_speed(self.speed_in_secs)
        browser.set_script_timeout(self.timeout_in_secs)
        browser.implicitly_wait(self.implicit_wait_in_secs)

        return browser

    def _get_window_infos(self, browser):
        window_infos = []
        try:
            starting_handle = browser.get_current_window_handle()
        except NoSuchWindowException:
            starting_handle = None
        try:
            for handle in browser.get_window_handles():
                browser.switch_to_window(handle)
                window_infos.append(browser.get_current_window_info())
        finally:
            if starting_handle:
                browser.switch_to_window(starting_handle)
        return window_infos

    def open_browser_moble(self, url, browser='firefox', alias=None, remote_url="http://localhost:4723/wd/hub", desired_capabilities=None, ff_profile_dir=None):
        """打开手机端的浏览器，用于H5测试，主要是为了能够支持远程连STF环境测试。

        例如:
        |  ${capabilitys}= | Create Dictionary |
        | Set To Dictionary | ${capabilitys} | platformName | android |
        | Set To Dictionary | ${capabilitys} | deviceName | 4d000000b8f23081 |
        | Open Browser Moble | https://192.168.1.207:6001/m-Wap | browser=chrome | alias=chrome | remote_url= http://localhost:4723/wd/hub | desired_capabilities=${capabilitys} |

        desired_capabilities:表示手机端附带参数。必填 （它必须是个字典，所以在使用前先将各种参数存到字典变量内。创建字典需要用到 *Collections库*，使用前记得先导入）。

        remote_url：远程appium server地址。不一定要在本地，只要是可连接的appium都支持。
        """
        if remote_url:
            self._info(u"Opening browser '%s' to base url '%s' through remote server at '%s'" % (browser, url, remote_url))
        else:
            self._info("Opening browser '%s' to base url '%s'" % (browser, url))

        browser_name = browser
        browser = self._make_browser(browser_name, desired_capabilities, ff_profile_dir, remote_url)
        try:
            browser.get(url)
        except:
            self._cache.register(browser, alias)
            self._debug("Opened browser with session id %s but failed to open url '%s'" % (browser.session_id, url))

            raise
        self._debug('Opened browser with session id %s' % browser.session_id)
        #print self.cache.current
        return self._cache.register(browser, alias)

    def get_window_handles(self):
        """
        返回并记录所有新打开的窗口句柄，存到列表内。结合Select Window By Handle使用，使用时以变量下标表示句柄位置。

        例如:
        | ${window}= | get window handles |
        | Select Window By Handle | ${window[1]} |

        ${window[1]}:表示第2个句柄位置
        """

        return self._log_list([ window_info[0] for window_info in self._get_window_infos(self._current_application()) ])

    def select_window_by_handle(self, toHandle=None):
        """
        根据窗口句柄切换浏览器窗口。通过Get Window Handles关键字获得窗口句柄。
        """
        self._current_application().switch_to_window(toHandle)

    def is_app_installed(self, App_Package):
        """ 检查App是否已被安装。参数为要查询的App。返回True或False

        例如:
        | Is App Installed |  com.azt.kaimai8 |

        """
        driver = self._current_application()
        return driver.is_app_installed(App_Package)

    def open_notifications(self):
        """ 打开系统通知栏。（注意：安卓系统专用且只支持API18以上的版本）
        """
        driver = self._current_application()
        return driver.open_notifications()
    # new add -----------------------------新添加的方法------------------------------