@echo off
echo 注意：如果firefox浏览器升级到了50.0.0版本以上，则需要同步升级selenium，且将最新版的 geckodriver.exe 文件放置在 Python 安装目录下

pip install Pillow-3.2.0-cp27-cp27m-win_amd64.whl
pip install setuptools-scm -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install pyyaml -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install pyodbc -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install xlrd -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install xlwt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install xlutils -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install requests -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install requests_ntlm -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install simplejson -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install jsonschema -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install uiautomator -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install matplotlib -i http://pypi.douban.com/simple --trusted-host pypi.douban.com


pip install robotframework_ride -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install robotframework_appiumlibrary==1.4.3 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install robotframework_databaselibrary==0.8.1 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install robotframework_selenium2library==1.8.0 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install Selenium2LibraryExtension -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install robotframework-allurereport -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install robotframework-pabot -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

pause