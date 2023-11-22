prefix_file_name = "test5"

fusion_result_file = prefix_file_name + "_fusion_result.txt"

audio_result_file = prefix_file_name + "_audio_result.txt"
vision_temp_result_file = prefix_file_name + "_vision_temp_result.txt"
vision_wind_result_file = prefix_file_name + "_vision_wind_result.txt"
silency_result_file = prefix_file_name + "_silency_result.txt" 


# [0] timestamp, [1] effect, [2] strength, [3] duration
audio_result = list()

# [0] timestamp, [1] effect, [2] (temp1, temp2), [3] duration
vision_temp_result = list()

# [0] timestamp, [1] effect, [2] strength, [3] duration
vision_wind_result = list()

# [0] timestamp, [1] (loc1, loc2, ... (delimeter='|')), [2] duration
silency_result = list()


try:
    with open(audio_result_file, "r") as f:
        for line in f.readlines():
            timestamp, effect, strength, duration = line.split(',')
            duration = duration.replace("\n", "")
            audio_result.append((float(timestamp), effect, strength, float(duration)))
except:
    pass

try:
    with open(vision_temp_result_file, "r") as f:
        for line in f.readlines():
            if len(line.split(',')) == 3: # [ timestamp, temp1, temp2 ] 
                effect = "ta"
                duration = 0.03
                timestamp, temp1, temp2 = line.split(',')
                temp2 = temp2.replace("\n", "")
                vision_temp_result.append((float(timestamp), effect, (float(temp1), float(temp2)), duration))
            elif len(line.split(',')) == 5: # [ timestamp, temp1, temp2, duration, direction ]
                effect = "ta"
                timestamp, temp1, temp2, duration, direction = line.split(',')
                direction = direction.replace("\n", "")
                vision_temp_result.append((float(timestamp), effect, (float(temp1), float(temp2)), float(duration), direction))
            else:
                raise Exception("not supported vision_temp_result file")
except:
    pass

try:
    with open(vision_wind_result_file, "r") as f:
        for line in f.readlines():
            timestamp, effect, strength, duration = line.split(',')
            duration = duration.replace("\n", "")
            vision_wind_result.append((float(timestamp), effect, strength, float(duration)))
except:
    pass

try:    
    with open(silency_result_file, "r") as f:
        for line in f.readlines():
            timestamp, location, duration = line.split(',')
            duration = duration.replace("\n", "")
            location = location.split('|')
            silency_result.append((float(timestamp), location, float(duration)))
except:
    pass

    
"""
[0] timestamp
[1-8] va (액츄에이터)
[9-10] pa (솔레노이드)
[11-12] ta (온도)
[13-14] wa (바람)
"""
fusion_result = list()

video_total_length = 100 # 시연 동영상 길이
now_timestamp = 0
frame_interval = 0.1 # 100ms 기준으로 자르기
solenoid_proper_duration = 0.25 # 적어도 0.25초마다 이벤트가 변화되도록 설정

audio_result_index = 0
vision_temp_result_index = 0
vision_wind_result_index = 0
silency_result_index = 0

