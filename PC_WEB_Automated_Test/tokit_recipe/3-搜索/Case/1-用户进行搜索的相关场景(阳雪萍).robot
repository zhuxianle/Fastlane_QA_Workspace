*** Settings ***
Library           Selenium2Library
Resource          ../Element/Elements.robot
Resource          ../Flow/Flow_搜索页面搜索.robot
Resource          ../../Common/Common.robot

*** Test Cases ***
Case_用户下拉选择筛选项进行搜索
    打开浏览器    ${tokit_recipes_na_url}    ${browser_type}
    点击搜索按钮
    等待搜索页面的搜索框可见
    判断筛选项是否存在
    点击搜索页面的筛选项
    筛选项可见后勾选筛选项
    聚焦至搜索按钮的位置
    点击筛选项的搜索按钮
    等待搜索结果列表的搜索数据可见
    点击搜索结果页面的搜索数据
    关闭浏览器

Case_用户输入搜索关键词进行搜索
    打开浏览器    ${tokit_recipes_na_url}    ${browser_type}
    点击搜索按钮
    等待搜索页面的搜索框可见
    输入搜索关键词
    点击搜索页面的搜索按钮
    等待搜索结果列表的搜索数据可见
    点击搜索结果页面的搜索数据
    判断菜谱详情页面的标题是否可见
    关闭浏览器

*** Keywords ***
