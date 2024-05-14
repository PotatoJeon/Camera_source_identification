import subprocess
import os

def h264_odd_to_binary(num):
    # 홀수번째는 3비트로 표현
    return format(num, '03b')

def h264_even_to_binary(num):
    # 짝수번째는 5비트로 표현
    return format(num, '05b')

def h265_to_binary(num):
    binary_str = format(num, '06b')
    binary_str = '0' + binary_str +'0'
    return hex(int(binary_str, 2))

# h.264 프레임 배치 구조가 각 GOP마다 모두 동일한지 확인함.
def h264_find_different_element(lst):
    if len(lst) < 2:
        return None  # 리스트가 비어 있거나 요소가 하나뿐이면 다른 요소가 없으므로 None 반환
    first_element = lst[0]
    for element in lst[1:]:
        if element != first_element:
            return first_element, element
    return None

# mp4 파일을 ffmpeg를 통해 h.264 비트스트림으로 전환한 후
# h264_analyze를 통해서 sps, pps를 파싱한 데이터를 저장
# "nal->" 이 포함된 문자열만을 뽑아, SPS, PPS, I-Frame, P-Frame의 배치 순서를 확인하는 함수
def parse_h264_mdat(file_addr):

    output_file = "./temp/bitstream.h264" #삭제하기 전 저장하는 비트스트림 파일 경로

    # ffmpeg 명령어, file_addr의 파일을 h.264 비트스트림으로 전환하여 out_file의 경로에 저장
    mp4_to_h264bitstream = [
        "./ffmpeg/ffmpeg.exe",
        "-i", file_addr,
        "-c:v", "copy",
        "-bsf", "h264_mp4toannexb",
        output_file]
    subprocess.run(mp4_to_h264bitstream)

    # h264_analyze를 통해 h264비트스트림 파일 파싱 명령어
    command = [
        "./h26x_analyze/h264_analyze.exe",
     output_file
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE) #stdout 옵션으로 실행 결과 PIPE에 임시 저장
    result_as_string = result.stdout.decode('latin-1') #result_as_string 변수에 실행결과 저장

    os.remove(output_file)

    # 파싱한 sps, pps 저장할 수 있는 딕셔너리
    sps = {}
    pps = {}

    #프레임 순서 확인을 위한 리스트
    nal_type = []

    #h264_analyze로 파싱한 결과 splutlines()함수를 통해서 줄단위로 나눈 후 리스트로 lines 변수에 저장
    lines =  result_as_string.splitlines()
    #같은 기기에서도 설정에 따라 달라질 수 있는 SPS 구성 요소
    need_del_keys = ['level_idc', 
                    'pic_width_in_mbs_minus1', 
                    'pic_height_in_map_units_minus1', 
                    'frame_cropping_flag',
                    'frame_crop_left_offset',
                    'frame_crop_right_offset',
                    'frame_crop_top_offset',
                    'frame_crop_bottom_offset']

    for i in range(len(lines)):
        if "nal->nal" in lines[i]: # 
             #print(lines[i])
             nal_num = lines[i].replace("\n", "").replace(" ", "").split("->")[1].split(":")[1]
             nal_type.append(int(nal_num))

        if "sps->" in lines[i]:
                splited_sps = lines[i].replace("\n", "").replace(" ", "").split("->")[1].split(":")
            
                if splited_sps[0] == 'profile_idc':
                    nal_ref_idc = lines[i-2].replace("\n", "").replace(" ", "").split("->")[1].split(":")
                    sps['nal_ref_idc'] = nal_ref_idc[1]

                if splited_sps[0] not in need_del_keys:
                    sps[f'{splited_sps[0]}'] = splited_sps[1]

        elif "pps->" in lines[i]:
                splited_pps = lines[i].replace("\n", "").replace(" ", "").split("->")[1].split(":")

                if splited_pps[0] == 'pic_parameter_set_id':
                    nal_ref_idc = lines[i-2].replace("\n", "").replace(" ", "").split("->")[1].split(":")
                    pps['nal_ref_idc'] = nal_ref_idc[1]

                pps[f'{splited_pps[0]}'] = splited_pps[1]
    
    kinds_of_frame={}
    frame_structure = []
    P_frame=[]
    I_frame=[]
    SEI_frame = []
    SPS_frame=[]
    PPS_frame=[]
    AUD_frame=[]
    etc_frame =[]

    bin_data =[]
    hex_data=[]

    for i in range(len(nal_type)):
        
        if i % 2 == 0:
            bin = h264_odd_to_binary(nal_type[i])
            bin_data.append(bin)
        else:
            bin = h264_even_to_binary(nal_type[i])
            bin_data.append(bin)
    
    for i in range(len(bin_data)):
        if i % 2 == 0:
            nal_type = str(bin_data[i]) + str(bin_data[i+1])
            hex_nal = hex(int(nal_type,2))
            hex_data.append(hex_nal)

            if str(bin_data[i+1]) == "00001":
                P_frame.append(hex_nal)
                P_frame = sorted(set(P_frame))
                kinds_of_frame['P_frame'] = P_frame
                frame_structure.append("P")
                
            elif str(bin_data[i+1]) == "00101":
                I_frame.append(hex_nal)
                I_frame = sorted(set(I_frame))
                kinds_of_frame['I_frame'] = I_frame
                frame_structure.append("I")

            elif str(bin_data[i+1]) == "00110":
                SEI_frame.append(hex_nal)
                SEI_frame = sorted(set(SEI_frame))
                kinds_of_frame['SEI_frame'] = SEI_frame
                frame_structure.append("SEI")

            elif str(bin_data[i+1]) == "00111":
                SPS_frame.append(hex_nal)
                SPS_frame = sorted(set(SPS_frame))
                kinds_of_frame['SPS_frame'] = SPS_frame
                frame_structure.append("SPS")

            elif str(bin_data[i+1]) == "01000":
                PPS_frame.append(hex_nal)
                PPS_frame= sorted(set(PPS_frame))
                kinds_of_frame['PPS_frame'] = PPS_frame
                frame_structure.append("PPS")

            elif str(bin_data[i+1]) == "01001":
                AUD_frame.append(hex_nal)
                AUD_frame = sorted(set(AUD_frame))
                kinds_of_frame['AUD_frame'] = AUD_frame
                frame_structure.append("AUD")

            else:
                etc_frame.append(hex_nal)
                etc_frame = sorted(set(etc_frame))
                kinds_of_frame['etc_frame'] = etc_frame
                frame_structure.append("etc")

    for i in range(len(frame_structure)):
        if frame_structure[i] == "P":
            gop_structure = frame_structure[:i+1]
            break

    return kinds_of_frame, gop_structure, sps, pps

