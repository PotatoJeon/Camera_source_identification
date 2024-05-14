import os
import pandas as pd
import get_exif_info
import data_decoder
import mdat_analyze
import json

video_attribute = {} #영상 재생 관련 정보 저장 딕셔너리
meta_attribute ={}  #영상 메타데이터 관련 정보 저장 딕셔너리
udta = {} #udta 박스 내 자식박스 목록 저장 딕셔너리
uuid = {} #uuid 박스 내 자식박스 목록 저장 딕셔너리


#ftyp 박스를 파싱하는 함수 - 사용 중
def parse_ftyp(mp4_file, current_box):
    major_brand=mp4_file[current_box[1]+8:current_box[1]+12]
    major_brand = data_decoder.decode(major_brand)
    minor_version=int(mp4_file[current_box[1]+12:current_box[1]+16].hex(), 16)
    comapatible_brand=mp4_file[current_box[1]+16:current_box[1]+current_box[2]]
    comapatible_brand= data_decoder.decode(comapatible_brand)
    video_attribute['ftyp_major_brand'] = major_brand
    video_attribute['ftyp_compatible_brand'] = comapatible_brand
    return {}

#mvhd 박스를 파싱하는 함수 - 사용 안함
def parse_mvhd(mp4_file, current_box):
    mvhd_data = mp4_file[current_box[1]+8:current_box[1]+current_box[2]]
    mvhd_info = {
        'Version': mvhd_data[0],
        'Flag' : mvhd_data[1:4],
        #'Creation_Time' : int.from_bytes(mvhd_data[4:8], byteorder='big'),
        #'Modification_Time' : int.from_bytes(mvhd_data[8:12], byteorder='big'),
        'Time_Scale' : int.from_bytes(mvhd_data[12:16], byteorder='big'),
        #'Duration' : int.from_bytes(mvhd_data[16:20], byteorder='big'),
        'Prefered_Rate' : int.from_bytes(mvhd_data[20:24], byteorder='big'),
        'Prefered_Volume' : int.from_bytes(mvhd_data[24:26], byteorder='big'),
        'Reserved_0' : mvhd_data[26],
        'Reserved_1' : mvhd_data[27],
        'Reserved_2' : mvhd_data[28],
        'Reserved_3' : mvhd_data[29],
        'Reserved_4' : mvhd_data[30],
        'Reserved_5' : mvhd_data[31],
        'Reserved_6' : mvhd_data[32],
        'Reserved_7' : mvhd_data[33],
        'Reserved_8' : mvhd_data[34],
        'Reserved_9' : mvhd_data[35],
        'Matrix_A' : int.from_bytes(mvhd_data[36:40], byteorder='big'),
        'Matrix_B' : int.from_bytes(mvhd_data[40:44], byteorder='big'),
        'Matrix_U' : int.from_bytes(mvhd_data[44:48], byteorder='big'),
        'Matrix_C' : int.from_bytes(mvhd_data[48:52], byteorder='big'),
        'Matrix_D' : int.from_bytes(mvhd_data[52:56], byteorder='big'),
        'Matrix_V' : int.from_bytes(mvhd_data[56:60], byteorder='big'),
        'Matrix_X' : int.from_bytes(mvhd_data[60:64], byteorder='big'),
        'Matrix_Y' : int.from_bytes(mvhd_data[64:68], byteorder='big'),
        'Matrix_W' : int.from_bytes(mvhd_data[68:72], byteorder='big'),
        'Preview_Time' : int.from_bytes(mvhd_data[72:76], byteorder='big'),
        'Preview_Duration' :int.from_bytes(mvhd_data[76:80], byteorder='big'),
        'Poster_Time' : int.from_bytes(mvhd_data[80:84], byteorder='big'),
        'Selection_Time' : int.from_bytes(mvhd_data[84:88], byteorder='big'),
        'Selection_Duration' : int.from_bytes(mvhd_data[88:92], byteorder='big'),
        'Current_Time' : int.from_bytes(mvhd_data[92:96], byteorder='big'),
        'Next_Track_Id' :int.from_bytes(mvhd_data[96:100], byteorder='big')
    }

    #print(mvhd_info)
    video_attribute['mvhd_time_scale'] = mvhd_info['Time_Scale']
    video_attribute['mvhd_next_track_ID'] = mvhd_info['Next_Track_Id']
    return {}

#tkhd 박스를 파싱하는 함수 - 사용 안함
def parse_tkhd(mp4_file, current_box):

    tkhd_data = mp4_file[current_box[1]+8:current_box[1]+current_box[2]]  # 92 바이트는 'tkhd' 상자의 크기로 가정합니다.
    tkhd_info = {
        'Version': tkhd_data[0],
        #'Dummy': tkhd_data[1:4],
        #'Creation_Time': int.from_bytes(tkhd_data[4:8], byteorder='big'),
        #'Modification_Time': int.from_bytes(tkhd_data[8:12], byteorder='big'),
        'Track_Id': int.from_bytes(tkhd_data[12:16], byteorder='big'),
        'Reserved_1': int.from_bytes(tkhd_data[16:20], byteorder='big'),
        #'Duration': int.from_bytes(tkhd_data[20:24], byteorder='big'),
        'Reserved_2': int.from_bytes(tkhd_data[24:32], byteorder='big'),
        'Layer': int.from_bytes(tkhd_data[32:34], byteorder='big'),
        'Alternated_Group': int.from_bytes(tkhd_data[34:36], byteorder='big'),
        'Volume': int.from_bytes(tkhd_data[36:38], byteorder='big'),
        'Reserved_3': int.from_bytes(tkhd_data[38:40], byteorder='big'),
        'Matrix_A': int.from_bytes(tkhd_data[40:44], byteorder='big'),
        'Matrix_B': int.from_bytes(tkhd_data[44:48], byteorder='big'),
        'Matrix_U': int.from_bytes(tkhd_data[48:52], byteorder='big'),
        'Matrix_C': int.from_bytes(tkhd_data[52:56], byteorder='big'),
        'Matrix_D': int.from_bytes(tkhd_data[56:60], byteorder='big'),
        'Matrix_V': int.from_bytes(tkhd_data[60:64], byteorder='big'),
        'Matrix_X': int.from_bytes(tkhd_data[64:68], byteorder='big'),
        'Matrix_Y': int.from_bytes(tkhd_data[68:72], byteorder='big'),
        'Matrix_W': int.from_bytes(tkhd_data[72:76], byteorder='big'),
        'Track_Width': int.from_bytes(tkhd_data[76:80], byteorder='big'),
        'Track_Height': int.from_bytes(tkhd_data[80:84], byteorder='big')
    }

    return tkhd_info

