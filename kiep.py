import os, time, json, argparse

def initialize_chat_file(chat_file_path: str) -> None:
    if os.path.isfile(chat_file_path):
        raise FileExistsError(f"Chat file already exists: {chat_file_path}")
    
    initial_json = {}
    messages = []
    initial_json["messages"] = messages
    
    with open(chat_file_path, "w") as file:
        json.dump(initial_json, file, indent = 4)

def parse_message(message: str) -> dict:
    username = os.environ.get("USER")[:3]
    timestamp = time.time_ns() // 1_000_000

    message_dict = {}
    message_dict["username"] = username
    message_dict["message"] = message
    message_dict["timestamp"] = timestamp

    return message_dict

def append_message(message_dict: dict, chat_file_path: str) -> None:
    existing_data = {}
    with open(chat_file_path, "r") as file:
        existing_data = json.load(file)

    existing_data["messages"].append(message_dict)
    existing_data["messages"] = existing_data["messages"][-4:]

    with open(chat_file_path, "w") as file:
        json.dump(existing_data, file, indent = 4)

    print(existing_data)

def main():
    parser = argparse.ArgumentParser(description='LCD2USB chat.')
    parser.add_argument('--chat_file', type=str, default='chat.json', help='Path to the chat file (default: chat.json)')
    parser.add_argument('--message', type=str, help='Message to send') 
    args = parser.parse_args()

    try:
        initialize_chat_file(args.chat_file)
    except FileExistsError:
        pass
    message = args.message
    if message is None:
        message = input("Enter message: ")
    
    message_dict = parse_message(message)

    append_message(message_dict, args.chat_file)



if __name__ == "__main__":
    main()