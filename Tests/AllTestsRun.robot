*** Settings ***
Documentation    All tests of this suite will be recorded as RECORDING value is set to True
Library    SeleniumLibrary
Library    String

*** Variables ***
${RECORDING}    True
${BROWSER_URL}    www.facebook.com
${user_id}    sample_username
${password}    sample_password
${login_page.login_fail_message}    id: error_box
${login_page.forgot_user}    //div[@id="login_link"]/a[contains(.,"Forgot account?")]
${password_reset_page.account_reset_text}    //h2[@class="uiHeaderTitle"][contains(.,"Find your account")]

*** Test Cases ***
Login_Fail_Message
    [Documentation]  Affirm Incorrect login message
    Open Browser    ${BROWSER_URL}
    Login with user  ${user_id}  ${password}
    Assert Display Of "Login Fail Message" On "Login Page"
    Close All Browsers

Password_Reset_Message
    [Documentation]  Affirm Password Reset message
    Open Browser    ${BROWSER_URL}
    Click "Forgot User" On "Login Page"
    Assert Display Of "Account Reset Text" On "Password Reset Page"
    Close All Browsers

*** Keywords ***

Login with user    ${user_id}    ${password}
    Input text    id: email    ${user_id}
    Input text    id: pass    ${password}
    click element    id: loginbutton

Assert Display Of "${element}" On "${page}"
    ${page}=    Convert To Lower Case    ${page}
    ${element}=    Convert To Lower Case    ${element}
    Replace String    ${page}    ' '    '_'
    Replace String    ${element}    ' '    '_'
    Element Should Be Visible    ${page.${element}}

Click "${element}" On "${page}"
    ${page}=    Convert To Lower Case    ${page}
    ${element}=    Convert To Lower Case    ${element}
    Replace String    ${page}    ' '    '_'
    Replace String    ${element}    ' '    '_'
    Click Element    ${page.${element}}