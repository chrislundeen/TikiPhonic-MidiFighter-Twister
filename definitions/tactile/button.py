from helpers.helpers import setTabs

def buildButton(id, controllerCoordinates, channel, group, controllerType, tags, controller_number, disableFeedback, toggleButton, depth):
    buttonInfo = {
        'tabs': setTabs(depth),
        'buttonId': controllerType + str(controller_number),
        'buttonName': controllerCoordinates + ' ' + controllerType,
        'group': group,
        'channel': str(channel),
        'controller_number': str(controller_number),
        'id': str(id)
    }
    
    # TAGS
    # finalOutput = finalOutput + tabs + 'tags = {' + '\n'
    # for tag in range(len(tags)):
    #    finalOutput = finalOutput + tabs + '\t"' +  tags[tagNum] + '",' + '\n'
    #    tagNum = tagNum + 1
    # finalOutput = finalOutput + tabs + '},' + '\n'
 

    buttonItem = ('{tabs}' '{{' '\n\t{tabs}'
        'id = "{buttonId}",' '\n\t{tabs}'
        'name = "{buttonName}",' '\n\t{tabs}'
        # tags go here
        'group = "{group}",' '\n\t{tabs}'
        # feedback enabled goes here
        'source = {{' '\n\t\t{tabs}'
        'kind = "MidiControlChangeValue",' '\n\t\t{tabs}'
        'channel = {channel},' '\n\t\t{tabs}'
        'controller_number = {controller_number},' '\n\t\t{tabs}'
        #'character = "Button",' '\n\t\t{tabs}'
        'fourteen_bit = false,' '\n\t{tabs}'
        '}},' '\n\t{tabs}'
        'glue = {{' '\n\t\t{tabs}'
        # if toggleButton:
        #'absolute_mode = "ToggleButton",' '\n\t\t{tabs}'
        'step_size_interval = {{0.01, 0.05}},' '\n\t{tabs}'
        'step_factor_interval = {{1, 5}},' '\n\t{tabs}'
        '}},' '\n\t{tabs}'
        'target = {{' '\n\t\t{tabs}'
        'kind = "Virtual",' '\n\t\t{tabs}'
        'id = {id},' '\n\t\t{tabs}'
        #'character = "Button",' '\n\t{tabs}'
        '}},' '\n{tabs}'
        '}},' '\n').format(**buttonInfo)
    return buttonItem