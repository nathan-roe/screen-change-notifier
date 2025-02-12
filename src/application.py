import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from time import sleep
from screentracker import ScreenTracker
from notification import NotificationType, Notification
from detectiontype import DetectionType, DetectionPreference

class Application:
    def __init__(self):
        self.running = False
        self.run_button = None
        self.root = self.create_window()
        self.frequency = tk.DoubleVar(value=5.0)
        self.detection_type = tk.StringVar(value=DetectionType.DISPLAY.value)
        self.detection_value = tk.StringVar()
        self.notification_type = tk.StringVar(value=NotificationType.SOUND.value)
        self.notification_value = tk.StringVar()
        self.create_components()
        self.root.mainloop()


    def create_window(self):
        root = ThemedTk(theme="yaru", background=True)
        root.title("Screen Notifier")
        root.geometry("500x200")
        root.resizable(False, False)
        frame = ttk.Frame(root, width=500, height=200)
        frame.pack(padx=10, pady=10)
        return frame

    def create_components(self):
        ttk.Label(self.root, text = "Refresh Rate in Seconds:").place(x=20, y=20)
        frequency_input = ttk.Entry(self.root, textvariable=self.frequency)
        frequency_input.place(x=200, y=20, width=90)

        ttk.Label(self.root, text = "Detection Type:").place(x=20, y=60)
        detection_type_menu = ttk.OptionMenu(self.root, self.detection_type, 0, *[option.value for option in DetectionType])
        detection_type_menu.place(x=200, y=60, width=90)
        detection_type_menu["menu"].configure(relief="flat", bg="white")
        detection_input = ttk.Entry(self.root, textvariable=self.detection_value)
        self.detection_type.trace('w', lambda *_, var=self.detection_type: self.update_detection_display(self.detection_type.get(), detection_input))

        ttk.Label(self.root, text = "Notification Type:").place(x=20, y=100)
        notification_type_menu = ttk.OptionMenu(self.root, self.notification_type, 0, *[option.value for option in NotificationType])
        notification_type_menu.place(x=200, y=100, width=90)
        notification_type_menu["menu"].configure(relief="flat", bg="white")
        notification_input = ttk.Entry(self.root, textvariable=self.notification_value)
        self.notification_type.trace('w', lambda *_, var=self.notification_type: self.update_notification_display(self.notification_type.get(), notification_input))


        self.run_button = ttk.Button(self.root, text="Record", command=self.track_screen)
        self.run_button.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)

    def update_detection_display(self, type: DetectionType, input: ttk.Entry):
        if type == DetectionType.DISPLAY.value:
            input.place_forget()
        else:
            input.place(x=300, y=60, width=180)
        input.update()

    def update_notification_display(self, type: NotificationType, input: ttk.Entry):
        if type == NotificationType.SCRIPT.value:
            input.place(x=300, y=100, width=180)
        else:
            input.place_forget()
        input.update()

    def allow_input_events(self, allow: bool):
        for el in self.root.winfo_children():
                if el != self.run_button:
                    el.config(state=tk.NORMAL if allow else tk.DISABLED)

    def track_screen(self):
        self.allow_input_events(False)
        self.run_button.config(text="Starting...", command=None)
        self.run_button.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
        self.run_button.update()
        sleep(2)
        detect_pref = DetectionPreference(self.detection_type.get(), self.detection_value.get())
        self.tracker = ScreenTracker(self.root, self.frequency.get(), detect_pref, self.on_process_start, self.on_process_complete)
        self.running = True
        self.tracker.start()

    def on_process_start(self):
        if self.run_button != None:
            self.run_button.config(text="Stop Recording", command=self.tracker.stop)
            self.run_button.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
            self.run_button.update()

    def on_process_complete(self, change_detected):
        self.allow_input_events(True)
        if(change_detected):
            Notification.notify(self.notification_type.get(), self.notification_value.get())
        self.run_button.config(text="Record", command=self.track_screen)
        self.run_button.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
        self.run_button.update()