#mdhd 박스를 파싱하는 함수 - 사용 안함
def parse_mdhd(mp4_file, current_box):
    mdhd_data = mp4_file[current_box[1]+8:current_box[1]+current_box[2]]
    mdhd_info = {
        'Version': mdhd_data[0],
        'Flag' : mdhd_data[1:4],
        'Creation_Time' : int.from_bytes(mdhd_data[4:8], byteorder='big'),
        'Modification_Time' : int.from_bytes(mdhd_data[8:12], byteorder='big'),
        'Time_Scale' : int.from_bytes(mdhd_data[12:16], byteorder='big'),
        'Duration' : int.from_bytes(mdhd_data[16:20], byteorder='big'),
        'Language' : int.from_bytes(mdhd_data[20:22], byteorder='big'),
        'Quality' : int.from_bytes(mdhd_data[22:24], byteorder='big')
    }

    #video_attribute['mdhd_time_scale'] = mdhd_info['Time_Scale']

    return mdhd_info

#vmhd 박스를 파싱하는 함수 - 사용 안함
def parse_vmhd(mp4_file, current_box):
    vmhd_data = mp4_file[current_box[1]+8:current_box[1]+current_box[2]]
    vmhd_info = {
        'Version' : vmhd_data[0],
        'Dummy' : vmhd_data[1:4],
        'Graphics_Mode' : vmhd_data[4:6],
        'OpColor(Red)' : vmhd_data[6:8],
        'OpColor(Green)' : vmhd_data[8:10],
        'OpColor(Blue)' : vmhd_data[10:12]
    }
    return vmhd_info

#smhd 박스를 파싱하는 함수 - 사용 안함
def parse_smhd(mp4_file, current_box):
    
    smhd_data = mp4_file[current_box[1]+8:current_box[1]+current_box[2]]
    smhd_info = {
        'Version' : smhd_data[0],
        'Flag' : smhd_data[1:4],
        'Reserved_1' : smhd_data[4:6],
        'Reserved_2' : smhd_data[6:8]
    }
    return smhd_info

#stsd 박스를 파싱하는 함수 - 사용 중
def parse_stsd(mp4_file, offset):
    temp={}
    box_size = int(mp4_file[offset:offset+4].hex(), 16)
    end_offset = offset+box_size
    version = mp4_file[offset+8]
    flag = mp4_file[offset+9:offset+12]
    entry_count = int(mp4_file[offset+12:offset+16].hex(), 16)

    child_box_offset = offset +16
    box_list = find_child_box_using_entry_count(mp4_file, child_box_offset, entry_count, end_offset)
    temp = {}
    rough = make_rough_dict(mp4_file, box_list, temp)
    #detail = make_detail_dict(mp4_file, box_list, temp)
    return rough

#mp4a 박스를 파싱하는 함수 - 사용 중
def parse_mp4a(mp4_file, offset):
    box_size = int(mp4_file[offset:offset+4].hex(), 16)

    #iPhone에서 내부에 아무 데이터도 없는 0xC 크기의 mp4a 박스를 확인함.
    #내부 데이터 있는 mp4a 박스랑 없는 mp4a 박스를 구분하기 위해서 아래의 조건문 두었음.
    if box_size <= 0xc:
        return {}
    
    else:
        data_reference_index = int(mp4_file[offset+8:offset+16].hex(),16)
        mp4a_version = int(mp4_file[offset+16:offset+18].hex(),16)
        channel_count = int(mp4_file[offset+18:offset+26].hex(),16)
        sample_size = int(mp4_file[offset+26:offset+28].hex(),16)

        if mp4a_version == 0:
            sample_rate = mp4_file[offset+28:offset+36]
            child_box_offset = offset +36
            box_list = find_child_box_offset(mp4_file, child_box_offset, box_size - 52)
            temp = {}
            rough = make_rough_dict(mp4_file, box_list, temp)
            #detail = make_detail_dict(mp4_file, box_list, temp)

        elif mp4a_version == 1:
            compress_id = int(mp4_file[offset+28:offset+30].hex(), 16)
            packet_size = int(mp4_file[offset+30:offset+32].hex(), 16)
            sample_rate = mp4_file[offset+32:offset+36]
            samples_per_packet = int(mp4_file[offset+36:offset+40].hex(), 16)
            bytes_per_packet = int(mp4_file[offset+40:offset+44].hex(), 16)
            bytes_per_frame = int(mp4_file[offset+44:offset+48].hex(), 16)
            bytes_per_sample = int(mp4_file[offset+48:offset+52].hex(), 16)
                
            child_box_offset = offset+52
            box_list = find_child_box_offset(mp4_file, child_box_offset, box_size - 52)
            temp = {}
            rough = make_rough_dict(mp4_file, box_list, temp)
            #detail = make_detail_dict(mp4_file, box_list, temp)
        
    return rough

#chan 박스를 파싱하는 함수 - 사용 중
def parse_chan(mp4_file, offset):
    temp = {}
    return temp

#wave 박스를 파싱하는 함수 - 사용 중
def parse_wave(mp4_file, offset):
    temp = {}
    
    box_size = int(mp4_file[offset:offset+4].hex(), 16)
    box_list = find_child_box_offset(mp4_file, offset+8, box_size-8)
    temp = {}
    rough = make_rough_dict(mp4_file, box_list, temp)
    #detail = make_detail_dict(mp4_file, box_list, temp)        
    return rough

#frma 박스를 파싱하는 함수 - 사용 중
def parse_frma(mp4_file, offset):
    coding_name = mp4_file[offset+8:offset+12].decode('latin-1')
    return {}

#esds 박스를 파싱하는 함수 - 사용 중
def parse_esds(mp4_file, offset):
    return {}

#mebx 박스를 파싱하는 함수 - 사용 중(아직 다 제작되지 않음 수정 필요)
def parse_mebx(mp4_file, offset):
    
    temp = {}
    temp['mebx'] = {}
    entry_count = int(mp4_file[offset+12:offset+16].hex(), 16)


    child_box_offset = offset +16
    child_box_size = int(mp4_file[child_box_offset:child_box_offset+4].hex(), 16)
    box_list = find_child_box_offset(mp4_file, child_box_offset, child_box_size)

    for child_info in box_list:
        #########################################################################################################################
        #아직 keys 형태가 다른걸 어떻게 처리할 지 몰라서 이렇게 남겨놓음
        temp['mebx']['{}'.format(child_info[0])] = {}
        
    return temp

