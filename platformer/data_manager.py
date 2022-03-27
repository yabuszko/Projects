import json

class Data_Manager:
    def __init__(self):
        self.data = {}

    def save_data(self, levels_completed, coins):
        self.data = {'levels_completed' : levels_completed,
                    'coins' : coins}
        
        with open('others/data.txt', 'w') as file:
            json.dump(self.data, file)
    
    def load_data(self):
        with open('others/data.txt') as file:
            data = json.load(file)
            return data
