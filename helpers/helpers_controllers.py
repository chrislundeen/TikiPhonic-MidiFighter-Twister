import json
import copy
from helpers.merge_utils import deep_merge

from helpers.helpers import setTabs

from definitions.projection.button import buildProjectionButton
from definitions.projection.encoder import buildProjectionEncoder

from definitions.tactile.button import buildButton
from definitions.tactile.encoder import buildEncoder

def buildTwisterController(config):

    # json -----------------------------
    objController = config['objects']['controller']
    objController['version'] = config['controller']['version']

    # add groups
    buildControllerGroups(config, objController)

    # add mappings
    buildControllerMappings(config, objController)

    # add projection controls
    buildProjectionControls(config, objController)

    # write json output
    filename = 'output/_twister_controller.json'

    fileHandler = open(filename, 'w')
    fileHandler.write(json.dumps(objController))
    fileHandler.close()

def buildControllerGroups(config, objController):
    groupNum = 0
    for y in range(len(config['controller']['groups'])):
        group = config['objects']['group']
        group['id'] = 'g' + str(groupNum)
        group['name'] = config['controller']['groups'][y]
        objController['value']['groups'].append(copy.deepcopy(group))
        groupNum = groupNum + 1

def getTactileControllerTemplate(config, controllerType):
    baseTemplate = copy.deepcopy(config['objects']['tactile']['base'])
    controllerTemplate = copy.deepcopy(config['objects']['tactile'][controllerType])
    return deep_merge(baseTemplate, controllerTemplate)

def getProjectionControllerTemplate(config, controllerType):
    baseTemplate = copy.deepcopy(config['objects']['projection']['base'])
    controllerTemplate = copy.deepcopy(config['objects']['projection'][controllerType])
    return deep_merge(baseTemplate, controllerTemplate)

def buildControllerMappings(config, objController):
    controller_number = 0
    id = 0
    for bankNum in range(1, 5):
        for rowNum in range(1, 5):
            for colNum in range(1, 5):
                disableFeedback = False
                toggleButton = True
                controllerCoordinates = '[' + str(bankNum) + '/' + str(rowNum) + '/' + str(colNum) + ']'

                if ( (rowNum == 4) and (colNum == 4) ):
                    # print(controllerCoordinates)
                    # disableFeedback = True
                    toggleButton = False

                # button
                controlElement = getTactileControllerTemplate(config, 'button')
                controlElement['id'] = 'Button' + str(controller_number)
                controlElement['name'] = controllerCoordinates + ' Button'
                controlElement['groupId'] = 'g0'
                controlElement['source']['number'] = controller_number
                controlElement['target']['controlElementIndex'] = id
                objController['value']['mappings'].append(copy.deepcopy(controlElement))
                print(controllerCoordinates + ' ' + controlElement['id'] + ' doing ('+str(controller_number)+') ('+str(id)+')')
                id = id + 1

                # rotary encoder
                controlElement = getTactileControllerTemplate(config, 'encoder')
                controlElement['id'] = 'Encoder' + str(controller_number)
                controlElement['name'] = controllerCoordinates + ' Encoder'
                controlElement['groupId'] = 'g1'
                controlElement['source']['number'] = controller_number
                controlElement['target']['controlElementIndex'] = id
                objController['value']['mappings'].append(copy.deepcopy(controlElement))
                print(controllerCoordinates + ' ' + controlElement['id'] + ' doing ('+str(controller_number)+') ('+str(id)+')')
                id = id + 1

                # push rotary encoder
                controlElement = getTactileControllerTemplate(config, 'pushencoder')
                controlElement['id'] = 'PushEncoder' + str(controller_number)
                controlElement['name'] = controllerCoordinates + ' Push Encoder'
                controlElement['groupId'] = 'g2'
                controlElement['source']['number'] = controller_number
                controlElement['target']['controlElementIndex'] = id
                objController['value']['mappings'].append(copy.deepcopy(controlElement))
                print(controllerCoordinates + ' ' + controlElement['id'] + ' doing ('+str(controller_number)+') ('+str(id)+')')
                id = id + 1

                controller_number = controller_number + 1


def buildProjectionControls(config, objController):
    controller_number = 0
    id = 0

    for bankNum in range(1, 5):
        for rowNum in range(1, 5):
            for colNum in range(1, 5):
                buttonSizeW = 130
                buttonSizeH = 40

                knobSizeW = 80
                knobSizeH = 80

                bankOffsetX = 0
                bankOffsetY = 0
                if (bankNum % 2) == 0:
                    bankOffsetX = 1000
                if bankNum > 2:
                    bankOffsetY = 1000
                rowOffset = rowNum * 220 + bankOffsetY
                colOffset = colNum * 220 + bankOffsetX

                # Button
                projectionElement = getProjectionControllerTemplate(config, 'button')
                projectionElement['id'] = 'Button' + str(controller_number)
                projectionElement['x'] = rowOffset
                projectionElement['y'] =  colOffset
                projectionElement['mappings'].append('Button' + str(controller_number))
                objController['value']['customData']['companion']['controls'].append(copy.deepcopy(projectionElement))
                id = id + 1

                # Encoder
                projectionElement = getProjectionControllerTemplate(config, 'encoder')
                projectionElement['id'] = 'Encoder' + str(controller_number)
                projectionElement['x'] = rowOffset
                projectionElement['y'] =  colOffset
                projectionElement['mappings'].append('Encoder' + str(controller_number))
                objController['value']['customData']['companion']['controls'].append(copy.deepcopy(projectionElement))
                id = id + 1

                # Push Encoder
                projectionElement = getProjectionControllerTemplate(config, 'pushencoder')
                projectionElement['id'] = 'PushEncoder' + str(controller_number)
                projectionElement['x'] = rowOffset
                projectionElement['y'] =  colOffset
                projectionElement['mappings'].append('PushEncoder' + str(controller_number))
                objController['value']['customData']['companion']['controls'].append(copy.deepcopy(projectionElement))
                id = id + 1

                controller_number = controller_number + 1
