*** Settings ***
Library    ImageHorizonLibrary    ${CURDIR}${/}reference_images${/}calculator    screenshot_folder=${OUTPUT_DIR}

*** Test cases ***

Calculator
    Set Confidence      0.9
    Launch application    python tests/atest/calculator/calculator.py
    ${location1}=    Wait for    failme     timeout=30
    Click to the above of     ${location1}    20
    Type    1010
    Click to the below of     ${location1}    20
    Type    1001
    ${location2}=    Locate    or_button.png
    Click to the below of     ${location2}    0
    Click to the below of     ${location2}    50
    ${result}=    Copy
    Should be equal as integers    ${result}    1011
    Click Image     close_button.png
    [Teardown]    Terminate application
