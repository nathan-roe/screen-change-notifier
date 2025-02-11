## Screen Change Notifier

### Purpose
- This is a Linux application used for executing commands when a selected portion of a screen display changes. Users have the ability to analyze a page for specific text changes, or run logic when the display is modified within a specified region.

### Getting Started
- Execute the scripts/gendist.sh script. This will create the executable file used to run the application.
- Execute the scripts/setup.sh script to configure system files and add the application to the Linux Application Menu.

### Libraries
  - pytesseract: Converts screen captures into text for use in the notification handling.
  - cv2: Used to detect changes between two images.
  - tkinter: Creates and displays the desktop application.
  - pyinstaller: Generates a single executable file through the scripts/gendist shell script.
  - gnome-screenshot: A custom implementation has been built for this project, to ensure animations aren't present when running this application. The scripts/setup shell script will configure this and other related system files.
  - pygame: Generates event loops while running the application.