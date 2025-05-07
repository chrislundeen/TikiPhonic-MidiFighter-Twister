import json
configFile = open('config/config.json')
config = json.load(configFile)
configFile.close()
# print(json.dumps(config))

from helpers.helpers_controllers import buildTwisterController
from helpers.helpers_main import buildTwisterMain

buildTwisterController(config)
buildTwisterMain()

