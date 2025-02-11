import tkinter as tk
from time import sleep
from screentracker import ScreenTracker
from notification import NotificationType, Notification
from detectiontype import DetectionType, DetectionPreference

class Application:
    def __init__(self):
        self.running = False
        self.run_button = None
        self.root = self.create_window()
        self.frequency = tk.DoubleVar(value=0.5)
        self.detection_type = tk.StringVar(value=DetectionType.DISPLAY.value)
        self.detection_value = tk.StringVar()
        self.notification_type = tk.StringVar(value=NotificationType.SOUND.value)
        self.notification_value = tk.StringVar()
        self.create_components()
        self.root.mainloop()


    def create_window(self):
        root = tk.Tk()
        root.title("Screen Notifier")
        root.geometry("500x200")
        root.resizable(False, False)
        return root

    def create_components(self):
        tk.Label(self.root, text = "Refresh Rate in Seconds:").place(x=20, y=40)
        frequency_input = tk.Entry(self.root, textvariable=self.frequency)
        frequency_input.place(x=200, y=40, width=90, height=25)

        tk.Label(self.root, text = "Detection Type:").place(x=20, y=80)
        detection_type_menu = tk.OptionMenu(self.root, self.detection_type, *[option.value for option in DetectionType])
        detection_type_menu.place(x=200, y=80, width=90, height=26)
        detection_input = tk.Entry(self.root, textvariable=self.detection_value)
        self.detection_type.trace('w', lambda *_, var=self.detection_type: self.update_detection_display(self.detection_type.get(), detection_input))

        tk.Label(self.root, text = "Notification Type:").place(x=20, y=120)
        notification_type_menu = tk.OptionMenu(self.root, self.notification_type, *[option.value for option in NotificationType])
        notification_type_menu.place(x=200, y=120, width=90, height=26)
        notification_input = tk.Entry(self.root, textvariable=self.notification_value)
        self.notification_type.trace('w', lambda *_, var=self.notification_type: self.update_notification_display(self.notification_type.get(), notification_input))


        self.run_button = tk.Button(self.root, text="Record", command=self.track_screen)
        self.run_button.place(x=410, y=165)

    def update_detection_display(self, type: DetectionType, input: tk.Entry):
        if type == DetectionType.DISPLAY.value:
            input.place_forget()
        else:
            input.place(x=300, y=80, width=145, height=25)
        input.update()

    def update_notification_display(self, type: NotificationType, input: tk.Entry):
        if type == NotificationType.SCRIPT.value:
            input.place(x=300, y=120, width=145, height=25)
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
        self.run_button.place(x=390, y=165)
        self.run_button.update()
        sleep(2)
        detect_pref = DetectionPreference(self.detection_type.get(), self.detection_value.get())
        self.tracker = ScreenTracker(self.root, self.frequency.get(), detect_pref, self.on_process_complete)
        self.running = True
        if self.run_button != None:
            self.run_button.config(text="Stop Recording", command=self.tracker.stop)
            self.run_button.place(x=365, y=165)
            self.run_button.update()
        self.tracker.start()
        
    def on_process_complete(self, change_detected):
        self.allow_input_events(True)
        if(change_detected):
            Notification.notify(self.notification_type.get(), self.notification_value.get())
        self.run_button.config(text="Record", command=self.track_screen)
        self.run_button.place(x=410, y=165)
        self.run_button.update()