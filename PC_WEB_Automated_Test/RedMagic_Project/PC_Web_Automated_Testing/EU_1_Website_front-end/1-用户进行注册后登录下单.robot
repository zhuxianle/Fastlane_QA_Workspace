*** Settings ***
Library           Selenium2Library
Library           AutoItLibrary
Resource          ../L2_Components.robot
Resource          ../L3_Element_用户在购物车登录后下单.robot
Resource          ../L3_Element_商城页登录.robot
Library           String

*** Variables ***
${User_Email}     daisy@fstln.io    #用户登录账号
${User_Password}    13048864661    #用户账号密码
${First_Name}     Daisy_Test    #输入第一个姓
${Last_Name}      Yang    #输入用户的姓名
${Shipping_Address}    Test Address    #用户输入收货地址
${Shipping_Address2_field}    Shipping_Address2_field_Test    #详细地址
${City}           City Test    #所在城市
${Postal_Code}    123456    #输入邮编
${Tel}            13048864661    #输入电话号码
${Standard}       Standard    #物流标准收费
${Priority}       Priority    # 物流状态-优先发货

*** Test Cases ***
Case1_用户进行注册
    [Setup]
    Open Browser    ${Buyer_EU_URL}
    Maximize Browser Window    #最大化全屏查看
    Wait Until Element Is Visible    xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[5]/a[1]    10
    Click Element    xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[5]/a[1]
    Wait Until Element Is Visible    xpath=//a[@id="customer_register_link"]    10    #等待注册入口可见
    Click Element    xpath=//a[@id="customer_register_link"]
    Wait Until Element Is Visible    id=UserEmail    10
    Input Text    id=UserEmail
    Input Text    xpath=//input[@id="CreatePassword"]

Case2_用户进行登录
    [Tags]    RM_Automated
    [Setup]    Run Keywords    Import Library    OperatingSystem
    ...    AND    OperatingSystem.run    taskkill /F /IM WerFault.exe
    Open Browser    ${Buyer_EU_URL}    #打开浏览器
    Maximize Browser Window
    点击进入登录页
    登录页输入用户名
    登录页输入密码
    登录页点击登录按钮
    点击进入个人中心
    判断用户是否登录正常
    [Teardown]    Close All Browsers

Case3_用户购物车内登录下单
    [Tags]    RM_Automated
    [Setup]    Run Keywords    Import Library    OperatingSystem
    ...    AND    OperatingSystem.run    taskkill /F /IM WerFault.exe
    Open Browser    ${Buyer_EU_URL}
    Maximize Browser Window
    进入首页的导航栏页    2
    进入购买手机页
    EU商城-选择第二个商品后获取金额    2
    EU商城选择手机配件后获取配件金额    2
    计算商品总金额
    将商品加入购物车
    验证购物车的金额是否正常
    点击去支付按钮    Tmp_Checkout.png
    等待登录输入框可见
    输入用户名以及密码
    点击登录按钮
    下拉选择保存的地址
    输入收货地址信息
    点击去购买
    验证物流选项是否可见
    [Teardown]    Close All Browsers

Testcase
    Open Browser    ${Buyer_EU_URL}
    Maximize Browser Window
    Wait Until Element Is Visible    xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[4]/a[1]    10
    点击Home首页

*** Keywords ***
