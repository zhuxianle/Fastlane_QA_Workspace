*** Keywords ***
点击去支付按钮
          [Arguments]          ${upload-checkout1}
          Sleep          1
          Selenium2Library.Capture Page Screenshot          Screenshot1.png
          ${result1}          Image Contrast          ${OUTPUT DIR}/Screenshot1.png          ${CURDIR}\\image_template\\${upload-checkout1}          display_result=True
          Click Contrasted Image          ${result1[0]}          ${result1[1]}          0          70

进入购买手机页
          Wait Until Element Is Visible          xpath=//main[@id="root"]/div/nav/p/span[1]          10
          Click Element          xpath=//div[@id="shopify-section-collection-template"]/div/div[1]/a/div/img          #点击购买手机页

EU商城-选择第二个商品后获取金额
          Wait Until Element Is Visible          xpath=//form[@id="purchase-form-without-bundle"]/button          10
          Click Element          xpath=//form[@id="purchase-form-without-bundle"]/label[2]          #选择第二个商品

将商品加入购物车
          ${Commodity_Prices}          Get Text          xpath=//form[@id="purchase-form-without-bundle"]/h3/span
          Set Global Variable          ${Commodity_Prices}
          Click Button          xpath=//form[@id="purchase-form-without-bundle"]/button          #点击进入购物车页面

验证购物车的金额是否正常
          Wait Until Element Is Visible          xpath=//main[@id="root"]/section/div/form/table/tfoot/tr[4]/td/p/span[2]          10
          ${Commodity_Prices1}=          Get Text          xpath=//main[@id="root"]/section/div/form/table/tfoot/tr[4]/td/p/span[2]          #获取购物车的金额
          Run Keyword If          "${Commodity_Prices1}"=="${Commodity_Prices}"          点击去支付按钮          Tmp_Checkout.png
          ...          ELSE          Fail          购物车价格跟商品详情页价格不一致

等待登录输入框可见
          Wait Until Element Is Visible          xpath=//input[@id="customer-username"]          10          #等待登录输入框可见

输入用户名以及密码
          Input Text          xpath=//input[@id="customer-username"]          ${User_Email}          #输入用户名
          Input Password          xpath=//input[@id="customer-password"]          ${User_Password}          #输入密码

点击登录按钮
          Click Button          xpath=//form[@id="create_customer"]/div[1]/button          #点击登录按钮

下拉选择保存的地址
          Wait Until Element Is Visible          id=checkout_shipping_address_id          10
          Select From List          id=checkout_shipping_address_id          Add address          #下拉选择保存的地址

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
          Wait Until Element Is Visible          xpath=//div[@class="content"]/div/div[1]/div[2]/div/form/div[1]/div[1]/div/div/div[2]/div[1]/div[2]/address          10
          ${Standard}          Get Text          xpath=//div[@class="content"]/div/div[1]/div[2]/div/form/div[1]/div[2]/div[2]/fieldset/div[1]/div/label/span[2]/span
          ${Priority}          Get Text          xpath=//div[@class="content"]/div/div[1]/div[2]/div/form/div[1]/div[2]/div[2]/fieldset/div[2]/div/label/span[2]/span
          Run Keyword If          "${Standard}"==True and "${Priority}"==True          log          可正常进行物流选择          Else          fail          #未获取物流选择项
