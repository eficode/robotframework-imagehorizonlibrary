*** Settings ***
Library    ImageHorizonLibrary    ${CURDIR}${/}reference_images${/}linux    screenshot_folder=${TEMPDIR}
Force Tags    linux

*** Test cases ***

Calculator
    Launch application    gnome-calculator
    ${location}=    Wait for    calculator
    Click to the above of     ${location}    50
    Type    5
    Click image    button plus
    Type     5
    Click image    button equals
    Press combination    key.ALT    key.A
    ${result}=    Copy
    Should be equal as integers    ${result}    10
    [Teardown]    Terminate application
