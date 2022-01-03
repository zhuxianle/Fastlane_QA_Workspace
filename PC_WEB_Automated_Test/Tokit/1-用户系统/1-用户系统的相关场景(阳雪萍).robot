*** Settings ***
Library           AutoItLibrary
Resource          ../Common_Library.robot
Library           Selenium2Library
Resource          L3_Element_用户进行登录.robot
Resource          L2_Components.robot
Library           DatabaseLibrary
Resource          L3_Element_用户进行注册.robot
Resource          L3_Element_用户申请重置密码.robot

*** Variables ***
${UserLogin_Name}    daisy@fstln.io    #用户登录邮箱
${UserLogin_Password}    Daisy123456    #用户登录密码
${Register_Account_Suffixt}    Test@fstln.io    #新注册账号
${Site_URL}       https://chunmi.myshopify.com/    #测试环境的访问地址
${Test_Environment_Password}    chunmi_    #访问测试环境的密码
${Set_New_Password}    Daisy123456

*** Test Cases ***
Case_用户进行注册
    [Setup]
    Open Browser    ${Tokit_Recipes_NA_URL}    ${Browser_Type}    #打开浏览器
    将浏览器最大化
    #    校验是否为测试环境    ${Tokit_Recipes_NA_URL}    chunmi_    #打开浏览器
    点击个人中心的icon
    跳转至注册页面
    输入未注册账号进行注册    ${Register_Account_Suffixt}
    悬浮至设置密码的文本框
    输入新密码    ${Set_New_Password}
    输入二次确认密码    ${Set_New_Password}
    等待设置用户昵称可见
    点击设置昵称页面的下一步
    进入个人中心页面
    等待个人中心的图标可见
    判断用户邮箱可见后退出登录
    关闭浏览器
    [Teardown]    Run Keyword If    '${PREV TEST STATUS}'=='FAIL'    fail    Run Keywords    Import Library    OperatingSystem
    ...    AND    OperatingSystem.run    taskkill /F /IM WerFault.exe

Case_用户进行登录
    Open Browser    ${Tokit_Recipes_EU_URL}    #打开浏览器
    将浏览器最大化
    点击个人中心的Icon
    用户进行登录    ${UserLogin_Name}    ${userLogin_Password}
    进入个人中心页面
    加载菜单后点击个人中心    1
    关闭浏览器
    [Teardown]    Run Keyword If    '${PREV TEST STATUS}'=='FAIL'    fail    Run Keywords    Import Library    OperatingSystem
    ...    AND    OperatingSystem.run    taskkill /F /IM WerFault.exe

Case_用户申请重置密码
    Open Browser    ${Tokit_Recipes_EU_URL}    #打开浏览器
    将浏览器最大化
    点击个人中心的Icon
    跳转至重置密码页面
    输入已注册邮箱进行重置密码
    重置密码页面点击Reset按钮
    判断页面是否展示重置密码的邮箱
    关闭浏览器
    [Teardown]    Run Keyword If    '${PREV TEST STATUS}'=='FAIL'    fail    Run Keywords    Import Library    OperatingSystem
    ...    AND    OperatingSystem.run    taskkill /F /IM WerFault.exe

1-Case_数据库初始化
    #先处理下数据库
    DatabaseLibrary.Connect To Database Using Custom Params    pymysql    db='aws-test01',user='root',password='ng6brE9LqSrt0M4H8HUD',host='18.167.6.45',port=3306
    ${query}=    DatabaseLibrary.Query    SELECT * FROM users
    log    ${query}
    Execute Sql String    SELECT * FROM users
    Disconnect From Database

*** Keywords ***
