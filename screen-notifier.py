import os
import uuid
import pyautogui
import pygame
import tkinter as tk
import cv2
import numpy as np
import time
import shutil
import threading

class ScreenTracker(threading.Thread):
	def __init__(self, root, freq, callback):
		super().__init__()
		self.signal = True
		self.freq = freq
		self.callback = callback
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
				pygame.draw.rect(screen, (0, 0, 0), rect, 2)
			pygame.display.flip()
		pygame.quit()
		return (0, 0)

	def take_screenshot(self, file_name, region):
		try:
			screenshot = pyautogui.screenshot(region=region) # region=(0,0,0,0)
			print(screenshot)
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

		self.signal = True
		while self.signal:
			time.sleep(self.freq)
			monitor_path = "equality-check.png"
			self.take_screenshot(monitor_path, formatted_region)
			if(not self.check_image_equality(ref_path, monitor_path)):
				print("Area was updated")
				self.stop(change_detected=True)
	
	def stop(self, change_detected = False):
		self.clear_monitor_files()
		self.signal = False
		self.callback(change_detected)

	def check_image_equality(self, img_path1, img_path2):
		img1 = cv2.imread(img_path1)
		img2 = cv2.imread(img_path2)

		if img1 is None or img2 is None or img1.shape != img2.shape:
			return False
		return not np.any(cv2.subtract(img1, img2))

	def create_tmp_dir(self):
		os.makedirs(self.tmp_dir, exist_ok=True)

	def clear_monitor_files(self):
		shutil.rmtree(self.tmp_dir)

class Notification:
	def __init__(self):
		pass

	def notify(self):
		try:
			os.system('play -nq -t alsa synth {} sine {}'.format(1, 440))
		except Exception:
			print("Change was detected. Unable to play sound")

	def notify_voice(self):
		try:
			os.system('spd-say "The screen was updated"')
		except Exception:
			self.notify()

class Application:
	def __init__(self):
		self.running = False
		self.run_button = None
		self.notification = Notification()
		self.root = self.create_window()
		self.frequency = tk.DoubleVar(value=0.5)
		self.create_components()
		self.root.mainloop()


	def create_window(self):
		root = tk.Tk()
		root.title("Screen Notifier")
		root.geometry("375x200")
		return root

	def create_components(self):
		tk.Label(self.root, text = "Refresh Rate in Seconds:").place(x=20, y=40)
		tk.Entry(self.root, textvariable=self.frequency).place(x=200, y=40)
		self.run_button = tk.Button(self.root, text="Record", command=self.track_screen)
		self.run_button.place(x=290, y=165)

	def track_screen(self):
		if self.run_button != None:
			self.run_button.config(text="Starting...", command=None)
			self.run_button.place(x=275, y=165)
			self.run_button.update()
		self.tracker = ScreenTracker(self.root, self.frequency.get(), self.on_process_complete)
		self.running = True
		print("button: ", self.run_button)
		if self.run_button != None:
			self.run_button.config(text="Stop Recording", command=self.tracker.stop)
			self.run_button.place(x=240, y=165)
			self.run_button.update()
		self.tracker.start()
		
	def on_process_complete(self, change_detected):
		if(change_detected):
			self.notification.notify_voice()
		self.run_button.config(text="Record", command=self.track_screen)
		self.run_button.place(x=290, y=165)
		self.run_button.update()

application = Application()