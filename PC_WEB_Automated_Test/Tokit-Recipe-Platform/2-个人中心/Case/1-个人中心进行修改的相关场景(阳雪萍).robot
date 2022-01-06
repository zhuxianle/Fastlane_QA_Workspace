*** Settings ***
Library           AutoItLibrary
Library           Selenium2Library
Resource          ../Element/Element.robot
Resource          ../Flow/Flow_对个人中心进行编辑.robot

*** Variables ***
${UserLogin_Name}    daisy@fstln.io    #用户邮箱
${UserLogin_Password}    Daisy123456    #用户密码
${First_Name}     Daisy    #设置用户名的姓氏
${Last_Name}      Yang    #设置用户名的姓名
${Select_Gender}    Female    #选择性别
${Email}          Daisy    #邮箱
${Phone_Number}    13048864661    #设置手机号

*** Test Cases ***
Case_对个人资料进行编辑
    [Tags]    Automated
    打开浏览器    ${Tokit_Recipes_NA_URL}    ${Browser_Type}
    Maximize Browser Window    #将浏览器最大化
    点击个人中心的Icon
    用户进行登录    ${UserLogin_Name}    ${UserLogin_Password}
    进入个人中心页面
    进入个人中心的个人信息页面
    点击编辑个人资料的按钮
    等待编辑个人资料的文案可见
    输入姓氏
    输入姓名
    选择性别
    选择国家地区
    输入手机号
    选择年份
    选择月份
    选择日期
    点击个人资料的提交按钮
    等待用户的姓氏可见
    关闭浏览器

Case_设置测试数据
    ${Set_Year}=    Set Variable    2021
    ${Set_Month}=    Set Variable    12
    ${Set_Day}=    Set Variable    04
    ${Birthday_Date}=    Catenate    SEPARATOR=-    ${Set_Year}    ${Set_Month}    ${Set_Day}    #将年月日用"-"字符串进行拼接

*** Keywords ***
