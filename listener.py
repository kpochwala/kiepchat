import time, json, os, pytz, argparse

from lcd2usb import LCD
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

def initialize_chat_file(chat_file_path: str) -> None:
    if os.path.isfile(chat_file_path):
        raise FileExistsError(f"Chat file already exists: {chat_file_path}")
    
    initial_json = {}
    messages = []
    initial_json["messages"] = messages
    
    with open(chat_file_path, "w") as file:
        json.dump(initial_json, file, indent = 4)

def reorder_lines(data: str) -> str:
    padded_data = f"{data: <80}"
    split_data = [padded_data[i:i+20] for i in range(0, len(padded_data), 20)]
    return f"{split_data[0]}{split_data[2]}{split_data[1]}{split_data[3]}"

def format_timestamp_to_local_time(timestamp_ms_since_epoch: int) -> str:
    seconds_since_epoch = timestamp_ms_since_epoch / 1000
    utc_time_object = datetime.utcfromtimestamp(seconds_since_epoch)    
    europe_warsaw_timezone = pytz.timezone('Europe/Warsaw')
    localized_time_object = pytz.utc.localize(utc_time_object).astimezone(europe_warsaw_timezone)
    formatted_time = localized_time_object.strftime('%H:%M')
    return formatted_time

def format_json_to_lcd(data: dict) -> str:
    all_lines = ""
    for message in data["messages"]:
        formatted_time = format_timestamp_to_local_time(message["timestamp"])
        formatted = f"{formatted_time}:{message['username'][:3]}: {message['message']}"[:20]
        print(formatted)
        all_lines = f"{all_lines}{formatted: <20}"
    return reorder_lines(all_lines)

class  MyHandler(FileSystemEventHandler):
    current_lcd_data = ""
    def  on_modified(self,  event):
        if False == os.path.isfile(event.src_path):
            return
        with open(event.src_path, "r") as file:
            data = json.load(file)
            print(data)
            
            lcd = LCD()
            received_data = format_json_to_lcd(data)
            if received_data != self.current_lcd_data:
                lcd.clear()
                lcd.write(received_data)
                self.current_lcd_data = received_data
        #  print(f'event type: {event.event_type} path : {event.src_path}')

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser(description='LCD2USB chat.')
    parser.add_argument('--chat_file', type=str, default='chat.json', help='Path to the chat file (default: chat.json)')    
    args = parser.parse_args()

    try:
        initialize_chat_file(args.chat_file)
    except FileExistsError:
        pass

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler,  path=args.chat_file,  recursive=False)
    observer.start()

    try:
        while  True:
            time.sleep(1)
    except  KeyboardInterrupt:
       observer.stop()
    observer.join()