#avc1 박스를 파싱하는 함수 - 사용 중
def parse_avc1(mp4_file, offset):

    
    temp = {}
    temp['avc1'] = {}
    box_size = int(mp4_file[offset:offset+4].hex(),16)

    avc1_box_data_end = 0

    for x in range(box_size):
        if mp4_file[offset+x:offset+x+2] == b'\xff\xff' :
                    
            avc1_box_data_end = offset+x
            
    child_offset = avc1_box_data_end + 2
    child_box_size = offset+box_size-child_offset
    box_list = find_child_box_offset(mp4_file, child_offset, child_box_size)
    temp = {}
    rough = make_rough_dict(mp4_file, box_list, temp)
    #detail = make_detail_dict(mp4_file, box_list, temp)
    return rough

#hvc1 박스를 파싱하는 함수 - 사용 중
def parse_hvc1(mp4_file, offset):
    
    temp = {}
    box_size = int(mp4_file[offset:offset+4].hex(),16)

    temp['hvc1'] = {}
    hvc1_box_data_end = 0
    for x in range(box_size):
        if mp4_file[offset+x:offset+x+2] == b'\xff\xff' :
            hvc1_box_data_end = offset+x
            break
            
    child_offset = hvc1_box_data_end + 2

    box_list = find_child_box_offset(mp4_file, child_offset, box_size - 52)
    temp = {}
    rough = make_rough_dict(mp4_file, box_list, temp)
    #detail = make_detail_dict(mp4_file, box_list, temp)

    return rough

#avcC 박스를 파싱하는 함수 - 사용 중
def parse_avcC(mp4_file, offset):

    video_attribute['codec'] = "h.264"
    #sps
    sps_offset = offset+14
    sps_size = int(mp4_file[sps_offset:sps_offset+2].hex(),16)
    sps_data = mp4_file[sps_offset+2:sps_offset+2+sps_size]
    hex_sps = ' '.join([f"{byte:02x}" for byte in sps_data])
    video_attribute['sps'] = hex_sps

    #pps
    pps_offset = sps_offset+2+sps_size+1
    pps_size = int(mp4_file[pps_offset:pps_offset+2].hex(),16)
    pps_data = mp4_file[pps_offset+2:pps_offset+2+pps_size]
    hex_pps = ' '.join([f"{byte:02x}" for byte in pps_data])
    video_attribute['pps'] = hex_pps
    return {}

#hvcC 박스를 파싱하는 함수 - 사용 중
def parse_hvcC(mp4_file, offset):

    video_attribute['codec'] = "h.265"
    box_size = int(mp4_file[offset:offset+4].hex(), 16)

    for y in range(box_size):
    #vps
        if mp4_file[offset + y : offset + y + 2] in [b'\xa0\x00', b'\x20\x00'] and mp4_file[offset+y+5] == 0x40:
            vps_offset = offset + y + 3
            vps_size = int(mp4_file[vps_offset:vps_offset+2].hex(), 16)
            vps_data = mp4_file[vps_offset+2:vps_offset + 2 + vps_size]
            hex_vps = ' '.join([f"{byte:02x}" for byte in vps_data])
            video_attribute['vps'] = hex_vps
                        
                #sps
        elif mp4_file[offset + y : offset + y + 2] in [b'\xa1\x00', b'\x21\x00'] and mp4_file[offset+y+5] == 0x42:
            sps_offset = offset + y + 3
            sps_size = int(mp4_file[sps_offset:sps_offset+2].hex(), 16)
            sps_data = mp4_file[sps_offset+2:sps_offset + 2 + sps_size]
            hex_sps = ' '.join([f"{byte:02x}" for byte in sps_data])
            video_attribute['sps'] = hex_sps
                        
        #pps
        elif mp4_file[offset + y : offset + y + 2] in [b'\xa2\x00', b'\x22\x00'] and mp4_file[offset+y+5] == 0x44:
            pps_offset = offset + y + 3
            pps_size = int(mp4_file[pps_offset:pps_offset+2].hex(), 16)
            pps_data = mp4_file[pps_offset+2:pps_offset + 2 + pps_size]
            hex_pps = ' '.join([f"{byte:02x}" for byte in pps_data])
            video_attribute['pps'] = hex_pps

    return {}

#stts 박스를 파싱하는 함수 - 사용 안함
def parse_stts(mp4_file, offset):
    
    
    temp={}
    version = mp4_file[offset+8]
    flag = mp4_file[offset+9:offset+12]
    entry_count = int(mp4_file[offset+12:offset+16].hex(), 16)

    for i in range(entry_count):
        index = mp4_file[offset+ 16 + i*8 : offset + 24 + i * 8]
        sample_count = int(index[:4].hex(), 16)
        sample_delta = int(index[4:].hex(), 16)
        temp['index_{}'.format(i+1)] = {'sample_count' : sample_count,
                                        'sample_delta' : sample_delta}

    return temp

#stsc 박스를 파싱하는 함수 - 사용 안함
def parse_stsc(mp4_file, offset):
    
    
    temp={}
    version = mp4_file[offset+8]
    flag = mp4_file[offset+9:offset+12]
    entry_count = int(mp4_file[offset+12:offset+16].hex(), 16)

    for i in range(entry_count):
        index = mp4_file[offset+ 16 + i*12 : offset + 28 + i * 12]
        first_chunk = int(index[:4].hex(), 16)
        samples_per_chunk = int(index[4:8].hex(), 16)
        sample_description_index = int(index[8:].hex(), 16)
        temp['index_{}'.format(i+1)] = {'first_chunk' : first_chunk,
                                        'samples_per_chunk' : samples_per_chunk,
                                        'sample_description_index' : sample_description_index}

    return temp

#stss 박스를 파싱하는 함수 - 사용 안함
def parse_stss(mp4_file, offset):
    

    version = mp4_file[offset+8]
    flag = mp4_file[offset+9:offset+12]
    entry_count = int(mp4_file[offset+12:offset+16].hex(), 16)
    sample_number = []
    
    for i in range(entry_count):
        sample_number.append(int(mp4_file[offset+16 + i*4: offset + 20+i*4].hex(), 16))

    temp = {'version': version, 'flag': flag, 'entry_count': entry_count, 'frame_offset' : sample_number}

    return temp

#stsz 박스를 파싱하는 함수 - 사용 안함
#애도 파싱 잘 안되어 보임
def parse_stsz(mp4_file, offset):
    
    
    version = mp4_file[offset+8]
    flag = mp4_file[offset+9:offset+12]
    entry_count = int(mp4_file[offset+12:offset+16].hex(), 16)
    entry_size = []
    
    for i in range(entry_count):
        entry_size.append(int(mp4_file[offset+16 + i*4: offset + 20+i*4].hex(), 16))

    temp = {'version': version, 'flag': flag, 'entry_count': entry_count, 'frame_offset' : entry_size}

    return temp

