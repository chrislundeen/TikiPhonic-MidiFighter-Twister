from helpers.helpers import setTabs

def buildEncoder(id, controllerCoordinates, channel, group, controllerType, tags, controller_number, disableFeedback, depth):
    encoderInfo = {
        'tabs': setTabs(depth),
        'encoderId': controllerType + str(controller_number),
        'encoderName': controllerCoordinates + ' ' + controllerType,
        'group': group,
        'channel': str(channel),
        'controller_number': str(controller_number),
        'id': str(id)
    }

    #finalOutput = finalOutput + tabs + 'tags = {' + '\n'
    #for tag in range(len(tags)):
    #    finalOutput = finalOutput + tabs + '\t"' +  tags[tagNum] + '",' + '\n'
    #    tagNum = tagNum + 1
    #finalOutput = finalOutput + tabs + '},' + '\n'

    #if disableFeedback:
    #    finalOutput = finalOutput + tabs + 'feedback_enabled = false,' + '\n'

    encoderItem = ('{tabs}' '{{' '\n\t{tabs}'
        'id = "{encoderId}",' '\n\t{tabs}'
        'name = "{encoderName}",' '\n\t{tabs}'
        # tags go here
        'group = "{group}",' '\n\t{tabs}'
        # feedback enabled goes here
        'source = {{' '\n\t\t{tabs}'
        'kind = "MidiControlChangeValue",' '\n\t\t{tabs}'
        'channel = {channel},' '\n\t\t{tabs}'
        'controller_number = {controller_number},' '\n\t{tabs}'
        '}},' '\n\t{tabs}'
        'glue = {{' '\n\t\t{tabs}'
        'absolute_mode = "MakeRelative",' '\n\t\t{tabs}'
        'step_size_interval = {{0.01, 0.05}},' '\n\t{tabs}'
        '}},' '\n\t{tabs}'
        'target = {{' '\n\t\t{tabs}'
        'kind = "Virtual",' '\n\t\t{tabs}'
        'id = {id},' '\n\t{tabs}'
        '}},' '\n{tabs}'
        '}},' '\n').format(**encoderInfo)
    return encoderItem
