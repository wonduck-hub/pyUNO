import os

class saveSettingManager:
    #파일의 내용을 저장하고 가져오는 클래스
    def __init__(self, ):
        self.fileName = "saveFile/settingFile.txt"
        
    def write(self, text):
        with open(self.file_path, "w") as f:
            f.write(text)
            
    def read(self):
        with open(self.file_path, "r") as f:
            return f.read()