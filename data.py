#data.py 
import os

def create_data(folder_path):
    data = []
    
    for folder_name in os.listdir(folder_path):
        folder_dir = os.path.join(folder_path, folder_name)

        if os.path.isdir(folder_dir):
            for file_name in os.listdir(folder_dir):
                if file_name.endswith('.wav'):
                    file_path = os.path.join(folder_dir, file_name)
                    entry = {
                        "question": f"Is this a {folder_name}?",
                        "sound": file_path,
                        "choices": ["Yes", "No", "Maybe"],
                    }
                    data.append(entry)

    return data

