import logging
import os

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

local_dir_path = os.path.dirname(__file__)

BOT_DATA_DIR = os.path.join(local_dir_path, "data")
BOT_EXTRA_PLUGIN_DIR = os.path.join(local_dir_path, "plugins")
BOT_EXTRA_BACKEND_DIR = os.path.join(local_dir_path, "backends")
BOT_LOG_FILE = os.path.join(local_dir_path, "errbot.log")
BOT_LOG_LEVEL = logging.INFO

BOT_ADMINS = ("@${YOUR_USERNAME}")
BACKEND = "kChat"

BOT_IDENTITY = {
    # Required
    "team": "${YOUR_TEAM_NAME}",
    "server": "${YOUR_TEAM_NAME}.kchat.infomaniak.com",
    "websocket_url": "websocket.kchat.infomaniak.com",
    "token": "${YOUR_BOT_TOKEN}",
}
