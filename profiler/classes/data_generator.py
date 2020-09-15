import random
import string

class DataGenerator:

    def __init__(self):
        data = []

    def generate_string(self, string_length=5):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))

    def generate_boolean(self):
        choices = (True, False)
        return random.choice(choices)

    def generate_random_data(self, string_length=5, num_results=5):
        for i in range(num_results):
            self.data.append(self.generate_string(string_length))
        return self.data
        