def parse_h265_mdat(file_addr):
    output_file = "./temp/bitstream.h265" #삭제하기 전 저장하는 비트스트림 파일 경로

    # ffmpeg 명령어, file_addr의 파일을 h.264 비트스트림으로 전환하여 out_file의 경로에 저장
    mp4_to_h265bitstream = [
        "./ffmpeg/ffmpeg.exe",
        "-i", file_addr,
        "-c:v", "copy",
        "-bsf", "hevc_mp4toannexb",
        output_file]
    subprocess.run(mp4_to_h265bitstream)

    # h264_analyze를 통해 h264비트스트림 파일 파싱 명령어
    command = [
        "./h26x_analyze/h265bitstreamVS.exe",
     output_file
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE) #stdout 옵션으로 실행 결과 PIPE에 임시 저장
    result_as_string = result.stdout.decode('latin-1') #result_as_string 변수에 실행결과 저장
    #print(result_as_string)

    os.remove(output_file)


    nal = []
    nal_unit = []
    vps_line=[]
    vps = {}
    sps_line=[]
    sps = {}
    pps_line=[]
    pps = {}

    #프레임 순서 확인을 위한 리스트
    nal_type = []

    #h265_analyze로 파싱한 결과 splutlines()함수를 통해서 줄단위로 나눈 후 리스트로 lines 변수에 저장
    lines =  result_as_string.splitlines()

    #같은 기기에서도 설정에 따라 달라질 수 있는 SPS 구성 요소
    need_del_keys = ['profile_tier_level( 1, vps_max_sub_layers_minus1 )',
                    '  general_tier_flag', 
                    '  general_level_idc', 
                    'pic_width_in_luma_samples', 
                    'pic_height_in_luma_samples',
                    'tiles_enabled_flag',
                    'num_tile_columns_minus1',
                    'num_tile_rows_minus1',
                    'uniform_spacing_flag',
                    'conformance_window_flag']
    
    for i in range(len(lines)):
        if "nal->nal" in lines[i]: # 
             #print(lines[i])
             nal_num = lines[i].replace("\n", "").split("->")[1].split(":")[1]
             nal_type.append(int(nal_num))

        if "!! Found NAL at offset" in lines[i]:
            nal.append(i)

    for i in range(len(nal)):
        if i != 0:
            nal_unit.append(lines[nal[i-1]:nal[i]])
            
    #print(nal_unit[0:5])

    for x in nal_unit:
        for y in range(len(x)):
            if "VPS:" in x[y]:
                if x[y:] not in vps_line:
                    vps_line.append(x[y+1:])
                
            elif "SPS:" in x[y]:
                if x[y:] not in sps_line:
                    sps_line.append(x[y+1:])

            elif "PPS:" in x[y]:
                if x[y:] not in pps_line:
                    pps_line.append(x[y+1:])


    for i in vps_line[0]:
        data = i.split(":")
        if data[0] not in need_del_keys:
            vps[f'{data[0]}'] = data[1]

    for i in sps_line[0]:
        data = i.split(":")
        if data[0] not in need_del_keys:
            sps[f'{data[0]}'] = data[1]
    
    for i in pps_line[0]:
        data = i.split(":")
        if data[0] not in need_del_keys:
            pps[f'{data[0]}'] = data[1]

    kinds_of_frame={}
    gop_structure = []

    SEI_Frame = [] 
    VPS_Frame = []
    SPS_Frame = []
    PPS_Frame = []
    I_Frame = []
    P_Frame = []
    ETC_Frame = []


    for i in nal_type:
        if i == 32:
            gop_structure.append("VPS")
            if h265_to_binary(i) not in VPS_Frame:
                VPS_Frame.append(h265_to_binary(i))
                VPS_Frame.sort()
            kinds_of_frame['VPS'] = VPS_Frame
            
        elif i == 33:
            gop_structure.append("SPS")
            if h265_to_binary(i) not in SPS_Frame:
                SPS_Frame.append(h265_to_binary(i))
                SPS_Frame.sort()
            kinds_of_frame['SPS'] = SPS_Frame

        elif i == 34:
            gop_structure.append("PPS")
            if h265_to_binary(i) not in PPS_Frame:
                PPS_Frame.append(h265_to_binary(i))
                PPS_Frame.sort()
            kinds_of_frame['PPS'] = PPS_Frame

        elif i in [19, 20]:
            gop_structure.append("I")
            if h265_to_binary(i) not in I_Frame:
                I_Frame.append(h265_to_binary(i))
                I_Frame.sort()
            kinds_of_frame['I'] = I_Frame
            

        elif i in [0,1]:
            gop_structure.append("P")
            if h265_to_binary(i) not in P_Frame:
                P_Frame.append(h265_to_binary(i))
                P_Frame.sort()
            kinds_of_frame['P'] = P_Frame

        elif i == 39:
            gop_structure.append("SEI")
            if h265_to_binary(i) not in SEI_Frame:
                SEI_Frame.append(h265_to_binary(i))
                SEI_Frame.sort()
            kinds_of_frame['SEI'] = SEI_Frame

        else:
            gop_structure.append("ETC")
            if h265_to_binary(i) not in ETC_Frame:
                ETC_Frame.append(h265_to_binary(i))
                ETC_Frame.sort()
            kinds_of_frame['ETC'] = ETC_Frame
    

    structure_end = 0
    for i in range(len(gop_structure)):
        if gop_structure[i] == "P":
            structure_end = i+1
            break
    
    gop_structure = gop_structure[:structure_end]

    return kinds_of_frame, gop_structure, vps, sps, pps

#result = parse_h265_mdat("D:/졸업논문/Galaxy Z Flip 5 종원/20240412_1220331대1.mp4")

#result = parse_h264_mdat("/mnt/d/졸업논문/iPhone_15_Pro/IMG_5761.mov")
#print(result)

# D46_L3S4C4.mp4 이거 이상함
# D46_L3S5C4.mp4 이거 이상함
#M23_Nokia_6.1_A, B 오류가 나는데 해결 방법이 리눅스에선 모르겠음 급하니까 일단 windows ffmpeg로 분석하고 코드 돌려보기
