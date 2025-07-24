import tkinter as tk
from tkinter import messagebox
import speedtest
from datetime import datetime
import logging

# file handler and stream handler setup
logger = logging.getLogger("Internet_Speed_Test_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("internet_speed_test.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

class SpeedCheckError(Exception):
    """Custom exception class for internet speed test related errors."""
    pass

class InternetSpeedTest:
    """GUI based internet speed testing application."""

    def __init__(self, root):
        """Initializes the GUI and setup widgets."""
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("500x600")
        self.root.config(bg="blue")

        self.create_widgets()

    def create_widgets(self):
        """Creates GUI components like labels and buttons."""
        self.lab_title = tk.Label(self.root,text="Internet Speed Test", 
                                    font=("Time New Roman", 30, "bold"),
                                    bg="blue", fg="white")
        self.lab_title.place(x=60, y=40, height=50,width=380)

        self.lab_down = tk.Label(self.root,text="Download Speed", 
                                  font=("Time New Roman", 30, "bold"), 
                                  bg="blue", fg="white")
        self.lab_down.place(x=60, y=130, height=50, width=380)

        self.lab_down_value = tk.Label(self.root,text="00 Mbps", 
                               font=("Time New Roman", 30, "bold"),
                               bg="blue", fg="white")
        self.lab_down_value.place(x=60, y=200, height=50, width=380)

        self.lab_up = tk.Label(self.root,text="Upload Speed",
                                font=("Time New Roman", 30, "bold"), 
                                bg="blue", fg="white")
        self.lab_up.place(x=60, y=290, height=50, width=380)

        self.lab_up_value = tk.Label(self.root,text="00 Mbps", 
                                       font=("Time New Roman", 30, "bold"), 
                                       bg="blue", fg="white")
        self.lab_up_value.place(x=60, y=360, height=50, width=380)

        self.check_button = tk.Button(self.root, text="Check Speed", 
                                        font=("Time New Roman", 30, "bold"), 
                                        relief=tk.RAISED, bg="red", command=self.run_speed_check)
        self.check_button.place(x=60, y=460, height=50, width=380)

    def run_speed_check(self):
        """Perform speed test and updates the GUI with results."""
        try:
            logger.info("Starting Speed Test")
            st = speedtest.Speedtest()
            st.get_servers()
            download_speed = round(st.download()/(10**6), 3)
            upload_speed = round(st.upload()/(10**6), 3)

            self.lab_down_value.config(text=f"{download_speed} Mbps")
            self.lab_up_value.config(text=f"{upload_speed} Mbps")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{timestamp}] Download: {download_speed}, Upload: {upload_speed}")
        except Exception as e:
            logger.error("An Unexpected error occurred during internet speed test: %s", e, exc_info=True)
            messagebox.showerror("Error", "Speed test failed. Please check your internet connection.")
            print(str(e))
            raise SpeedCheckError("Speed Test Failed.") 


if __name__ == "__main__":
        """Main entry point to run the speed test app."""
        root = tk.Tk()
        app = InternetSpeedTest(root)
        root.mainloop()