while now_timestamp <= video_total_length:
    # 현재 timestamp 에 맞는 index 찾기
    while len(audio_result) > audio_result_index + 1 and now_timestamp > audio_result[audio_result_index][0] + audio_result[audio_result_index][3]:
        audio_result_index += 1
    while len(vision_temp_result) > vision_temp_result_index + 1 and now_timestamp > vision_temp_result[vision_temp_result_index][0] + vision_temp_result[vision_temp_result_index][3]:
        vision_temp_result_index += 1
    while len(vision_wind_result) > vision_wind_result_index + 1 and now_timestamp > vision_wind_result[vision_wind_result_index][0] + vision_wind_result[vision_wind_result_index][3]:
        vision_wind_result_index += 1
    while len(silency_result) > silency_result_index + 1 and now_timestamp > silency_result[silency_result_index + 1][0]: # 다음 시작점을 넘기면 silency index 변경
        silency_result_index += 1

    fusion = [now_timestamp,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0,
              0, 0,
              0, 0]

    # 오디오 이벤트에 해당되는 이벤트 연산 진행
    if len(audio_result) > audio_result_index:
        audio_event = audio_result[audio_result_index]
        event_timestamp = audio_event[0]
        effect = audio_event[1]
        strength = audio_event[2]
        max_strength = 255
        duration = audio_event[3]
        if event_timestamp <= now_timestamp and now_timestamp <= event_timestamp + duration:
            if effect == "va|pa":
                for i in range(1, 8 + 1):
                    fusion[i] = round(float(strength.split('|')[0]) * max_strength)
                for i in range(9, 10 + 1):
                    # 솔레노이드 들썩들썩 효과 연출을 위한 조건문 추가 (최소 효과 유지 시간 추가)
                    if len(fusion_result) > 0 and fusion_result[-1][i] == 0:
                        solenoid_push_start_time = now_timestamp
                    elif len(fusion_result) == 0:
                        solenoid_push_start_time = now_timestamp
    
                    if now_timestamp - solenoid_push_start_time > solenoid_proper_duration:
                        fusion[i] = 0
                    else:
                        fusion[i] = round(float(strength.split('|')[1]) * max_strength)
                        
            elif effect == "va":
                for i in range(1, 8 + 1):
                    fusion[i] = round(float(strength) * max_strength)

    # 비전에서의 온도 이벤트에 해당되는 이벤트 연산 진행
    # 0 : 아무 온도도 아님
    # 1 : 뜨거운 것
    # 2 : 차가운 것
    if len(vision_temp_result) > vision_temp_result_index:
        vision_temp_event = vision_temp_result[vision_temp_result_index]

        if len(vision_temp_event) == 4: # [ timestamp, effect, (temp1, temp2), duration ]
            event_timestamp = vision_temp_event[0]
            effect = vision_temp_event[1]
            temp1, temp2 = vision_temp_event[2]
            duration = vision_temp_event[3]
            if event_timestamp <= now_timestamp and now_timestamp <= event_timestamp + duration:
                if effect == "ta":
                    for i in range(11, 12 + 1):
                        if temp1 < temp2:
                            fusion[i] = 1
                        else:
                            fusion[i] = 2
                        # 일단 온도 부분 이렇게 설정해두었습니다.
                        #fusion[i] = str(temp1) + "|" + str(temp2)
        elif len(vision_temp_event) == 5: # [ timestamp, effect, (temp1, temp2), duration, direction [
            event_timestamp = vision_temp_event[0]
            effect = vision_temp_event[1]
            temp1, temp2 = vision_temp_event[2]
            duration = vision_temp_event[3]
            direction = vision_temp_event[4] # 온열 및 냉각 방향
            if event_timestamp <= now_timestamp and now_timestamp <= event_timestamp + duration:
                if effect == "ta":
                    if direction == "l":
                        if temp1 < temp2: # 뜨거운 상황
                            fusion[11] = 1
                            fusion[12] = 0
                        elif temp1 > temp2: # 차가운 상황
                            fusion[11] = 2
                            fusion[12] = 0
                    elif direction == "r":
                        if temp1 < temp2: # 뜨거운 상황
                            fusion[11] = 0
                            fusion[12] = 1
                        elif temp1 > temp2: # 차가운 상황
                            fusion[11] = 0
                            fusion[12] = 2
                    elif direction == "lr":
                        if temp1 < temp2: # 뜨거운 상황
                            fusion[11] = 1
                            fusion[12] = 1
                        elif temp1 > temp2: # 차가운 상황
                            fusion[11] = 2
                            fusion[12] = 2
                    else:
                        raise Exception("not supported vision_temp_event format")
        else:
            raise Exception("not supported vision_temp_event format")
    
    # 비전에서의 바람 이벤트에 해당되는 이벤트 연산 진행
    if len(vision_wind_result) > vision_wind_result_index:
        vision_wind_event = vision_wind_result[vision_wind_result_index]
        event_timestamp = vision_wind_event[0]
        effect = vision_wind_event[1]
        strength = vision_wind_event[2]
        duration = vision_wind_event[3]
        if event_timestamp <= now_timestamp and now_timestamp <= event_timestamp + duration:
            if effect == "wa":
                for i in range(13, 14 + 1):
                    fusion[i] = strength
    
    # silency detection 을 바탕으로 액츄에이터 위치 조절
    if len(silency_result) > silency_result_index:
        silency_info = silency_result[silency_result_index]
        event_timestamp = silency_info[0]
        location = silency_info[1]
        duration = silency_info[2]
        if event_timestamp <= now_timestamp and now_timestamp <= event_timestamp + duration:
            # location 에 해당되는 액츄에이터의 경우 신호를 끄게 됨
            if "va" not in location:
                for i in range(1, 8+1):
                    if fusion[i] != 0 and (("v" + str(i-1)) not in location):
                        fusion[i] = 0
    
    fusion_result.append(fusion)

    now_timestamp += frame_interval
    now_timestamp = round(now_timestamp, 3)
    
"""
[0] timestamp
[1-8] va (액츄에이터)
[9-10] pa (솔레노이드)
[11-12] ta (온도)
[13-14] wa (바람)
"""
# 계산된 fusion 데이터 파일로 쓰기
with open(fusion_result_file, "w") as f:
    for fusion in fusion_result:
        f.write(str(fusion[0]) + "," + str(fusion[1]) + "," + \
                str(fusion[2]) + "," + str(fusion[3]) + "," + \
                str(fusion[4]) + "," + str(fusion[5]) + "," + \
                str(fusion[6]) + "," + str(fusion[7]) + "," + \
                str(fusion[8]) + "," + str(fusion[9]) + "," + \
                str(fusion[10]) + "," + str(fusion[11]) + "," + \
                str(fusion[12]) + "," + str(fusion[13]) + "," + \
                str(fusion[14]) + "\n")
