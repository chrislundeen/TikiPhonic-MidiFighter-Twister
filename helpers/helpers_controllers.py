import json
import copy
from helpers.merge_utils import deep_merge
from helpers.optimize_deep_copy import optimized_deep_copy_dict, optimized_list_append
from helpers.template_cache import cached_template

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

    # write json output - use with statement for proper resource cleanup
    filename = 'output/_twister_controller.json'

    with open(filename, 'w') as fileHandler:
        json.dump(objController, fileHandler)  # Direct dump without unnecessary string conversion

def buildControllerGroups(config, objController):
    groupNum = 0
    for y in range(len(config['controller']['groups'])):
        group = config['objects']['group']
        group['id'] = 'g' + str(groupNum)
        group['name'] = config['controller']['groups'][y]
        # Use a shallow copy instead of deep copy since group is a simple dictionary with immutable values
        objController['value']['groups'].append({k: v for k, v in group.items()})
        groupNum = groupNum + 1

@cached_template(lambda config, controllerType: f"tactile_{controllerType}")
def getTactileControllerTemplate(config, controllerType):
    baseTemplate = optimized_deep_copy_dict(config['objects']['tactile']['base'])
    controllerTemplate = optimized_deep_copy_dict(config['objects']['tactile'][controllerType])
    return deep_merge(baseTemplate, controllerTemplate)

@cached_template(lambda config, controllerType: f"projection_{controllerType}")
def getProjectionControllerTemplate(config, controllerType):
    baseTemplate = optimized_deep_copy_dict(config['objects']['projection']['base'])
    controllerTemplate = optimized_deep_copy_dict(config['objects']['projection'][controllerType])
    return deep_merge(baseTemplate, controllerTemplate)

def buildControllerMappings(config, objController):
    controller_number = 0
    id = 0
    # Pre-fetch templates once instead of doing it in every loop iteration
    button_template = getTactileControllerTemplate(config, 'button')
    encoder_template = getTactileControllerTemplate(config, 'encoder')
    pushencoder_template = getTactileControllerTemplate(config, 'pushencoder')

    # Create format string template for coordinates once
    coordinate_fmt = '[{}/{}]/[{}]'

    # Enable or disable debug printing
    debug_print = False

    for bankNum in range(1, 5):
        for rowNum in range(1, 5):
            for colNum in range(1, 5):
                # Pre-calculate values used in both control elements
                disableFeedback = False
                toggleButton = True
                controllerCoordinates = f'[{bankNum}/{rowNum}/{colNum}]'

                if (rowNum == 4) and (colNum == 4):
                    toggleButton = False

                # Add button
                button = optimized_deep_copy_dict(button_template)
                button['id'] = f'Button{controller_number}'
                button['name'] = f'{controllerCoordinates} Button'
                button['groupId'] = 'g0'
                button['source']['number'] = controller_number
                button['target']['controlElementIndex'] = id
                objController['value']['mappings'].append(button)
                if debug_print:
                    print(f"{controllerCoordinates} {button['id']} doing ({controller_number}) ({id})")
                id += 1

                # Add rotary encoder
                encoder = optimized_deep_copy_dict(encoder_template)
                encoder['id'] = f'Encoder{controller_number}'
                encoder['name'] = f'{controllerCoordinates} Encoder'
                encoder['groupId'] = 'g1'
                encoder['source']['number'] = controller_number
                encoder['target']['controlElementIndex'] = id
                objController['value']['mappings'].append(encoder)
                if debug_print:
                    print(f"{controllerCoordinates} {encoder['id']} doing ({controller_number}) ({id})")
                id += 1

                # Add push rotary encoder
                pushencoder = optimized_deep_copy_dict(pushencoder_template)
                pushencoder['id'] = f'PushEncoder{controller_number}'
                pushencoder['name'] = f'{controllerCoordinates} Push Encoder'
                pushencoder['groupId'] = 'g2'
                pushencoder['source']['number'] = controller_number
                pushencoder['target']['controlElementIndex'] = id
                objController['value']['mappings'].append(pushencoder)
                if debug_print:
                    print(f"{controllerCoordinates} {pushencoder['id']} doing ({controller_number}) ({id})")
                id += 1

                controller_number += 1

def buildProjectionControls(config, objController):
    controller_number = 0
    id = 0

    # Pre-fetch templates once instead of doing it in every loop iteration
    button_template = getProjectionControllerTemplate(config, 'button')
    encoder_template = getProjectionControllerTemplate(config, 'encoder')
    pushencoder_template = getProjectionControllerTemplate(config, 'pushencoder')

    # Constants used in calculations
    buttonSizeW = 130
    buttonSizeH = 40
    knobSizeW = 80
    knobSizeH = 80

    for bankNum in range(1, 5):
        # Pre-calculate bank-dependent offsets
        bankOffsetX = 1000 if (bankNum % 2) == 0 else 0
        bankOffsetY = 1000 if bankNum > 2 else 0

        for rowNum in range(1, 5):
            rowOffset = rowNum * 220 + bankOffsetY

            for colNum in range(1, 5):
                colOffset = colNum * 220 + bankOffsetX

                # Add Button with optimized deep copy
                button = optimized_deep_copy_dict(button_template)
                button['id'] = f'Button{controller_number}'
                button['x'] = rowOffset
                button['y'] = colOffset
                button['mappings'] = [f'Button{controller_number}']  # Direct assignment instead of append
                objController['value']['customData']['companion']['controls'].append(button)
                id += 1

                # Add Encoder with optimized deep copy
                encoder = optimized_deep_copy_dict(encoder_template)
                encoder['id'] = f'Encoder{controller_number}'
                encoder['x'] = rowOffset
                encoder['y'] = colOffset
                encoder['mappings'] = [f'Encoder{controller_number}']  # Direct assignment instead of append
                objController['value']['customData']['companion']['controls'].append(encoder)
                id += 1

                # Add Push Encoder with optimized deep copy
                pushencoder = optimized_deep_copy_dict(pushencoder_template)
                pushencoder['id'] = f'PushEncoder{controller_number}'
                pushencoder['x'] = rowOffset
                pushencoder['y'] = colOffset
                pushencoder['mappings'] = [f'PushEncoder{controller_number}']  # Direct assignment instead of append
                objController['value']['customData']['companion']['controls'].append(pushencoder)
                id += 1

                controller_number += 1
