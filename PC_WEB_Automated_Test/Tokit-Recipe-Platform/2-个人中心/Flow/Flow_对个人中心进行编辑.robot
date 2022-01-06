*** Settings ***
Library           Selenium2Library
Resource          ../Element/Element.robot

*** Keywords ***
点击编辑个人资料的按钮
    ${Edit_Profile}    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//main[@id="root"]//div/div[1]/a    10
    Run Keyword If    "${Edit_Profile}"=="True"    Click Element    xpath=//main[@id="root"]//div/div[1]/a
    ...    ELSE    log    无法定位到“Edit profile”的元素的位置

输入姓氏
    Input Text    id=first-name    ${First_Name}

输入姓名
    Input Text    id=last-name    ${Last_Name}

选择性别
    Click Element    id=gender-female

输入手机号
    Input Text    id=phone-number    13048864661

选择年份
    Select From List By Label    id=year    2001

选择国家地区
    Select From List By Index    id=region    7

选择月份
    Select From List By Label    id=month    12

选择日期
    Select From List By Label    id=day    04

点击个人资料的提交按钮
    Click Button    xpath=//button[@class="as-submit btn btn-primary w-100 mt-4"]

等待用户的姓氏可见
    Wait Until Element Is Visible    id=first-name    10

等待编辑个人资料的文案可见
    Wait Until Element Is Visible    xpath=//div[@class="as-set-username"]/h2    10
