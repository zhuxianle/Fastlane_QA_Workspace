*** Settings ***
Library           AutoItLibrary
Library           Selenium2Library
Library           DatabaseLibrary
Resource          ../Flow/Flow_用户进行注册.robot
Resource          ../Flow/Flow_用户申请重置密码.robot
Resource          ../Element/Element.robot
Resource          ../../Common/Common.robot

*** Variables ***
${userlogin_name}    daisy@fstln.io    #用户登录邮箱
${userlogin_password}    Daisy123456    #用户登录密码
${register_account_suffixt}    Test@fstln.io    #新注册账号
${site_url}       https://chunmi.myshopify.com/    #测试环境的访问地址
${test_environment_password}    chunmi_    #访问测试环境的密码
${set_new_password}    Daisy123456

*** Test Cases ***
Case_用户进行注册
    [Setup]
    Open Browser    ${tokit_recipes_na_url}    ${browser_type}    #打开浏览器
    将浏览器最大化
    点击个人中心的icon
    跳转至注册页面
    输入未注册账号进行注册    ${register_account_suffixt}
    悬浮至设置密码的文本框
    输入新密码    ${set_new_password}
    输入二次确认密码    ${set_new_password}
    等待设置用户昵称可见
    点击设置昵称页面的下一步
    进入个人中心页面
    等待个人中心的图标可见
    判断用户邮箱可见后退出登录
    关闭浏览器
    [Teardown]    Run Keyword If    '${PREV TEST STATUS}'=='FAIL'    fail    Run Keywords    Import Library    OperatingSystem
    ...    AND    OperatingSystem.run    taskkill /F /IM WerFault.exe

Case_用户进行登录
    Open Browser    ${tokit_recipes_na_url}    ${browser_type}    #打开浏览器
    将浏览器最大化
    点击个人中心的Icon
    用户进行登录    ${userlogin_name}    ${userlogin_password}
    关闭浏览器
    [Teardown]    Run Keyword If    '${PREV TEST STATUS}'=='FAIL'    fail    Run Keywords    Import Library    OperatingSystem
    ...    AND    OperatingSystem.run    taskkill /F /IM WerFault.exe

Case_用户申请重置密码
    Open Browser    ${tokit_recipes_na_url}    ${browser_type}    #打开浏览器
    将浏览器最大化
    点击个人中心的Icon
    跳转至重置密码页面
    输入已注册邮箱进行重置密码
    重置密码页面点击Reset按钮
    判断页面是否展示重置密码的邮箱
    关闭浏览器
    [Teardown]    Run Keyword If    '${PREV TEST STATUS}'=='FAIL'    fail    Run Keywords    Import Library    OperatingSystem
    ...    AND    OperatingSystem.run    taskkill /F /IM WerFault.exe

Case_数据库初始化(Test)
    #先处理下数据库
    DatabaseLibrary.Connect To Database Using Custom Params    pymysql    db='fstlnerp',user='root',password='ng6brE9LqSrt0M4H8HUD',host='18.167.6.45',port=3306
    ${query}=    DatabaseLibrary.Query    SELECT * FROM users
    log    ${query}
    Execute Sql String    SELECT * FROM users
    Disconnect From Database

*** Keywords ***
