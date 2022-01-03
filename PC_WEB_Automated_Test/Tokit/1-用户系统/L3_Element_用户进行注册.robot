*** Settings ***
Library           Selenium2Library

*** Keywords ***
输入二次确认密码
    [Arguments]    ${Confirm_Password}
    Input Text    id=confirm-pwd    ${Confirm_Password}
    Click Button    xpath=//form[@class="as-set-pwd-form mt-4"]/button

输入未注册账号进行注册
    [Arguments]    ${Register_Account_Suffixt}
    Wait Until Element Is Enabled    id=email-register    10
    ${time}=    Evaluate    datetime.datetime.now().strftime('%H%M%S')    datetime    #获取当前的日期戳
    ${Register_Account_Suffixt}    Set Variable    ${time}${Register_Account_Suffixt}    #使用获取的时间戳，作为新注册的邮箱
    Set Global Variable    ${Register_Account_Suffixt}
    Input Text    xpath=//input[@id="email-register"]    ${Register_Account_Suffixt}
    Click Element    xpath=//input[@id="flexCheckDefault"]
    Click Button    xpath=//form[@class="as-check-email-form mt-4"]/button

输入新密码
    [Arguments]    ${Set_New_Password}
    Input Text    id=set-pwd    ${Set_New_Password}
    ${Input_Password}    Get Text    id=set-pwd
    Set Global Variable    ${Input_Password}

等待设置用户昵称可见
    Sleep    5
    Wait Until Element Is Visible    id=username    10

点击设置昵称页面的下一步
    Click Button    xpath=//form[@class="as-set-username-form mt-4"]/button

等待个人中心的图标可见
    Wait Until Element Is Visible    xpath=//body[@id="account"]/div[4]//div/div[1]/p[2]    10
    ${Register_Account_Suffixt1}    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//div[@id="UserInfo"]/a/span    10    #等待个人中心的图标可见
    Set Global Variable    ${Register_Account_Suffixt1}

悬浮至设置密码的文本框
    Sleep    3
    ${set_pwd}=    Run Keyword And Return Status    Wait Until Element Is Visible    id=set-pwd    10
    Run Keyword If    "${set_pwd}"=="PASS"    Mouse Over    id=set-pwd

判断用户邮箱可见后退出登录
    Run Keyword And Return If    "${Register_Account_Suffixt}"=="${Register_Account_Suffixt1}"    用户退出登录
    ...    ELSE    fail    系统获取用户昵称失败
