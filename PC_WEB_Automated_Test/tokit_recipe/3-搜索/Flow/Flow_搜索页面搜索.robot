*** Settings ***
Library           Selenium2Library

*** Keywords ***
判断菜谱详情页面的标题是否可见
    ${recipt_title}    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//div[@class="mb-4"]/h3    10
    Run Keyword And Return If    "${recipt_title}"=="PASS"    log    菜谱详情页面的标题可见
    ...    ELSE    fail    菜谱详情页面的标题不可见

输入搜索关键词
    Input Text    xpath=//main[@id="root"]//div/div[1]/div[2]/input    cookies

等待搜索页面的搜索框可见
    Wait Until Element Is Visible    xpath=//main[@id="root"]//div/div[1]/div[2]/input    10

判断筛选项是否存在
    ${filter_function}=    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//span[text()="Filter"]    10
    Run Keyword And Return If    "${filter_function}"=="PASS"    Mouse Over    xpath=//span[text()="Filter"]
    ...    ELSE    log    筛选项无法正常识别，点击失败

点击搜索页面的筛选项
    Click Element    xpath=//span[text()="Filter"]
