*** Settings ***
Library    ImageHorizonLibrary    tests${/}windows${/}reference_images

*** Test Cases ***
Test empty lib initialization
    No operation

Test open application
    Launch application    Calc.exe
    Wait for    calculator active    8
    Press combination    key.alt    key.f4

Test notepad with images
    Type    Key.WIN    notepad    Key.enter    interval=0.1
    Wait for    notepad active
    Type    I love ImageHorizonLibrary    key.enter
    Type with keys down    shift makes me shout    key.shift    pause=0.1    interval=0.05
    Press combination    KEY.CTRL    a
    Copy
    Type    key.Enter
    Press combination    Key.ctrl    V
    Press combination    key.alt    key.F4
    Type    key.right    key.enter


    