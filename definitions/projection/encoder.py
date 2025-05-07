from helpers.helpers import setTabs

def buildProjectionEncoder(
        id,
        encoder_type,
        controller_number, 
        knobSizeW, 
        knobSizeH, 
        rowOffset, 
        colOffset, 
        xOffset, 
        yOffset, 
        depth):
    encoderInfo = {
        'tabs': setTabs(depth),
        'encoder_type': str(encoder_type),
        'controller_number': str(controller_number),
        'knobSizeW': str(knobSizeW),
        'knobSizeH': str(knobSizeH),
        'rowOffset': str(rowOffset),
        'colOffset': str(colOffset),
        'xOffset': str(xOffset),
        'yOffset': str(yOffset),
    }

    encoderItem = ('{tabs}' '{{' '\n\t{tabs}'
        'height = {knobSizeH},' '\n\t{tabs}'
        'id = "{encoder_type}{controller_number}",' '\n\t{tabs}'
        'labelOne = {{' + '\n\t\t{tabs}'
        'angle = 0,' + '\n\t\t{tabs}'
        'position = "aboveTop",' + '\n\t\t{tabs}'
        'sizeConstrained = true,' + '\n\t{tabs}'
        '}},' + '\n\t{tabs}'
        'mappings = {{' + '\n\t\t{tabs}'
        '"{encoder_type}' + str(controller_number) + '",' + '\n\t{tabs}'
        '}},' + '\n\t{tabs}'
        'shape = "circle",' + '\n\t{tabs}'
        'width = ' + str(knobSizeW) + ',' + '\n\t{tabs}'
        'x = ' + str(colOffset + xOffset) + ',' + '\n\t{tabs}'
        'y = ' + str(rowOffset + yOffset) + ',' + '\n{tabs}'

        '}},' '\n').format(**encoderInfo)
    return encoderItem