*** Settings ***
Library           Selenium2Library
Resource          ../Element/Elements.robot

*** Test Cases ***
Case_用户下拉选择筛选项进行搜索
    打开浏览器    ${Tokit_Recipes_NA_URL}    ${Browser_Type}
    点击搜索按钮
    Wait Until Element Is Visible    xpath=//div[@id="shopify-section-search-template"]//input    10

Case_用户输入搜索关键词进行搜索
    打开浏览器    ${Tokit_Recipes_NA_URL}    ${Browser_Type}
    点击搜索按钮
    Wait Until Element Is Visible    xpath=//main[@id="root"]//div/div[1]/div[2]/input    10
    Input Text    xpath=//main[@id="root"]//div/div[1]/div[2]/input    cookies
    Click Element    xpath=//main[@id="root"]//div[1]/button/span[1]
    sleep    3
    Wait Until Element Is Visible    xpath=//main[@id="root"]/div/div[2]//div/ul/li[1]/div/a    10
    ${Search_Result}    Get Text    xpath=//main[@id="root]//div[1]/div/ul/li[1]/div/a
    Set Global Variable    ${Search_Result}
    Click Element    xpath=//main[@id="root"]/div/div[2]//div/ul/li[1]/div/a
    Wait Until Element Is Visible    xpath=//main[@id="root"]//div/div[2]/p    10
    ${Recipt_Title}    Get Text    xpath=//div[@id="root"]//div[1]/h3
    Run Keyword If    "${Recipt_Title}"=="${Search_Result}"    log    搜索结果匹配正常
    ...    ELSE    fail    搜索结果匹配失败
