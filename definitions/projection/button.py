from helpers.helpers import setTabs

def buildProjectionButton(
        id,
        controller_number, 
        buttonSizeW,
        buttonSizeH, 
        rowOffset, 
        colOffset, 
        depth):
    buttonInfo = {
        'tabs': setTabs(depth),
        'controller_number': str(controller_number),
        'buttonSizeW': str(buttonSizeW),
        'buttonSizeH': str(buttonSizeH),
        'rowOffset': str(rowOffset),
        'colOffset': str(colOffset),
    }

    buttonItem = ('{tabs}' '{{' '\n\t{tabs}'
        'height = {buttonSizeH},' '\n\t{tabs}'
        'id = "Button{controller_number}",' '\n\t{tabs}'
        'labelOne = {{' + '\n\t\t{tabs}'
        'angle = 0,' + '\n\t\t{tabs}'
        'position = "aboveTop",' + '\n\t\t{tabs}'
        'sizeConstrained = true,' + '\n\t{tabs}'
        '}},' + '\n\t{tabs}'
        'mappings = {{' + '\n\t\t{tabs}'
        '"Button' + str(controller_number) + '",' + '\n\t{tabs}'
        '}},' + '\n\t{tabs}'
        'shape = "rectangle",' + '\n\t{tabs}'
        'width = ' + str(buttonSizeW) + ',' + '\n\t{tabs}'
        'x = ' + str(colOffset + 20) + ',' + '\n\t{tabs}'
        'y = ' + str(rowOffset) + ',' + '\n{tabs}'

        '}},' '\n').format(**buttonInfo)
    return buttonItem