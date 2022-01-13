*** Settings ***
Library           Selenium2Library

*** Variables ***

*** Keywords ***
进入个人中心的个人信息页面
    FOR    ${index}    IN RANGE    20
        ${staus}    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//main[@id="root"]//ul/li[2]/a/span    10
        Run Keyword If    ${staus}==True    Exit For Loop
        sleep    3
        log    ${index}
    END
    log    ${index}
    Click Element    xpath=//main[@id="root"]/div//div[2]/ul/li[1]/a/span

进入个人中心的我的收藏页面
    Wait Until Element Is Visible    xpath=//main[@id="root"]//ul/li[2]/a/span
    Click Element    xpath=//main[@id="root"]/div//div[2]/ul/li[2]/a/span

打开浏览器
    [Arguments]    ${Tokit_Recipes_NA_URL}    ${Browser_Type}
    Open Browser    ${Tokit_Recipes_NA_URL}    ${Browser_Type}    #打开浏览器

点击个人中心的icon
    Sleep    2
    ${personal_Center_Icon}    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//div[@id="UserInfo"]/a/span    10    #等待个人中心的图标可见
    Run Keyword And Return If    '${Personal_Center_Icon}'=='PASS'    AutoItLibrary.Mouse Down    xpath=//div[@id="UserInfo"]/a/span
    ...    ELSE    fail    找不到个人中心的图标    #等待个人中心的图标可见，悬浮至个人中心的图标上
    Click Element    xpath=//div[@id="UserInfo"]/a/span    #点击个人中心的图标

用户进行登录
    [Arguments]    ${userLogin_Name}    ${userLogin_Password}
    Wait Until Element Is Visible    xpath=//section[@class="container py-8"]/div/h2    10    #等待用户登录页面的标题可见
    Input Text    xpath=//input[@id="floatingInput"]    ${userLogin_Name}    #用户登录页面输入正确的用户邮箱
    Set Global Variable    ${userLogin_Name}
    Input Text    xpath=//input[@id="floatingPassword"]    ${userLogin_Password}    #用户登录页面输入正确的的密码
    Set Global Variable    ${userLogin_Password}
    Click Button    xpath=//form[@class="as-login-form mt-4"]/button    #点击登录按钮

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

关闭浏览器
    Close Browser