#dref 박스를 파싱하는 함수 - 사용 중
def parse_dref(mp4_file, offset):
    
    
    temp={}
    box_size = int(mp4_file[offset:offset+4].hex(), 16)
    end_offset = offset + box_size
    entry_count = int(mp4_file[offset+8:offset+16].hex(),16)
    child_box_offset = offset + 16


    box_list = find_child_box_using_entry_count(mp4_file, child_box_offset, entry_count, end_offset)
    temp = {}
    rough = make_rough_dict(mp4_file, box_list, temp)
    #detail = make_detail_dict(mp4_file, box_list, temp)
    return rough

#stco 박스를 파싱하는 함수 - 사용 안함
def parse_stco(mp4_file, current_box):
    
    version = mp4_file[current_box[1]+8]
    flag = mp4_file[current_box[1]+9:current_box[1]+12]
    entry_count = int(mp4_file[current_box[1]+12:current_box[1]+16].hex(), 16)
    chunk_offset = []
    
    for i in range(entry_count):
        chunk_offset.append(int(mp4_file[current_box[1]+16 + i*4: current_box[1] + 20+i*4].hex(), 16))

    temp = {'version': version, 'flag': flag, 'entry_count': entry_count, 'frame_offset' : chunk_offset}
    #print(temp)
    return temp

#co64 박스를 파싱하는 함수 - 사용 안함
#제대로 파싱이 안되는 듯
def parse_co64(mp4_file, offset):
    
    version = mp4_file[offset+8]
    flag = mp4_file[offset+9:offset+12]
    entry_count = int(mp4_file[offset+12:offset+16].hex(), 16)
    chunk_offset = []
    
    for i in range(entry_count):
        chunk_offset.append(int(mp4_file[offset+16 + i*8: offset + 20+i*8].hex(), 16))

    temp = {'version': version, 'flag': flag, 'entry_count': entry_count, 'frame_offset' : chunk_offset}

    return {}

#hdlr 박스를 파싱하는 함수 - 사용 중
def parse_hdlr(mp4_file, current_box):
    hdlr= {}
    handler_type= mp4_file[current_box[1]+16:current_box[1]+20]
    handler_type = data_decoder.decode(handler_type)
    component_manufacutre = mp4_file[current_box[1]+20:current_box[1]+24]
    component_flags_mask = mp4_file[current_box[1]+24:current_box[1]+28]
    rest_data = mp4_file[current_box[1]+28:current_box[1]+current_box[2]]
    rest_data = data_decoder.decode(rest_data)

    if handler_type == "vide":
        hdlr['hdlr_vide'] = rest_data

    elif handler_type == "soun":
        hdlr['hdlr_soun'] = rest_data
    
    video_attribute.update(hdlr)

    temp = handler_type

    #meta_attribute['handler_type'] = temp
    return temp

#keys 박스를 파싱하는 함수 - 사용 중
def parse_keys(mp4_file, offset):

    box_size = int(mp4_file[offset:offset+4].hex(), 16)
    entry_count = int(mp4_file[offset+12:offset+16].hex(), 16)
    
    child_box_offset = offset + 16
    box_list = find_child_box_using_entry_count(mp4_file, child_box_offset, entry_count, box_size)
    temp = {}
    rough = make_rough_dict(mp4_file, box_list, temp)
    #detail = make_detail_dict(mp4_file, box_list, temp)

    return {}

def parse_mdta(mp4_file, current_box):
    mdta_data = mp4_file[current_box[1]+8:current_box[1]+current_box[2]]
    mdta_data = data_decoder.decode(mdta_data)
    return mdta_data

#iPhone 기기 식별 정보가 남는 곳이라서 iPhone 기준으로 파싱 방법을 만들었음.
#그래서 타 기기에서 ilst박스가 나왔을 때 파싱 방법이 맞지 않아 오류가 발생할 수 있음.
#ilst 박스를 파싱하는 함수 - 사용 중
def parse_ilst(mp4_file, offset):
    box_list = []
    box_size = int(mp4_file[offset:offset+4].hex(), 16)
    child_offset = offset + 16

    while child_offset < offset + box_size:
        child_box_size = int(mp4_file[child_offset:child_offset+4].hex(), 16)
        child_box_name = mp4_file[child_offset+4:child_offset+8].decode('latin-1')
        
        data = [child_box_name, child_offset, child_box_size]
        box_list.append(data)
        child_offset += child_box_size+8

    temp = {}
    rough = make_rough_dict(mp4_file, box_list, temp)

    meta_attribute.update(rough)
    return {}

def parse_YITH(mp4_file, current_box):
    data = mp4_file[current_box[1]+8:current_box[1]+current_box[2]]
    data = data_decoder.decode(data)
    data = json.loads(data)
    meta_attribute.update(data)
    return {}

#iPhone 기기 식별 정보가 남는 곳이라서 iPhone 기준으로 파싱 방법을 만들었음.
#그래서 타 기기에서 data박스가 나왔을 때 파싱 방법이 맞지 않아 오류가 발생할 수 있음.
#삼성 동영상의 경우 utf-8로 디코딩이 안되는 값이 ilst의 data 박스의 값으로 들어간 경우를 식별함.
#따라서 if로 분기문 만들어서 저장하였음.
#data 박스를 파싱하는 함수 - 사용 중
def parse_data(mp4_file, offset):
    box_size = int(mp4_file[offset:offset+4].hex(), 16)
    data = mp4_file[offset+16:offset+box_size]
    data = data_decoder.decode(data)
    return data

def parse_xyz(mp4_file, current_box):
    end_offset = current_box[1] + current_box[2]
    xyz = mp4_file[current_box[1]+12:end_offset]
    xyz=data_decoder.decode(xyz)
    meta_attribute['xyz'] = xyz
    return xyz

def parse_swr(mp4_file, current_box):
    end_offset = current_box[1] + current_box[2]
    os_version = mp4_file[current_box[1]+12:end_offset]
    os_version=data_decoder.decode(os_version)
    meta_attribute['swr'] = os_version
    return os_version

def parse_day(mp4_file, current_box):
    end_offset = current_box[1] + current_box[2]
    date = mp4_file[current_box[1]+12:end_offset]
    date=data_decoder.decode(date)
    meta_attribute['day'] = date 
    return date

