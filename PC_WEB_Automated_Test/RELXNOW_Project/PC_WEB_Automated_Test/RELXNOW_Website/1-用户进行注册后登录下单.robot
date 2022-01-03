*** Settings ***
Library                 Selenium2Library
Resource                L2_Components.robot

*** Variables ***
${User_Email}           pndtedddddg6z@huweimail.cn          #输入用户的登录邮箱
${User_Password}          oyxp13048864661          #输入用户密码
${First_name}           Daisy          #输入用户的姓名
${Last_name}            Yang          #输入用户的姓氏

*** Test Cases ***
Case1_用户进行注册
          Open Browser          ${RELXNOW_URL}
          Wait Until Element Is Visible          xpath=//div[@class="d-flex flex-column mt-5"]/button          10
          Click Button          xpath=//div[@class="d-flex flex-column mt-5"]/button
          Wait Until Element Is Visible          xpath=//div[@id="as-navbar-topbar"]/nav/div/ul/li[2]/a/span          10
          Click Element          xpath=//div[@id="as-navbar-topbar"]/nav/div/ul/li[2]/a/span
          ${C_Account_registration}=          Set Variable          Create Account          #创建临时的变量定义
          Set Global Variable          ${C_Account_registration}
          Wait Until Element Is Visible          xpath=//a[text()="${C_Account_registration}"]          10
          Click Element          xpath=//a[text()="${C_Account_registration}"]
          Comment          ${C_Account_registration1}=          Run Keyword And Return Status          Get Text          xpath=//a[@id="as-signin-signup-modal"]/div/div/div[2]/div[1]/div[2]/a[1]
          Comment          Run Keyword If          "${C_Account_registration1}"=="${C_Account_registration}"          点击注册按钮          ${C_Account_registration}          Else          fail
          Wait Until Element Is Visible          xpath=//form[@class="as-signup-form"]/div[1]/input          10
          ${U_Register_Email}          Set Variable          Daisy_Yang
          ${time1}          Evaluate          datetime.datetime.now().strftime('%H%M%S')
          ${U_Register_Email}          Set Variable          ${U_Register_Email}${time1}
          Input Text          xpath=//form[@class="as-signup-form"]/div[1]/input          ${U_Register_Email}          #输入用户的注册邮箱
          Input Text          xpath=//form[@class="as-signup-form"]/div[2]/input          ${User_Password}          #输入用户的注册密码
          Input Text          xpath=//form[@class="as-signup-form"]/div[3]/input          ${First_name}          #输入用户的姓名
          Input Text          xpath=//form[@class="as-signup-form"]/div[4]/input          ${Last_name}          #输入用户的姓氏
          ${C_Account_registration2}=          Run Keyword And Return Status          Wait Until Element Is Visible          xpath=//button[text()="${C_Account_registration}"]
          Run Keyword If          "${C_Account_registration2}"=="${C_Account_registration}"          Click Element          xpath=//button[text()="${C_Account_registration}"]          Else          log          未找到注册按钮无法注册
          [Teardown]          Run Keyword If          '${PREV TEST STATUS}'=='FAIL'          fail          Run Keywords          Import Library          OperatingSystem
          ...          AND          OperatingSystem.run          taskkill /F /IM WerFault.exe

Case2_用户进行登录
          Open Browser          ${RELXNOW_URL}
          Wait Until Element Is Visible          xpath=//div[@id="as-navbar-topbar"]/nav/div/ul/li[2]/a/span          10
          Click Element          xpath=//div[@id="as-navbar-topbar"]/nav/div/ul/li[2]/a/span
          Wait Until Element Is Visible          xpath=//a[@id="as-signin-signup-modal"]/div/div/div[2]/div[1]/form/div[1]/input          10          #等待登录框的输入框可见
          Input Password          ${User_Email}          xpath=//a[@id="as-signin-signup-modal"]/div/div/div[2]/div[1]/form/div[1]/input          #用户登录框输入用户邮箱
          Input Password          ${User_Password}          xpath=//a[@id="as-signin-signup-modal"]/div/div/div[2]/div[1]/form/div[2]/input          #用户登录框输入用户密码
          Click Button          xpath=//a[@id="as-signin-signup-modal"]/div/div/div[2]/div[1]/form/button          #点击登录按钮

*** Keywords ***
点击注册按钮
          [Arguments]          ${C_Account_registration}
          Mouse Over          xpath=//a[@id="as-signin-signup-modal"]/div/div/div[2]/div[1]/div[2]/a[1]
          Click Element          xpath=//a[text()="${C_Account_registration}"]
