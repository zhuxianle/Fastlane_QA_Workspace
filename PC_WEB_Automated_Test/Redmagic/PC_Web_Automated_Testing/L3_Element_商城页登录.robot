*** Keywords ***
点击进入登录页
          Wait Until Element Is Visible          xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[5]/a[1]          15
          Click Element          xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[5]/a[1]          #点击进入登录页

登录页输入用户名
          Wait Until Element Is Visible          id=customer-username          10          #等待登录输入框可见
          Input Text          id=customer-username          ${User_Email}          #输入用户名

登录页输入密码
          Input Password          id=customer-password          ${User_Password}          #输入密码

登录页点击登录按钮
          Click Button          xpath=//form[@id="create_customer"]/div[1]/button          #点击登录按钮

点击进入个人中心
          Sleep          3
          Wait Until Element Is Visible          xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[5]/a[1]          10
          Click Element          xpath=//div[@id="shopify-section-header"]/header/div/nav/ul/li[5]/a[1]
          Wait Until Element Is Visible          xpath=//div[@id="shopify-section-account-sidebar"]/div/h3/span          10          #等待个人中心的用户昵称可见

判断用户是否登录正常
          ${a}          Set Variable          daisy          #设置临时变量的用户昵称
          ${User_Name}          Run Keyword And Return Status          Page Should Contain Element          xpath=//main[@id="root"]/div[2]/div/section/div/p[1]/span[text()="${a}"]          10          #判断界面是否存在用户账号
          Run Keyword If          "${User_Name}"==True          log          用户登录成功          Else          FAIL          用户登录失败
