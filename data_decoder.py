def decode(data):  
    filtered_data = []

    for i in data:
        if i >= 32 and i <= 126:
            filtered_data.append(i)

    # 바이트로 변환
    bytes_data = bytes(filtered_data)
    decoded_data = bytes_data.decode('latin-1')

    return decoded_data