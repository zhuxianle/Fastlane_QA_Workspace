*** Settings ***
Library                 Selenium2Library

*** Keywords ***
点击去支付按钮
          [Arguments]          ${upload-checkout1}
          Sleep          2
          Selenium2Library.Capture Page Screenshot          Screenshot2.png
          ${result1}          Image Contrast          ${OUTPUT DIR}/Screenshot2.png          ${CURDIR}\\image_template\\${upload-checkout1}          display_result=True          #${EXECDIR} 根路径 #${CURDIR} 当前目录
          Click Contrasted Image          ${result1[0]}          ${result1[1]}          0          70

进入购买手机页
          Wait Until Element Is Visible          xpath=//main[@id="root"]/div/nav/p/span[1]          10
          Click Element          xpath=//div[@id="shopify-section-collection-template"]/div/div[1]/a/div/img          #点击购买手机页

EU商城-选择第二个商品后获取金额
          [Arguments]          ${Second_Commodity}
          Wait Until Element Is Visible          xpath=//form[@id="purchase-form-without-bundle"]/button          10
          Click Element          xpath=//form[@id="purchase-form-without-bundle"]/label[${Second_Commodity}]          #选择第二个商品
          ${Commodity_Prices}          Get Text          xpath=//form[@id="purchase-form-without-bundle"]/h3/span
          ${Commodity_Prices}          Evaluate          "${Commodity_Prices}".split("€")[1]
          ${Commodity_Prices}          replace string          ${Commodity_Prices}          ,          .
          Set Global Variable          ${Commodity_Prices}

将商品加入购物车
          Click Button          xpath=//form[@id="purchase-form-without-bundle"]/button          #点击进入购物车页面

验证购物车的金额是否正常
          Wait Until Element Is Visible          xpath=//form[@id="purchase-form-without-bundle"]/button          10
          ${Commodity_Prices1}=          Get Text          xpath=//form[@id="purchase-form-without-bundle"]/button          #获取购物车的金额
          ${Commodity_Prices1}=          replace string          ${Commodity_Prices1}          ,          .
          Set Global Variable          ${Commodity_Prices1}
          Run Keyword If          "${Commodity_Prices1}"<="{Total_Amount}"          log          购物车价格跟详情页的价格一致
          ...          ELSE          Fail          购物车价格跟商品详情页价格不一致
          sleep          2

等待登录输入框可见
          Wait Until Element Is Visible          xpath=//input[@id="customer-username"]          10          #等待登录输入框可见

输入用户名以及密码
          Input Text          xpath=//input[@id="customer-username"]          ${User_Email}          #输入用户名
          Input Password          xpath=//input[@id="customer-password"]          ${User_Password}          #输入密码

点击登录按钮
          Click Button          xpath=//form[@id="create_customer"]/div[1]/button          #点击登录按钮

下拉选择保存的地址
          Wait Until Element Is Visible          id=checkout_shipping_address_id          10
          Select From List          id=checkout_shipping_address_id          #下拉选择保存的地址

输入收货地址信息
          Input Text          id=checkout_shipping_address_first_name          ${First_Name}          #输入姓名
          Input Text          id=checkout_shipping_address_last_name          ${Last_Name}          #输入姓氏
          Input Text          id=checkout_shipping_address_address1          ${Shipping_Address}          #输入收货地址
          Input Text          id=checkout_shipping_address_address2          ${Shipping_Address2_field}          #输入详细地址
          Select From List By Index          id=checkout_shipping_address_country          15
          Input Text          id=checkout_shipping_address_zip          ${Postal_Code}          #邮编
          Input Text          id=checkout_shipping_address_city          ${City}          #输入所在城市
          Input Text          id=checkout_shipping_address_phone          ${Tel}          #输入电话号码

点击去购买
          Click Button          id=continue_button          #点击去购买按钮

验证物流选项是否可见
          Wait Until Element Is Visible          xpath=//fieldset[@class="content-box"]/div[1]/div/div          10
          ${Standard1}          Get Text          xpath=//fieldset[@class="content-box"]/div[1]/div/label/span[1]/span[2]
          ${Priority1}          Get Text          xpath=//fieldset[@class="content-box"]/div[2]/div/label/span[1]/span[2]
          Run Keyword If          "${Standard1}"==True and "${Priority1}"==True          log          可正常进行物流选择          Else          fail          #未获取物流选择项

计算商品总金额
          ${Total_Amount}=          Evaluate          ${Commodity_Prices}+${Accessories_Price}          #手机金额+配件金额
          Set Global Variable          ${Total_Amount}

EU商城选择手机配件后获取配件金额
          [Arguments]          ${num}
          Click Element          xpath=//form[@id="purchase-form-without-bundle"]/div/div[1]/div/div/button/i
          ${Accessories_Price}          Get Text          XPATH=//form[@id="purchase-form-without-bundle"]/div/div[${num}]/div/figure/figcaption/p[2]/span
          ${Accessories_Price}          Evaluate          "${Accessories_Price}".split("€")[1]
          ${Accessories_Price}          replace string          ${Accessories_Price}          ,          .
          Set Global Variable          ${Accessories_Price}

UK商城-选择第二个商品后获取金额
          [Arguments]          ${Second_Commodity}
          Wait Until Element Is Visible          xpath=//form[@id="purchase-form-without-bundle"]/button          10
          Click Element          xpath=//form[@id="purchase-form-without-bundle"]/label[${Second_Commodity}]          #选择第二个商品
          ${Commodity_Prices}          Get Text          xpath=//form[@id="purchase-form-without-bundle"]/h3/span
          ${Commodity_Prices}          Evaluate          "${Commodity_Prices}".split("£")[1]
          ${Commodity_Prices}          replace string          ${Commodity_Prices}          ,          .
          Set Global Variable          ${Commodity_Prices}

UK商城选择手机配件后获取配件金额
          [Arguments]          ${num}
          Click Element          xpath=//form[@id="purchase-form-without-bundle"]/div/div[1]/div/div/button/i
          ${Accessories_Price}          Get Text          XPATH=//form[@id="purchase-form-without-bundle"]/div/div[${num}]/div/figure/figcaption/p[2]/span
          ${Accessories_Price}          Evaluate          "${Accessories_Price}".split("£")[1]
          ${Accessories_Price}          replace string          ${Accessories_Price}          ,          .
          Set Global Variable          ${Accessories_Price}
