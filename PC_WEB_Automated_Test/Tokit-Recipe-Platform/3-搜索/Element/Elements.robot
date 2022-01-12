*** Settings ***
Library           Selenium2Library

*** Variables ***
${Tokit_Recipes_NA_URL}    https://na.cooknjoy.tokitglobal.com/
${Tokit_Recipes_EU_URL}    https://eu.cooknjoy.tokitglobal.com/
${Browser_Type}    Firefox    #默认为火狐浏览器

*** Keywords ***
打开浏览器
    [Arguments]    ${Tokit_Recipes_NA_URL}    ${Browser_Type}
    Open Browser    ${Tokit_Recipes_NA_URL}    ${Browser_Type}    #打开浏览器

点击搜索按钮
    Wait Until Element Is Visible    xpath=//header[@class="site-top-nav"]/nav/div/ul/li[1]/a/span    10
    Click Element    xpath=//header[@class="site-top-nav"]/nav/div/ul/li[1]/a/span