def parse_mak(mp4_file, current_box):
    end_offset = current_box[1] + current_box[2]
    maker = mp4_file[current_box[1]+12:end_offset]
    maker=data_decoder.decode(maker)
    meta_attribute['mak'] = maker
    return maker

def parse_mod(mp4_file, current_box):
    end_offset = current_box[1] + current_box[2]
    mod = mp4_file[current_box[1]+12:end_offset]
    mod=data_decoder.decode(mod)
    meta_attribute['mod'] = mod 
    return mod

def parse_mdl(mp4_file, current_box):
    end_offset = current_box[1]+current_box[2]
    mdl = mp4_file[current_box[1]+8:end_offset]
    mdl=data_decoder.decode(mdl)
    meta_attribute['mdl'] = mdl
    return mdl

def parse_modl(mp4_file, current_box):
    model_name_start_offset = current_box[1]+14
    end_offset = current_box[1]+current_box[2]
    model_name = mp4_file[model_name_start_offset:end_offset]
    model_name=data_decoder.decode(model_name)
    meta_attribute['modl'] = model_name
    return model_name

#canon와 sony에서 확인되는 박스 였음.
#canon의 경우 기기모델명과 제조사를 식별할 수 있는 박스가 담겨있었음.
#반면 소니의 경우 uuid 박스가 2개가 식별되었는데, 2개 박스의 구조가 달랐음.
#그래서 uuid 딕셔너리로 uuid 박스에 해당하는 데이터를 따로 빼어 canon 식별이 가능하도록 일단 조치함.
def parse_uuid(mp4_file, current_box):
    
    children_start_offset = current_box[1] + 24
    box_list = find_child_box_offset(mp4_file, children_start_offset, current_box[2]-24)
    temp = {}
    rough = make_rough_dict(mp4_file, box_list, temp)
    uuid.update(rough)
    return {}

def parse_CNDA(mp4_file, current_box):
    jpeg_start_offset = current_box[1]+8
    end_offset = current_box[1]+current_box[2]
    jpeg_img = mp4_file[jpeg_start_offset:end_offset]
    image_addr = "./temp/in_video_jpg_file.jpg"

    jpeg_file = open(image_addr, "wb")
    jpeg_file.write(jpeg_img)
    jpeg_file.close()
    exif = get_exif_info.get_image_exif(image_addr)
    
    meta_attribute.update(exif)
    os.remove(image_addr)
    return exif

def parse_auth(mp4_file, current_box):
    end_offset = current_box[1]+current_box[2]
    device = mp4_file[current_box[1]+8:end_offset]    
    device = data_decoder.decode(device)
    meta_attribute['auth']=device

    return device

def parse_CAME(mp4_file, current_box):
    end_offset = current_box[1]+current_box[2]
    device = mp4_file[current_box[1]+8:end_offset]    
    device=data_decoder.decode(device)
    meta_attribute['CAME']=device
    return device

def parse_FIRM(mp4_file, current_box):
    end_offset = current_box[1]+current_box[2]
    firmware = mp4_file[current_box[1]+8:end_offset]    
    firmware =data_decoder.decode(firmware)
    meta_attribute['FIRM']= firmware
    return firmware
    
#모르는 박스를 파싱하는 함수
def parse_unknown_box(mp4_file, offset, box_size):
    
    
    unknown_box_data = mp4_file[offset+8:offset+box_size]
    return unknown_box_data


############################################################################################################
############################################################################################################
############################################################################################################


def get_file_size(file_address):
    try:
        size = os.path.getsize(file_address)
        return size
    except FileNotFoundError:
        return None

def box_name_and_size(mp4_file, start_offset, size):
    box_info = []

    end_offset = start_offset +size

    box_size = int(mp4_file[start_offset:start_offset+0x4].hex(), 16)

    #start_offset으로부터 4바이트가 박스 사이즈가 맞는지 체크
    #자식 박스 크기로 인식한 4바이트가 부모 박스 혹은 파일 크기보다 클 경우 자식 박스가 아니라고 판단
    if box_size > end_offset:
        return False
    
    #박스 크기가 0이거나 1보다 크면서 8보다 작을 경우 자식 박스가 아니라고 판단
    elif box_size == 0 or box_size > 1 and box_size < 8:
        return False        
    
    else:
        box_name = mp4_file[start_offset+0x4:start_offset+0x8]
        
    #박스 이름에 해당하는 데이터가 아스키코드 4바이트로 이루어진 것인지 확인
    #이었으나, 애플 iPhone 박스 이름이 아스키 코드가 아닌 경우를 확인하여서 1이상으로 수정하였음.
    #애플 iPhone 박스 이름을 예외로 처리하는 것이 더 안정적이라 다시 수정하였음.
        if all(20 <= byte <=126 for byte in box_name): 
        
            #삼성카메라의 경우 mdat 박스의 앞 4바이트가 0x00 0x00 0x00 0x01인 것을 반영
            if box_size == 1 and box_name == b'mdat':
                box_size = int(mp4_file[start_offset + 8:start_offset+16].hex(), 16)
        
            box_info.extend([box_name.decode('latin-1'), start_offset, box_size])
            return box_info

        #©xyz, ©xsp, ©ysp 같은 박스 읽기 위하여 만든 조건문
        elif box_name[0] == 0xa9 and all(40 <= byte <=126 for byte in box_name[1:4]):
            box_info.extend([box_name.decode('latin-1'), start_offset, box_size])
            return box_info

    #박스 이름에 해당하는 데이터가 아스키코드로 이루어지지 않았을 시 False 반환
        else:
            box_info.extend(["    ", start_offset, box_size])
            return box_info
            #return False

def find_child_box_using_entry_count(mp4_file, start_offset, entry_count, size):
    child_box_list = []
    current_offset = start_offset

    for i in range(entry_count):
        child_box = box_name_and_size(mp4_file, current_offset, size)
        
        #######################################################################################################이부분 고쳐져야 할 것 같음.
        if child_box == False:
            print("wrong")

        else:
            if child_box[0] == '':
                child_box[0] = 'unknown_DATA'

            child_box_list.append(child_box)
            current_offset+=child_box[2]
    
    return child_box_list
         

#예하 박스의 경우 예하 박스 시작 offset과 부모박스 사이즈에서 -8을 하여 아래의 함수 사용 가능
def find_child_box_offset(mp4_file, start_offset, box_size):
    child_box_list = []

    current_offset=start_offset

    end_offset = start_offset+box_size

    while True:
        child_box = box_name_and_size(mp4_file, current_offset, end_offset)
        if child_box == False:
            unknown_box_data = mp4_file[current_offset:start_offset+box_size]
            not_calculated_data = ['unknown_DATA', current_offset, len(unknown_box_data)]
            child_box_list.append(not_calculated_data)
            break
            
        else:
            if child_box[0] == '':
                child_box[0] = 'unknown_DATA'

            child_box_list.append(child_box)

        if child_box[2] == 0:
            break

        else:
            current_offset+=child_box[2]
            if current_offset >= start_offset + box_size:
                break

    return child_box_list

