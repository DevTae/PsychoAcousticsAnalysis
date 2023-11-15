import os
import threading

# python -m pip install pygame
# pip install pygame -i https://pypi.python.org/simple/
import pygame
import time


# 파일 이름 읽기
mp3_file_name = os.path.join("demo", "test1.mp3")
event_file_name = mp3_file_name.replace(".mp3", ".txt")


# 이벤트 읽기
index = 0
events = []

with open(event_file_name, "r") as f:
    for line in f.readlines():
        start_time, haptic_type, haptic_level, duration = line.split(',')
        duration = duration.replace("\n", "")

        # 값 읽어오기
        start_time = float(start_time) * 1000
        duration = float(duration) * 1000

        events.append((start_time, haptic_type, haptic_level, duration))


# mp3 파일 총 시간 구하기
pygame.init()
sound = pygame.mixer.Sound(mp3_file_name)
total_duration = sound.get_length()

# mp3 파일 재생하기
pygame.mixer.music.load(mp3_file_name)
pygame.mixer.music.play()
start_time = time.time()

# 이벤트 탐지하여 출력하기
for event in events:
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        elapsed_time *= 1000
        if elapsed_time >= event[0]:
            print(f"[log] {event[1]} 타입의 {event[2]} 단계 이벤트 발생! {round(elapsed_time, 2)}")
            if elapsed_time > event[0] + event[3]:
                break
        time.sleep(0.025)

# 재생이 끝날 때까지 기다리기
while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time >= total_duration:
        break

pygame.mixer.music.stop()
pygame.quit()
