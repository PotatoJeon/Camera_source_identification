import os
import data_decoder

def get_file_size(file_address):
    try:
        size = os.path.getsize(file_address)
        return size
    except FileNotFoundError:
        return None
    

def list_name_and_size(avi_file, start_offset):
    list_size = int(avi_file[start_offset+4:start_offset+8].hex(),16)
    list_name = avi_file[start_offset+8:start_offset+12]
    list_name = data_decoder.decode(list_name)

    return(list_name, list_size)

def parse_riff(avi_file):
    return 0


def find_child_list(avi_file, start_offset, size):
    riff = list_name_and_size(avi_file, 0)



file_addr = "D:/졸업논문/illegal_camera_dataset/GeneralPlus/V8 Pen/MOV00004.AVI"
with open(file_addr, "rb") as file:
    file_size = get_file_size(file_addr)
    video_data = file.read()

a =  list_name_and_size(video_data, 0)

print(a)