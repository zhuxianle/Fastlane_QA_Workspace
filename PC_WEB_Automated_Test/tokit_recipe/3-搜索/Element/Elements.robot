*** Settings ***
Library           Selenium2Library

*** Variables ***

*** Keywords ***
打开浏览器
    [Arguments]    ${Tokit_Recipes_NA_URL}    ${Browser_Type}
    Open Browser    ${Tokit_Recipes_NA_URL}    ${Browser_Type}    #打开浏览器

点击搜索按钮
    Wait Until Element Is Visible    xpath=//header[@class="site-top-nav"]/nav/div/ul/li[1]/a/span    10
    Click Element    xpath=//header[@class="site-top-nav"]/nav/div/ul/li[1]/a/span

等待搜索结果列表的搜索数据可见
    sleep    5
    Wait Until Element Is Visible    xpath=//ul[@class="p-0 row gx-3 gx-md-4 row-cols-2 row-cols-md-3 row-cols-lg-4 mb-0"]/li[1]    10

点击搜索结果页面的搜索数据
    Click Element    xpath=//ul[@class="p-0 row gx-3 gx-md-4 row-cols-2 row-cols-md-3 row-cols-lg-4 mb-0"]/li[1]

点击搜索页面的搜索按钮
    Click Element    xpath=//main[@id="root"]//div[1]/button/span[1]

筛选项可见后勾选筛选项
    Wait Until Element Is Visible    xpath=//h6[text()="Main Course"]    10
    Click Element    xpath=//div[@class=" border-bottom-gray d-flex flex-wrap pb-2 mb-3"]/div[1]/input

聚焦至搜索按钮的位置
    Focus    xpath=//div[@class="modal-footer border-0 d-flex justify-content-center pb-5"]/button[1]

点击筛选项的搜索按钮
    Click Button    xpath=//div[@class="modal-footer border-0 d-flex justify-content-center pb-5"]/button[1]

关闭浏览器
    Close Browser
