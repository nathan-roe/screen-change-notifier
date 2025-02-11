import os
from enum import Enum

class NotificationType(Enum):
    SOUND = "Sound"
    VOICE = "Voice"
    SCRIPT = "Script"

class Notification:

    def notify(notification_type: NotificationType, value = "echo Nothing executed"):
        try:
            match notification_type:
                case NotificationType.SOUND.value:
                    os.system('play -nq -t alsa synth {} sine {}'.format(1, 440))
                case NotificationType.VOICE.value:
                    os.system('spd-say "The screen was updated"')
                case NotificationType.SCRIPT.value:
                    os.system(value)
                
        except Exception:
            print("Change was detected. Unable to run notification")