*** Settings ***
Library    ImageHorizonLibrary    ${CURDIR}${/}reference_images${/}win    screenshot_folder=${TEMPDIR}
Force Tags    windows

*** Test Cases ***
Test open application
    Launch application    Calc.exe
    Wait for    calculator active    8
    Press combination    key.alt    key.f4
    [Teardown]    Terminate application

Test notepad with images
    Type    Key.WIN    notepad    Key.enter    interval=0.1
    Wait for    notepad active
    Type    I love ImageHorizonLibrary    key.enter
    Type with keys down    shift makes me shout    key.shift
    ...                    pause=0.1    interval=0.05
    Press combination    KEY.CTRL    a
    ${retval}=   Copy
    Should be equal as strings    ${retval}
    ...                           I love ImageHorizonLibrary\nSHIFT MAKES ME SHOUT
    Type    key.Enter
    Press combination    Key.ctrl    V
    Press combination    key.alt    key.F4
    Type    key.right    key.enter
