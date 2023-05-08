import json

class SaveManager:
    def __init__(self):
        self.__filePath = './json/setting.json'
        self.__data = {'backgroundColor' : [0, 80, 0], 
                         'screenSize' : [650, 400]}
        
    def status(self):
        print(self.__data)
        
    def write(self, data):# 나중에 data를 받아오게끔 수정
        self.__data = data
        with open(self.__filePath, "w") as f:
            json.dump(self.__data, f, indent = 4)
            
    def read(self):
        with open(self.__filePath, "r") as f:
            return json.load(f)
          

save = SaveManager()

if __name__ == "__main__":
    # 여기서 테스트
    test = SaveManager()
    test.write()