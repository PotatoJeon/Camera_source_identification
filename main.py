import os
import sys
import pandas
import mp4_parser

def container_classify(target_video):
    if target_video[0:4] == b'RIFF':
        return "avi"
    
    #mp4, mov, 3gp
    elif target_video[4:8] == b'ftyp':
        return "mpeg-4"

    else:
        print("can't support this container")
        return False   

def get_file_size(file_address):
    try:
        size = os.path.getsize(file_address)
        return size
    except FileNotFoundError:
        return None

def file_info(file_addr):
    with open(file_addr, "rb") as file:
        file_size = get_file_size(file_addr)
        video_data = file.read()
    
    return video_data, file_size

path = "D:/졸업논문/iPhone_15_Pro/IMG_5761.mov"

info = file_info(path)
video_data = file_info(path)[0]
file_size = file_info(path)[1]

container = container_classify(video_data[0:8])

if container == "mpeg-4":
    result = mp4_parser.file_analyze(video_data, file_size, path)
    print(result[2]['codec'])
    print(result)

elif container == "avi":
    print("avi")


'''
root_dir = "D:/졸업논문/data_mp4_h26X/"

device_dir = os.listdir(root_dir)

h264_device = []
h264_video_file = []
h264_atom_structure = []
h264_major_brand = []  
h264_compatible_brand = []
h264_vmhd_time_scale = []
h264_parsed_sps = []
h264_parsed_pps = []
h264_hdlr_vide = []
h264_hdlr_soun = []
h264_frame_structure = []
h264_specifited_model = []



for dir in device_dir: #폴더 넘어가는게 이 반복문
    files = os.listdir(f"{root_dir}{dir}/")
    
    #print(files)
    md5 = []
    
    for file in files: #파일 넘어가는게 이 반복문
        path = f"{root_dir}{dir}/{file}"
        print(path)

        info = file_info(path)

        video_data = file_info(path)[0]
        file_size = file_info(path)[1]

        container = container_classify(video_data[0:8])

        if container == "mpeg-4":
            result = mp4_parser.file_analyze(video_data, file_size, path)
            print(result[2]['codec'])
            print(result)

        elif container == "avi":
            print("avi")


#'''