#mp4 컨테이너 구조를 파악하여 딕셔너리로 저장하는 함수임.
#trak 같은 여러개 있을 수 있는 atom(박스)의 경우 뒤에 숫자를 붙혀서 키가 중복되지 않게 처리하였음.

#Samsung Galaxy S21에서 1:1, full 화면 비율의 경우 9:16 비율에서는 확인할 수 없었던 edts 박스가 생기는 것을 확인함.
#동일 기기에서는 동일 구조를 나타내도록 하기 위하여 edts 박스를 키에서 제거하는 옵션을 넣어줌
#근데 Galaxy Note 10에서는 화면 비율을 변경하여도 edts 박스가 생기지 않았음.

#©xyz, ©xsp, ©ysp의 경우 사용자가 위치 설정을 켜고 끄느냐에 따라 영상에 포함되거나 포함되지 않는 경우가 선택이 됨.
#©xyz가 포함되면서 원래는 발생하지 않는 udta 박스가 생기는 경우를 포착함
#따라서 udts도 edts 박스처럼 키에서 제거하는 옵션을 넣었음.
#udts는 나중에 따로 파싱하여 필요한 데이터 넣어주는  

#2024년 03월 29일
#udta, edts, avc1, hvc1의 경우 사용자 의지대로 바꾸는 것이 가능하기 때문에 해당 키 제외 필요성 확인
#화웨이 P9의 영상 대부분은 co64를 사용했는데 영상 한개에서 stco를 사용하는 것을 확인, 상황에 따라 바뀔 수도 있다고 판단.

#ver2는 udta, edts, stco, co64만 제거한 버전
def make_rough_dict(mp4_file, box_list, dict):
    keys = dict.keys()
    #print(box_list)

    for box in box_list:
        same_key = 0
        for key in keys:
            if box[0] in key:
                same_key+=1

        if same_key == 0:
            if box[2] == 8: #박스 사이즈가 8인 애들에 대한 처리
                dict['{}'.format(box[0])] = {}
            else:
                dict['{}'.format(box[0])] = identify_box(mp4_file, box)

        else:
            #augentix 기기의 경우 mdat과 moof가 프레임마다 하나씩 발생하였음.
            #그래서 영상 길이마다 박스 개수가 달라질 것이기에 5개까지만 구조에 포함하도록 만듦 
            if box[0] == 'mdat' or box[0] == 'moof':  
                if same_key < 5:
                    dict['{}_{}'.format(box[0], same_key)] = identify_box(mp4_file, box)

            else:
                if box[2] == 8: #박스 사이즈가 8인 애들에 대한 처리
                    dict['{}'.format(box[0])] = {}
                else:
                    dict['{}_{}'.format(box[0], same_key)] = identify_box(mp4_file, box)

    return(dict)

