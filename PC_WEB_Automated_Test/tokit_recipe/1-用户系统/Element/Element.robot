*** Settings ***
Library           Selenium2Library
Library           AutoItLibrary

*** Variables ***

*** Keywords ***
校验是否为测试环境
    [Arguments]    ${site_url}    ${test_environment_password}
    Open Browser    {site_url}
    ${password}=    Run Keyword And Return Status    Page Should Contain Element    id=password    10
    Run Keyword If    "${password}"=="True"    log    当前站点为测试环境，需要输入密码
    ...    ELSE    LOG    当前站点非测试环境，不需要输入密码
    Input Password    id=password    ${test_environment_password}
    Click Button    xpath=//div[@class="content--block"]/form/button

点击个人中心的Icon
    Sleep    2
    ${personal_center_icon}    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//div[@id="UserInfo"]/a/span    10    #等待个人中心的图标可见
    Run Keyword And Return If    '${personal_center_icon}'=='PASS'    AutoItLibrary.Mouse Down    xpath=//div[@id="UserInfo"]/a/span
    ...    ELSE    fail    找不到个人中心的图标    #等待个人中心的图标可见，悬浮至个人中心的图标上
    Click Element    xpath=//div[@id="UserInfo"]/a/span    #点击个人中心的图标

进入个人中心页面
    sleep    3
    FOR    ${index}    IN RANGE    20
        ${staus}    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//div[@id="UserInfo"]/a/span    20    #等待个人中心的图标可见，悬浮至个人中心的图标上
        Run Keyword If    ${staus}==True    Exit For Loop
        sleep    3
        log    ${index}
    END
    Mouse Over    xpath=//div[@id="UserInfo"]/a/span
    Mouse Over    xpath=//div[@id="shopify-section-header"]/header//div[2]/a[2]/span
    ${my_collection}=    Get Text    xpath=//div[@id="shopify-section-header"]/header//div[2]/a[2]/span
    ${my_collection1}=    Set Variable    My Collection    #设置临时变量
    Run Keyword If    '${my_collection}'=="${my_collection1}"    Mouse Over    xpath=//div[@id="shopify-section-header"]/header//div[2]/a[2]/span
    Click Element    xpath=//div[@id="shopify-section-header"]/header//div[2]/a[2]/span    #点击二级导航栏的"account"链接进行跳转
    Sleep    2

用户退出登录
    Wait Until Element Is Visible    xpath=//li[2]/div[@id="UserInfo"]/a/span    10    #等待个人中心的图标可见，悬浮至个人中心的图标上
    AutoItLibrary.Mouse Down    xpath=//li[2]/div[@id="UserInfo"]/a/span
    Mouse Over    xpath=//li[2]/div[@id="UserInfo"]/a/span    #鼠标悬浮至个人中心的icon上
    Mouse Over    xpath=//div[@id="shopify-section-header"]/header/nav/div//div[2]/a[3]    #鼠标悬浮至退出登录按钮上
    Click Element    xpath=//div[@id="shopify-section-header"]/header/nav/div//div[2]/a[3]    #点击退出登录的按钮

点击页头的搜索框
    Wait Until Element Is Visible    id=CartInfo    10
    AutoItLibrary.Mouse Up    id=CartInfo
    Click Element    id=CartInfo

跳转至注册页面
    ${create_account}=    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//section[@class="container py-8"]/div/div[3]/a[1]    15
    Run Keyword If    '${create_account}'=='True'    Click Element    xpath=//section[@class="container py-8"]/div/div[3]/a[1]
    ...    ELSE    FAIL    页面找不到"Create Account"的跳转地址

用户进行登录
    [Arguments]    ${userlogin_name}    ${userlogin_password}
    Wait Until Element Is Visible    xpath=//section[@class="container py-8"]/div/h2    10    #等待用户登录页面的标题可见
    Input Text    xpath=//input[@id="floatingInput"]    ${userlogin_name}    #用户登录页面输入正确的用户邮箱
    Set Global Variable    ${userlogin_name}
    Input Text    xpath=//input[@id="floatingPassword"]    ${userlogin_password}    #用户登录页面输入正确的的密码
    Set Global Variable    ${userlogin_password}
    Click Button    xpath=//form[@class="as-login-form mt-4"]/button    #点击登录按钮

关闭浏览器
    Close Browser

将浏览器最大化
    Maximize Browser Window    #将浏览器最大化

点击框架页头的一级菜单
    [Arguments]    ${num}
    [Documentation]    参数注解： _页头的一级菜单选项_
    ...
    ...    *${memu-pic1}* ：表示页面上的 *哪一个* 一级菜单（用数字表示菜单项），如果不填则 *默认选择* 第一个一级菜单
    ...
    ...    1: Popular /====/
    ...    2：Latest Collections/====/
    ...    3：Store/==== /
    ...    4: About TOKIT/====/
    Wait Until Element Is Visible    xpath=//div[@id="collapseExample"]/div/ul/li[${num}]/a/span    10
    Click Element    xpath=//div[@id="collapseExample"]/div/ul/li[${num}]/a/span

跳转至重置密码页面
    ${forget_password}=    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//section[@class="container py-8"]/div/div[3]/a[2]    15
    Run Keyword If    '${forget_password}'=='True'    Click Element    xpath=//section[@class="container py-8"]/div/div[3]/a[2]
    ...    ELSE    FAIL    页面找不到"Forgot Password"的跳转地址
