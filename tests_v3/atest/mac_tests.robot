*** Settings ***
Library    ImageHorizonLibrary    ${CURDIR}${/}reference_images${/}mac
Force Tags    mac

*** Test Cases ***
Test empty lib initialization
    No operation

Test open and close application
    ${alias1}=    Launch application    open -a /Applications/Calculator.app
    Wait for    calculator_active
    Terminate application    ${alias1}
    Launch application    open -a Calculator     alias=My calculator
    Wait for    calculator_active
    Terminate application    My calculator
    Launch application    open -a Calculator.app
    Wait for    calculator_active
    Terminate application

Test folder as reference image
    Launch application    open -a Calculator     alias=My calculator
    Wait for    folder_calculator_active
    Terminate application    My calculator

Test calculator
    Launch application    open -a Calculator
    Wait for    calculator active
    Clear calculator
    ${button_5_pos}=    Click image    button 5
    Click image    button plus
    Move to    ${button_5_pos}
    Click
    Click image    button equals
    Wait for    result 10
    press combination    key.command    q

Test click to directions
    Launch application    open -a Calculator
    Wait for    calculator active
    Clear calculator
    ${button_5_pos}=    locate    button 5
    Click to the left of    ${button_5_pos}    56     clicks=2    button=left
    ...    interval=0.0
    Click to the above of    ${button_5_pos}    56     clicks=2    button=left
    ...    interval=0.0
    Click to the right of    ${button_5_pos}    56     clicks=2    button=left
    ...    interval=0.0
    Click to the below of    ${button_5_pos}    56     clicks=2    button=left
    ...    interval=0.0
    Wait for    result 44886622
    Terminate application

*** Keywords ***
Clear calculator
    Type    c