#박스 이름을 받고 해당 이름에 맞는 파싱 함수 호출
def identify_box(mp4_file, current_box):

    if 'ftyp' in current_box[0] :
        temp = parse_ftyp(mp4_file, current_box)
        return {}
    
    elif 'wide' in current_box[0]:
        return {}

    elif 'mdat' in current_box[0] :
        return {}
    
    elif 'moov' in current_box[0] :
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough
    
    elif 'trak' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough

    elif 'tkhd' in current_box[0]:
        return {}
    
    elif 'tapt' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough
    
    elif 'clef' in current_box[0]:
        return {}
    
    elif 'prof' in current_box[0]:
        return {}
    
    elif 'enof' in current_box[0]:
        return {}
    
    elif 'meta' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough

    elif 'mdia' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough
    
    elif 'mvhd' in current_box[0]:
        temp = parse_mvhd(mp4_file, current_box)
        return {}
    
    elif 'mdhd' in current_box[0]:
        return {}

    elif 'mvex' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough
    
    elif 'moof' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough
    
    elif 'tfhd' in current_box[0]:
        return {}
    
    elif 'trun' in current_box[0]:
        return {}

    elif 'tref' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough
    
    elif 'cdsc' in current_box[0]:
        return {}
    
    elif 'cdep' in current_box[0]:
        return {}

    elif 'hdlr' in current_box[0]:
        temp = parse_hdlr(mp4_file, current_box)
        return temp

    elif 'minf' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough

    elif 'smhd' in current_box[0]:
        return {}

    elif 'vmhd' in current_box[0]:
        return {}

    elif 'dinf' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough

    elif 'dref' in current_box[0]: 
        temp = parse_dref(mp4_file, current_box[1])
        return temp

    elif 'url ' in current_box[0]:
        return {}

    elif 'alis' in current_box[0]:
        return {}

    elif 'stbl' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough

    elif 'stsd' in current_box[0]: #내부 박스 코딩 필요
        temp = parse_stsd(mp4_file, current_box[1])
        return temp
    
    elif 'mp4a' in current_box[0]:
        temp = parse_mp4a(mp4_file, current_box[1])
        return temp
    
    elif 'chan' in current_box[0]:
        temp = parse_chan(mp4_file, current_box[1])
        return temp
    
    elif 'wave' in current_box[0]:
        temp = parse_wave(mp4_file, current_box[1])
        return temp
    
    elif 'frma' in current_box[0]:
        temp = parse_frma(mp4_file, current_box[1])
        return temp

    elif 'esds' in current_box[0]:
        temp = parse_esds(mp4_file, current_box[1])
        return temp

    elif 'hvc1' in current_box[0]:
        temp = parse_hvc1(mp4_file, current_box[1])
        return temp
    
    elif 'hvcC' in current_box[0]:
        temp = parse_hvcC(mp4_file, current_box[1])
        return temp
    
    elif 'avc1' in current_box[0]:
        temp = parse_avc1(mp4_file, current_box[1])
        return temp
    
    elif 'avcC' in current_box[0]:
        temp = parse_avcC(mp4_file, current_box[1])
        return temp

    elif 'colr' in current_box[0]:
        return {}
    
    #mebx 박스의 경우 자식 박스인 keys가 meta 박스의 자식 박스인 keys와 겹침.
    #둘을 구분해서 얻을 사항이 없어 보여 일단 빈 딕셔너리를 리턴하도록 조치함.
    elif 'mebx' in current_box[0]:
        temp = parse_mebx(mp4_file, current_box[1])
        return {}

    elif 'stco' in current_box[0]:
        temp = parse_stco(mp4_file, current_box)
        return {}
    
    elif 'stss' in current_box[0]:
        return {}

    elif 'stsz' in current_box[0]:
        return {}

    elif 'stts' in current_box[0]:
        return {}

    elif 'stsc' in current_box[0]:
        return {}

    elif 'co64' in current_box[0]:
        return {}
    
    elif 'free' in current_box[0]:
        return {}
    
    elif 'skip' in current_box[0]:
        return {}
    
    elif 'gmin' in current_box[0]:
        return {}

    elif 'elst' in current_box[0]:
        return {}

    elif 'cslg' in current_box[0]:
        return {}
    
    elif 'ctts' in current_box[0]:
        return {}
    
    elif 'sdtp' in current_box[0]:
        return {}

    elif 'udta' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        udta.update(rough)
        return rough
    
    elif 'auth' in current_box[0]:
        temp = parse_auth(mp4_file, current_box)
        return {}
    
    elif 'YITH' in current_box[0]:
        temp = parse_YITH(mp4_file, current_box)
        return {}
    
    elif 'meta' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough
    
    elif 'edts' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough
    
    elif 'keys' in current_box[0]:
        temp = parse_keys(mp4_file, current_box[1])
        return temp
    
    elif 'mdta' in current_box[0]:
        temp = parse_mdta(mp4_file, current_box)
        return {}
    
    elif 'ilst' in current_box[0]:
        temp = parse_ilst(mp4_file, current_box[1])
        return temp
    
    elif 'data' in current_box[0]:
        temp = parse_data(mp4_file, current_box[1])
        return temp
    
    elif '©xyz' in current_box[0]:
        temp = parse_xyz(mp4_file, current_box)
        return {}
    
    elif '©swr' in current_box[0]:
        temp = parse_swr(mp4_file, current_box)
        return {}
    
    elif '©day' in current_box[0]:
        temp = parse_day(mp4_file, current_box)
        return {}
    
    elif '©mod' in current_box[0]:
        temp = parse_mod(mp4_file, current_box)
        return {}
    
    elif '©mak' in current_box[0]:
        temp = parse_mak(mp4_file, current_box)
        return {}
    
    elif '©mdl' in current_box[0]:
        temp = parse_mdl(mp4_file, current_box)
        return {}
    
    elif 'uuid' in current_box[0]:
        temp = parse_uuid(mp4_file, current_box)
        return temp

    elif 'CNTH' in current_box[0]:
        box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
        temp = {}
        rough = make_rough_dict(mp4_file, box_list, temp)
        return rough
    
    elif 'CNDA' in current_box[0]:
        temp = parse_CNDA(mp4_file, current_box)
        return {}
    
    elif 'modl' in current_box[0]:
        temp = parse_modl(mp4_file, current_box)
        return {}
    
    elif 'CAME' in current_box[0]:
        temp = parse_CAME(mp4_file, current_box)
        return {}
    
    elif 'FIRM' in current_box[0]:
        temp = parse_FIRM(mp4_file, current_box)
        return {}
    
    
    else :
        '''
        temp = box_name_and_size(mp4_file, current_box[1], current_box[2])
        if temp == False :
            return {}
        
        else :
            
            box_list=find_child_box_offset(mp4_file, current_box[1]+8, current_box[2]-8)
            if box_list != False:
                temp = {}
                rough = make_rough_dict(mp4_file, box_list, temp)
                return rough

            else:
                return {}        
        '''        
        return {}

def box_analyze(mp4_file, file_size):
    file = {}
    grand_parent_box = find_child_box_offset(mp4_file, 0, file_size)
    parse_result = make_rough_dict(mp4_file, grand_parent_box, file)
     
    return parse_result, video_attribute, meta_attribute, udta, uuid

'''
file_addr = "/mnt/c/users/jsj97/downloads/IMG_5595.mov"
with open(file_addr, "rb") as file:
    file_size = get_file_size(file_addr)
    video_data = file.read()

print(file_addr)
print(box_analyze(video_data, file_size))
'''

root_dir = "D:/졸업논문/data_mp4_h26X/"

device_dir = os.listdir(root_dir)

h264_device = []
h264_mp4 = []
h264_box_structure = []
h264_major_brand = []
h264_compatible_brand = []
h264_mvhd_time_scale = []
h264_mdhd_time_scale = []
h264_sps_result = []
h264_parsed_sps = []
h264_pps_result = []
h264_parsed_pps = []
h264_hdlr_vide = []
h264_hdlr_soun = []
h264_kinds_of_frames = []
h264_frame_structure = []
h264_meta_data = []
h264_udta_data = []
h264_uuid_data = []

h265_device = []
h265_mp4 = []
h265_box_structure = []
h265_major_brand = []
h265_compatible_brand = []
h265_mvhd_time_scale = []
#h265_mdhd_time_scale = []
h265_vps_result =[]
h265_parsed_vps =[]
h265_sps_result = []
h265_parsed_sps = []
h265_pps_result = []
h265_parsed_pps = []
h265_hdlr_vide = []
h265_hdlr_soun = []
h265_meta_data = []
h265_udta_data = []
h265_uuid_data = []
h265_kinds_of_frames = []
h265_frame_structure = []

