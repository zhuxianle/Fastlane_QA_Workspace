*** Settings ***
Library           Selenium2Library

*** Keywords ***
输入已注册邮箱进行重置密码
    Wait Until Element Is Visible    id=email    10
    Input Text    id=email    ${Register_Account_Suffixt}

重置密码页面点击Reset按钮
    click button    xpath=//form[@class="as-forgot-pwd-form mt-4"]/button    #点击ReSet按钮
    Wait Until Element Is Visible    xpath=//div[@class="text-center mt-2"]/p[2]    10

判断页面是否展示重置密码的邮箱
    ${Register_Account_Suffixt1}    Get Text    xpath=//div[@class="text-center mt-2"]/p[2]
    Run Keyword If    "${Register_Account_Suffixt}"=="${Register_Account_Suffixt1}"    log    重置密码页面，可正常查看申请忘记密码的注册邮箱
    ...    ELSE    log    重置密码页面，不展示忘记密码的注册邮箱
