import os

class saveSettingManager:
    #파일의 내용을 저장하고 가져오는 클래스
    def __init__(self):
        self.__fileName = "saveFile/settingFile.txt"
        self.__backgroundColor = None
        self.__inputKey = None

        
    def write(self, text):
        with open(self.__fileName, "w") as f:
            f.write(text)
            
    def read(self):
        with open(self.__fileName, "r") as f:
            return f.read()