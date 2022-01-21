*** Settings ***
Library           Selenium2Library

*** Test Cases ***
输入正确账号密码，登陆成功
    open browser    https://us.tokitglobal.com/    ff    #打开浏览器，进入纯米商城US站
    Click Element    xpath=//*[@id="shopify-section-header"]/header/nav/div/ul[2]/li[1]    #点击个人中心icon
    Wait Until Element Is Visible    xpath=//*[@id="floatingInput"]    5    #等待元素出现，进行下一步操作
    Input text    xpath=//*[@id="floatingInput"]    kevin@fstln.io    #点击邮箱输入框，输入正确账号
    Wait Until Element Is Visible    xpath=//*[@id="floatingPassword"]    5    #等待元素出现，进行下一步操作
    Input text    xpath=//*[@id="floatingPassword"]    Xzk991231    #点击密码输入框，输入正确密码
    sleep    1    #等待1秒
    Click element    xpath=/html/body/main/section/section/div/form/button    #点击Login登陆
    sleep    3    #等待3秒
    Close browser    #退出浏览器...

输入正确账号错误密码，登陆失败
    open browser    https://us.tokitglobal.com/    gc    #打开浏览器，进入纯米商城US站
    Click Element    xpath=//*[@id="shopify-section-header"]/header/nav/div/ul[2]/li[1]    #点击个人中心icon
    Wait Until Element Is Visible    xpath=//*[@id="floatingInput"]    5    #等待元素出现，进行下一步操作
    Input text    xpath=//*[@id="floatingInput"]    kevin@fstln.io    #点击邮箱输入框，输入正确账号
    Wait Until Element Is Visible    xpath=//*[@id="floatingPassword"]    5    #等待元素出现，进行下一步操作
    Input text    xpath=//*[@id="floatingPassword"]    123123    #点击密码输入框，输入错误密码
    sleep    1    #等待1秒
    Click element    xpath=/html/body/main/section/section/div/form/button    #点击Login登陆
    sleep    3    #等待3秒
    Close browser    #退出浏览器

输入未注册邮箱，登陆失败
    open browser    https://us.tokitglobal.com/    gc    #打开浏览器，进入纯米商城US站
    Click Element    xpath=//*[@id="shopify-section-header"]/header/nav/div/ul[2]/li[1]    #点击个人中心icon
    Wait Until Element Is Visible    xpath=//*[@id="floatingInput"]    5    #等待元素出现，进行下一步操作
    Input text    xpath=//*[@id="floatingInput"]    eqwe2e1@test.com    #点击邮箱输入框，输入未注册账号
    Wait Until Element Is Visible    xpath=//*[@id="floatingPassword"]    5    #等待元素出现，进行下一步操作
    Input text    xpath=//*[@id="floatingPassword"]    13123    #点击密码输入框，输入任意密码
    sleep    1    #等待1秒
    Click element    xpath=/html/body/main/section/section/div/form/button    #点击Login登陆
    sleep    3    #等待3秒
    Close browser    #退出浏览器

空输入账号密码，登陆失败
    open browser    https://us.tokitglobal.com/    gc    #打开浏览器，进入纯米商城US站
    Click Element    xpath=//*[@id="shopify-section-header"]/header/nav/div/ul[2]/li[1]    #点击个人中心icon
    sleep    3    #等待1秒
    Click element    xpath=/html/body/main/section/section/div/form/button    #点击Login登陆
    sleep    3    #等待3秒
    Close browser    #退出浏览器

空输入账号，输入任意密码，登陆失败
    open browser    https://us.tokitglobal.com/    gc    #打开浏览器，进入纯米商城US站
    Click Element    xpath=//*[@id="shopify-section-header"]/header/nav/div/ul[2]/li[1]    #点击个人中心icon
    Wait Until Element Is Visible    xpath=//*[@id="floatingPassword"]    5    #等待元素出现，进行下一步操作
    Input text    xpath=//*[@id="floatingPassword"]    123iia    #点击密码输入框，输入任意密码
    sleep    1    #等待1秒
    Click element    xpath=/html/body/main/section/section/div/form/button    #点击Login登陆
    sleep    3    #等待3秒
    Close browser    #退出浏览器

输入任意账号，空输入密码，登陆失败
    open browser    https://us.tokitglobal.com/    gc    #打开浏览器，进入纯米商城US站
    Click Element    xpath=//*[@id="shopify-section-header"]/header/nav/div/ul[2]/li[1]    #点击个人中心icon
    Wait Until Element Is Visible    xpath=//*[@id="floatingInput"]    5    #等待元素出现，进行下一步操作
    Input text    xpath=//*[@id="floatingInput"]    kevin@fstln.io    #点击邮箱输入框，输入正确账号
    sleep    1    #等待1秒
    Click element    xpath=/html/body/main/section/section/div/form/button    #点击Login登陆
    sleep    3    #等待3秒
    Close browser    #退出浏览器
