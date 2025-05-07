from helpers.helpers import setTabs

def buildEncoder(id, controllerCoordinates, channel, group, controllerType, tags, controller_number, disableFeedback, depth):
    encoderInfo = {
        'tabs': setTabs(depth),
        'buttonId': 'gfx_' + controllerType + str(controller_number),
        'buttonName': controllerType + ' ' + controllerCoordinates,
        'group': group,
        'channel': str(channel),
        'controller_number': str(controller_number),
        'id': str(32 + (controller_number)*3 + 1),
        'param': str(controller_number + 1)
    }

    #finalOutput = finalOutput + tabs + 'tags = {' + '\n'
    #for tag in range(len(tags)):
    #    finalOutput = finalOutput + tabs + '\t"' +  tags[tagNum] + '",' + '\n'
    #    tagNum = tagNum + 1
    #finalOutput = finalOutput + tabs + '},' + '\n'

    #if disableFeedback:
    #    finalOutput = finalOutput + tabs + 'feedback_enabled = false,' + '\n'

    encoderItem = ('{tabs}' '{{' '\n\t{tabs}'
        'id = "{buttonId}",' '\n\t{tabs}'
        'name = "{buttonName}",' '\n\t{tabs}'
        'tags = {{"button",}},' '\n\t{tabs}'
        'source = {{' '\n\t\t{tabs}'
        'kind = "Virtual",' '\n\t\t{tabs}'
        'id = {id},' '\n\t\t{tabs}' # id = 32
        '}},' '\n\t{tabs}'
        'glue = {{' '\n\t\t{tabs}'
        'step_size_interval = {{0.01, 0.05}},' '\n\t\t{tabs}'
        'step_factor_interval = {{1, 5}},' '\n\t{tabs}'
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
        '}},' '\n').format(**encoderInfo)
    return encoderItem