for dir in device_dir: #폴더 넘어가는게 이 반복문
    files = os.listdir(f"{root_dir}{dir}/")
    
    #print(files)
    md5 = []
    
    for file in files: #파일 넘어가는게 이 반복문
        path = f"{root_dir}{dir}/{file}"
        print(path)
    
        if file in [".json" ,".AVI"] :
            pass
        
        else:
            with open(path, "rb") as file:
                file_size = get_file_size(path)
                video_data = file.read()
            video_attribute = {}
            meta_attribute = {}
            udta = {}
            uuid = {}
            parsed_result = box_analyze(video_data, file_size)

            if parsed_result[1]['codec'] == 'h.264':
                mdat = mdat_analyze.parse_h264_mdat(path)
                h264_device.append(dir)
                h264_mp4.append(file)
                h264_box_structure.append(str(parsed_result[0]))
                h264_major_brand.append(str(parsed_result[1]['ftyp_major_brand']))
                h264_compatible_brand.append(str(parsed_result[1]['ftyp_compatible_brand']))
                h264_mvhd_time_scale.append(str(parsed_result[1]['mvhd_time_scale']))
                #264_mdhd_time_scale.append(str(parsed_result[1]['mdhd_time_scale']))
                h264_sps_result.append(str(parsed_result[1]['sps']))
                h264_parsed_sps.append(str(mdat[2]))
                h264_pps_result.append(str(parsed_result[1]['pps']))
                h264_parsed_pps.append(str(mdat[3]))
                h264_hdlr_vide.append(str(parsed_result[1]['hdlr_vide']))

                keys = parsed_result[1].keys()
                if 'hdlr_soun' in keys:
                    h264_hdlr_soun.append(str(parsed_result[1]['hdlr_soun']))
                else:
                    h264_hdlr_soun.append("")
                h264_kinds_of_frames.append(str(mdat[0]))
                h264_frame_structure.append(str(mdat[1]))
                h264_meta_data.append(str(parsed_result[2]))
                h264_udta_data.append(str(parsed_result[3]))
                h264_uuid_data.append(str(parsed_result[4]))

            
            elif parsed_result[1]['codec'] == 'h.265':
                h265_device.append(dir)
                h265_mp4.append(file)
                mdat = mdat_analyze.parse_h265_mdat(path)
                h265_box_structure.append(str(parsed_result[0]))
                h265_major_brand.append(str(parsed_result[1]['ftyp_major_brand']))
                h265_compatible_brand.append(str(parsed_result[1]['ftyp_compatible_brand']))
                h265_mvhd_time_scale.append(str(parsed_result[1]['mvhd_time_scale']))
                #h265_mdhd_time_scale.append(str(parsed_result[1]['mdhd_time_scale']))
                h265_vps_result.append(str(parsed_result[1]['vps']))
                h265_parsed_vps.append(str(mdat[2]))
                h265_sps_result.append(str(parsed_result[1]['sps']))
                h265_parsed_sps.append(str(mdat[3]))
                h265_pps_result.append(str(parsed_result[1]['pps']))
                h265_parsed_pps.append(str(mdat[4]))
                h265_hdlr_vide.append(str(parsed_result[1]['hdlr_vide']))
                keys = parsed_result[1].keys()
                if 'hdlr_soun' in keys:
                    h265_hdlr_soun.append(str(parsed_result[1]['hdlr_soun']))
                else:
                    h265_hdlr_soun.append("")
                h265_kinds_of_frames.append(str(mdat[0]))
                h265_frame_structure.append(str(mdat[1]))    
                h265_meta_data.append(str(parsed_result[2]))
                h265_udta_data.append(str(parsed_result[3]))
                h265_uuid_data.append(str(parsed_result[4]))

print(len(h264_device))
print(len(h264_mp4))
print(len(h264_box_structure))
print(len(h264_major_brand))
print(len(h264_compatible_brand))
#print(len(h264_vmhd_time_scale))
print(len(h264_mdhd_time_scale))

print(len(h264_sps_result))
print(len(h264_parsed_sps))
print(len(h264_pps_result))
print(len(h264_parsed_pps))
print(len(h264_hdlr_vide))
print(len(h264_hdlr_soun))
print(len(h264_kinds_of_frames))
print(len(h264_frame_structure))
print(len(h264_meta_data))
print(len(h264_udta_data))
print(len(h264_uuid_data))

h264_video_info = {}
h264_video_info['h264_device'] = h264_device
h264_video_info['h264_mp4'] = h264_mp4
h264_video_info['h264_box_structure'] = h264_box_structure
h264_video_info['h264_major_brand'] = h264_major_brand
h264_video_info['h264_compatible_brand'] = h264_compatible_brand
h264_video_info['h264_vmhd_time_scale'] = h264_mvhd_time_scale
#h264_video_info['h264_mdhd_time_scale'] = h264_mdhd_time_scale
h264_video_info['h264_sps_result'] = h264_sps_result
h264_video_info['h264_parsed_sps'] = h264_parsed_sps
h264_video_info['h264_pps_result'] = h264_pps_result
h264_video_info['h264_parsed_pps'] = h264_parsed_pps
h264_video_info['h264_hdlr_vide'] = h264_hdlr_vide
h264_video_info['h264_hdlr_soun'] = h264_hdlr_soun
h264_video_info['h264_kinds_of_frames'] = h264_kinds_of_frames
h264_video_info['h264_frame_structure'] = h264_frame_structure
h264_video_info['h264_meta_data'] = h264_meta_data
h264_video_info['h264_udta_data'] = h264_udta_data
h264_video_info['h264_uuid_data'] = h264_uuid_data

print(len(h265_device))
print(len(h265_mp4))
print(len(h265_box_structure))
print(len(h265_major_brand))
print(len(h265_compatible_brand))
print(len(h265_vps_result))
print(len(h265_sps_result))
print(len(h265_pps_result))
print(len(h265_hdlr_vide))
print(len(h265_hdlr_soun))
print(len(h265_meta_data))
print(len(h265_udta_data))
print(len(h265_uuid_data))
print(len(h265_parsed_vps))
print(len(h265_parsed_sps))
print(len(h265_parsed_pps))
print(len(h265_kinds_of_frames))
print(len(h265_frame_structure))

h265_video_info={}
h265_video_info['h265_device'] = h265_device
h265_video_info['h265_mp4'] = h265_mp4
h265_video_info['h265_box_structure'] = h265_box_structure
h265_video_info['h265_major_brand'] = h265_major_brand
h265_video_info['h265_compatible_brand'] = h265_compatible_brand
h265_video_info['h265_vmhd_time_scale'] = h265_mvhd_time_scale
#h265_video_info['h265_mdhd_time_scale'] = h265_mdhd_time_scale
h265_video_info['h265_vps_result'] = h265_vps_result
h265_video_info['h265_parsed_vps'] = h265_parsed_vps
h265_video_info['h265_sps_result'] = h265_sps_result
h265_video_info['h265_parsed_sps'] = h265_parsed_sps
h265_video_info['h265_pps_result'] = h265_pps_result
h265_video_info['h265_parsed_pps'] = h265_parsed_pps
h265_video_info['h265_hdlr_vide'] = h265_hdlr_vide
h265_video_info['h265_hdlr_soun'] = h265_hdlr_soun
h265_video_info['h265_kinds_of_frames'] = h265_kinds_of_frames
h265_video_info['h265_frame_structure'] = h265_frame_structure
h265_video_info['h265_meta_data'] = h265_meta_data
h265_video_info['h265_udta_data'] = h265_udta_data
h265_video_info['h265_uuid_data'] = h265_uuid_data

h264_info = pd.DataFrame(h264_video_info)
h264_info.to_csv("./result/h264_result.csv")

h265_info = pd.DataFrame(h265_video_info)
h265_info.to_csv("./result/h265_result.csv")
#'''