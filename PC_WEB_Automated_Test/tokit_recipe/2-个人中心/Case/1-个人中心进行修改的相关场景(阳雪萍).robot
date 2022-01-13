*** Settings ***
Library           AutoItLibrary
Library           Selenium2Library
Resource          ../Element/Element.robot
Resource          ../Flow/Flow_对个人中心进行编辑.robot
Resource          ../../Common/Common.robot

*** Variables ***
${userlogin_name}    daisy@fstln.io    #用户邮箱
${userlogin_password}    Daisy123456    #用户密码
${first_name}     Daisy    #设置用户名的姓氏
${last_name}      Yang    #设置用户名的姓名
${select_gender}    Female    #选择性别
${email}          Daisy    #邮箱
${phone_number}    13048864661    #设置手机号

*** Test Cases ***
Case_对个人资料进行编辑
    [Tags]    tokit_recipe_automated
    打开浏览器    ${tokit_recipes_na_url}    ${browser_type}
    Maximize Browser Window    #将浏览器最大化
    点击个人中心的Icon
    用户进行登录    ${userlogin_name}    ${userlogin_password}
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
    ${set_year}=    Set Variable    2021
    ${set_month}=    Set Variable    12
    ${set_day}=    Set Variable    04
    ${birthday_date}=    Catenate    SEPARATOR=-    ${set_year}    ${set_month}    ${set_day}    #将年月日用"-"字符串进行拼接

*** Keywords ***
