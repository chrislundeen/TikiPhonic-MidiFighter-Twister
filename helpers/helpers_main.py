from helpers.helpers import setTabs

# from definitions.projection.button import buildProjectionButton
# from definitions.projection.encoder import buildProjectionEncoder

from definitions.guitar_rig.button import buildButton
from definitions.guitar_rig.encoder import buildEncoder

def buildTwisterMain():
    depth = 0
    filename = 'output/_twister_main.lua'
    print(filename)
    fileHandler = open(filename, 'w')
    fileHandler.write(buildMainShell(depth))
    fileHandler.close()
    print('done')


def buildMainShell(depth):
    shellInfo = {
        'tabs': setTabs(depth),
        #'groups': buildMainGroups(3),
        'mappings': buildMainMappings(3),
        # 'controls': buildMainControls(5),
    }
    shellItem = ('{tabs}' '{{' '\n\t{tabs}'
        'kind = "MainCompartment",' '\n\t{tabs}'
        'version = "2.14.3",' '\n\t{tabs}'
        'value = {{' '\n\t\t{tabs}'
        # 'groups = {{' '\n{tabs}'
        # '{groups}' '\t\t{tabs}'
        # '}},' '\n\t\t{tabs}'
        'mappings = {{' '\n{tabs}'
        '{mappings}' '\t\t{tabs}'
        '}},' '\n\t\t{tabs}'
        #'custom_data = {{' '\n\t\t\t{tabs}'
        #'companion = {{' '\n\t\t\t\t{tabs}'
        #'controls = {{' '\n{tabs}'
        #'{controls}' '\t\t\t\t{tabs}'
        #'}},' '\n\t\t\t{tabs}'
        #'}},' '\n\t\t{tabs}'
        #'}},' '\n\t{tabs}'
        '}},' '\n{tabs}'
        '}}' '\n').format(**shellInfo)
    return shellItem


#def buildMainGroups(depth):
#    finalOutput = ''
#    groupNames = ['Buttons', 'Encoders', 'Push Encoders'] #'Side Buttons'
#    groupNum = 0
#    for y in range(len(groupNames)):
#        groupInfo = {'tabs': setTabs(depth), 'gId': str(groupNum), 'gName': groupNames[groupNum]}
#        groupItem = ('{tabs}' '{{' '\n\t{tabs}'
#            'id = "g{gId}",' '\n\t{tabs}'
#            'name = "{gName}"' '\n{tabs}'
#            '}},' '\n').format(**groupInfo)
#        finalOutput = finalOutput + groupItem
#        groupNum = groupNum + 1
#    return finalOutput

def buildMainMappings(depth):
    # first 3 banks used
    #   bank 1: button and rotary
    #   bank 2: button, rotary, and push rotary
    #   bank 3: button, rotary, and push rotary
    #   bank 4: unused
    finalOutput = ''
    controller_number = 0
    id = 0
    # for bankNum in range(1, 4):
    bankNum = 2
    virtualIndex = 1
    for rowNum in range(1, 5):
        for colNum in range(1, 5):
            disableFeedback = False
            toggleButton = True
            controllerCoordinates = '[' + str(bankNum) + '/' + str(rowNum) + '/' + str(colNum) + ']'

            # button
            finalOutput = finalOutput + buildButton(id, controllerCoordinates, 1, 'g0', 'Button', ['bank' + str(bankNum), 'button'], controller_number, disableFeedback, toggleButton, depth)
            #id = id + 1

            # rotary encoder
            finalOutput = finalOutput + buildEncoder(id, controllerCoordinates, 0, 'g1', 'Encoder', ['bank' + str(bankNum), 'encoder'], controller_number, disableFeedback, depth)
            id = id + 1

            controller_number = controller_number + 1

    return finalOutput

#def buildMainControls(depth):
#    tabs = setTabs(depth)
#    finalOutput = ''
#    controller_number = 0
#    id = 0
#
#    for bankNum in range(1, 4):
#        for rowNum in range(1, 5):
#            for colNum in range(1, 5):
#                buttonSizeW = 130
#                buttonSizeH = 40
#
#                knobSizeW = 80
#                knobSizeH = 80
#
#                bankOffsetX = 0
#                bankOffsetY = 0
#                if (bankNum % 2) == 0:
#                    bankOffsetX = 1000
#                if bankNum > 2:
#                    bankOffsetY = 1000
#                rowOffset = rowNum * 220 + bankOffsetY
#                colOffset = colNum * 220 + bankOffsetX
#
#
#                # need to mirror initial selection
#                # Button
#                finalOutput = finalOutput + buildProjectionButton(id, controller_number, buttonSizeW, buttonSizeH, rowOffset, colOffset, depth)
#                id = id + 1
#
#                # Encoder
#                finalOutput = finalOutput + buildProjectionEncoder(id, 'Encoder', controller_number, knobSizeW, knobSizeH, rowOffset, colOffset, 0, 60, depth)
#                id = id + 1
#
#                if ( (bankNum == 2) or (bankNum == 3) ):
#                    # Push Encoder
#                    finalOutput = finalOutput + buildProjectionEncoder(id, 'PushEncoder', controller_number, knobSizeW, knobSizeH, rowOffset, colOffset, 90, 60, depth)
#                    id = id + 1
#
#                controller_number = controller_number + 1
#
#
#    finalOutput = finalOutput + tabs + 'gridDivisionCount = 5,' + '\n'
#    finalOutput = finalOutput + tabs + 'gridSize = 100,' + '\n'
#
#    return finalOutput

