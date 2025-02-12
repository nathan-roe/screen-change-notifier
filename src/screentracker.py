import os
import uuid
import pyautogui
import pygame
import cv2
import numpy as np
import time
import shutil
import threading
import tkinter as tk
from wordscanner import WordScanner 
from detectiontype import DetectionPreference, DetectionType

class ScreenTracker(threading.Thread):
    def __init__(self, root: tk.Tk, freq: float, detect_pref: DetectionPreference, on_start, on_complete):
        super().__init__()
        self.detect_pref = detect_pref
        self.signal = True
        self.freq = 0 if freq <= 2 else freq \
            if detect_pref.type == DetectionType.DISPLAY \
            else 0 if freq <= 5 else freq
            
        self.on_start = on_start
        self.on_complete = on_complete
        self.tmp_dir = f'{os.path.dirname(os.path.realpath(__file__))}/tmp'
        self.tk_root = root
        self.create_tmp_dir()

    def __del__(self):
        self.stop()

    def select_region(self):
        file_name = f'{uuid.uuid4()}.png'
        self.take_screenshot(file_name, (
            0, 0,
            self.tk_root.winfo_screenwidth(),
            self.tk_root.winfo_screenheight()
        ))

        pygame.init()
        screen = pygame.display.set_mode((
            self.tk_root.winfo_screenwidth(),
            self.tk_root.winfo_screenheight()
        ))
        pygame.display.set_caption("Select area to track")
        background_image = pygame.image.load(file_name)

        drawing = False
        start_pos = (0, 0)
        end_pos = (0, 0)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        drawing = True
                        start_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        drawing = False
                        end_pos = event.pos
                        pygame.quit()
                        os.remove(file_name)
                        return (start_pos, end_pos)
                elif event.type == pygame.MOUSEMOTION:
                    if drawing:
                        end_pos = event.pos
            screen.blit(background_image, (0, 0))

            if drawing:
                rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                pygame.draw.rect(screen, "#0bae4a", rect, 2)
            pygame.display.flip()
        os.remove(file_name)
        pygame.quit()
        return (0, 0)

    def take_screenshot(self, file_name: str, region: tuple[int, int, int, int]):
        try:
            screenshot = pyautogui.screenshot(region=region) # region=(0,0,0,0)
            screenshot.save(file_name)

        except Exception as e:
            print(f'An error has occurred {e}')

    def run(self):
        region = self.select_region()
        ref_path = f'{uuid.uuid4()}.png'
        start_pos, end_pos = region
        formatted_region = (
            start_pos[0],
            start_pos[1],
            end_pos[0] - start_pos[0],
            end_pos[1] - start_pos[1]
        )
        self.take_screenshot(ref_path, formatted_region)
        self.on_start()
        self.check_screen_change(ref_path, formatted_region)

    def check_screen_change(self, ref_path: str, formatted_region: tuple[int, int, int, int]):
        self.signal = True
        while self.signal:
            time.sleep(self.freq)
            start_time = time.perf_counter()
            monitor_path = f'{uuid.uuid4()}.png'
            self.take_screenshot(monitor_path, formatted_region)
            detected_change = self.detect_change(ref_path, monitor_path)
            os.remove(monitor_path)
            if(detected_change):
                os.remove(ref_path)
                self.stop(change_detected=True)
                end_time = time.perf_counter()
                print(end_time - start_time)
  
    def detect_change(self, ref_path: str, monitor_path: str):
        match self.detect_pref.type:
            case DetectionType.TEXT.value:
                return self.detect_pref.value in WordScanner.scan(monitor_path)
            case DetectionType.DISPLAY.value:
                return not self.check_image_equality(ref_path, monitor_path)

    def stop(self, change_detected = False):
        self.clear_monitor_files()
        self.signal = False
        self.on_complete(change_detected)

    def check_image_equality(self, img_path1: str, img_path2: str):
        img1 = cv2.imread(img_path1)
        img2 = cv2.imread(img_path2)

        if img1 is None or img2 is None or img1.shape != img2.shape:
            return False
        return not np.any(cv2.subtract(img1, img2))

    def create_tmp_dir(self):
        os.makedirs(self.tmp_dir, exist_ok=True)

    def clear_monitor_files(self):
        shutil.rmtree(self.tmp_dir)