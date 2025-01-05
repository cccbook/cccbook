import os

def safe_exec(file_path):
    allowed_files = ['/safe/directory/file1.py', '/safe/directory/file2.py']
    if file_path in allowed_files:
        with open(file_path, 'r') as file:
            exec(file.read())
    else:
        print("Attempted to execute an untrusted file!")
