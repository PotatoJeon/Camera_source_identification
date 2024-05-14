def container_classify(target_video):
    if target_video[0:4] == b"RIFF":
        return "avi"
    
    #mp4, mov
    elif target_video[4:8] == b"ftyp":

        if target_video[8:12] == b"qt  ":
            return "mov"
        
        else:
            return "mp4"