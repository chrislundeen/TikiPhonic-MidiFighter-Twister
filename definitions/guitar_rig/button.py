from helpers.helpers import setTabs

def buildButton(id, controllerCoordinates, channel, group, controllerType, tags, controller_number, disableFeedback, toggleButton, depth):
    buttonInfo = {
        'tabs': setTabs(depth),
        'buttonId': 'gfx_' + controllerType + str(controller_number),
        'buttonName': controllerType + ' ' + controllerCoordinates,
        'group': group,
        'channel': str(channel),
        'controller_number': str(controller_number),
        'id': str(32 + (controller_number)*3),
        'param': str(controller_number + 1)
    }

    buttonItem = ('{tabs}' '{{' '\n\t{tabs}'
        'id = "{buttonId}",' '\n\t{tabs}'
        'name = "{buttonName}",' '\n\t{tabs}'
        'tags = {{"button",}},' '\n\t{tabs}'
        'source = {{' '\n\t\t{tabs}'
        'kind = "Virtual",' '\n\t\t{tabs}'
        'id = {id},' '\n\t\t{tabs}' # id = 32
        '}},' '\n\t{tabs}'
        'glue = {{' '\n\t\t{tabs}'
        'absolute_mode = "ToggleButton",' '\n\t\t{tabs}'
        'step_size_interval = {{0.01, 0.05}},' '\n\t{tabs}'
        '}},' '\n\t{tabs}'
        'target = {{' '\n\t\t{tabs}'
        'kind = "FxParameterValue",' '\n\t\t{tabs}'
        'parameter = {{' '\n\t\t\t{tabs}'
        'address = "ById",' '\n\t\t\t{tabs}'
        'fx = {{' '\n\t\t\t\t{tabs}'
        'address = "ByName",' '\n\t\t\t\t{tabs}'
        'chain = {{' '\n\t\t\t\t\t{tabs}'
        'address = "Track",' '\n\t\t\t\t\t{tabs}'
        'track = {{' '\n\t\t\t\t\t\t{tabs}'
        'address = "Selected",' '\n\t\t\t\t\t{tabs}'
        '}},' '\n\t\t\t\t{tabs}'
        '}},' '\n\t\t\t\t{tabs}'
        'name = "VST3: Guitar Rig 6 (Native Instruments)",' '\n\t\t\t{tabs}'
        '}},' '\n\t\t\t{tabs}'
        'index = {param},' '\n\t\t{tabs}'
        '}},' '\n\t{tabs}'
        '}},' '\n{tabs}'
        '}},' '\n').format(**buttonInfo)
    return buttonItem