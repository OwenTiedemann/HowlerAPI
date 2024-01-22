import json
import os

import requests
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import json_util
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_CLIENT= os.getenv('MONGO_CLIENT')

client = MongoClient(MONGO_CLIENT)

custom_commands_collection = client['commands']['custom']


@app.route('/image_commands', methods=['GET'])
def get_image_commands():
    commands = custom_commands_collection.find()
    image_commands = []
    for command in commands:
        if 'image_url' in command:
            image_commands.append(command)

    return json.loads(json_util.dumps(image_commands))

@app.route('/text_commands', methods=['GET'])
def get_text_commands():
    commands = custom_commands_collection.find()
    text_commands = []
    for command in commands:
        if 'image_url' not in command:
            text_commands.append(command)

    return json.loads(json_util.dumps(text_commands))

@app.route('/utils/roles', methods=['GET'])
async def get_roles_information():
    roles = request.args.getlist('roles[]')

    url = "https://discord.com/api/guilds/" + str(360903377216864267) + "/roles"

    payload = ""
    headers = {
        "Authorization": "Bot " + DISCORD_TOKEN
    }

    response = requests.request("GET", url, headers=headers)

    guild_roles = []

    for guild_role in response.json():
        for user_role in roles:
            if guild_role['id'] == user_role:
                guild_roles.append(guild_role)
                break

    return jsonify(guild_roles)
