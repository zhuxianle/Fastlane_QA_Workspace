*** Variables ***
${Buyer_EU_URL}          https://eu.redmagic.gg/          #进入EU商城
${Buyer_UK_URL}          https://uk.redmagic.gg          #进入UK商城页面

*** Keywords ***
点击Home首页
          Click Element          xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[4]/a[1]
          进入Phone页面

进入Phone页面
          Click Element          xpath=//div[@id="shopify-section-header]/header/div/nav/ul/li[4]/div/div[1]/span

进入首页的导航栏页
          [Arguments]          ${num}
          [Documentation]          /*
          ...          1、STORE 为菜单三的选项，表示选中了store,输入值为2
          ...          2、SUOPPORT 为菜单四的选项，表示选中了SUOPPORT，输入值为3
          ...          3、NEWS 为菜单五的选项，表示选中了news，输入值为4
          ...          4、ABOUT为菜单六的选项，表示选中了about，输入值为5
          ...          */
          Wait Until Element Is Visible          xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[4]/a[1]          10
          Click Element          xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[4]/a[${num}]
