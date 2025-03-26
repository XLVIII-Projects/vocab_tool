import json
from create_word import Creator
import random
import csv

class Tester:
    def __init__(self):
        # with open("words_created.json", "r") as file2:
        #     self.words_created = json.load(file2) 

        # with open("mastery.json", "r") as file3:
        #     self.mastery = json.load(file3)

        # with open ("words_list_exp.csv", "r") as file1:
        #     self.words_list = list(csv.reader(file1))
        pass

    def get_initial_word(self, mastery, words_list, words_created):
        creator = Creator()
        while len(mastery["mastery_0"]) < 3:
            print(f"creating initial word")
            print(f"length mastery_0: {len(mastery['mastery_0'])}")
            creator.create_word(mastery, words_list, words_created)

        return random.choice(mastery["mastery_0"])
    
    def pick_mastery(self):
        testing_probability = [0,0,0,0,0,1,1,1,2,2,3,4,5]
        mastery_level = random.choice(testing_probability)

        return mastery_level

    def get_word(self, mastery, words_list, words_created):
        creator = Creator() 
        while len(mastery["mastery_0"]) < 3:
            print(f"current length of mastery_0: {len(mastery['mastery_0'])}")
            creator.create_word(mastery, words_list, words_created)

        mastery_level = self.pick_mastery()
        while mastery[f"mastery_{mastery_level}"] == []:
            mastery_level = self.pick_mastery()
                
        print(f"chosen mastery_level: {mastery_level}")
        word_to_test = random.choice(mastery[f"mastery_{mastery_level}"])
        
        return word_to_test, mastery_level

        # mastery_level = random.choice(testing_probability)
        # if self.mastery[f"mastery_{mastery_level}"] != []:
        #     word_to_test = random.choice(self.mastery[f"mastery_{mastery_level}"])
        #     return word_to_test, mastery_level

    def check_answer(self, answer, mastery, words_created, word_to_test, mastery_level):
        word_data = words_created[word_to_test]
        if answer == word_data['translation_decoded'] or answer == word_data['synonyms'][0] or answer == word_data['synonyms'][1] or answer == word_data['synonyms'][2]:
            self.correct_answer(word_to_test, mastery_level, mastery)
            return True
        else:
            self.incorrect_answer(word_to_test, mastery_level, mastery)
            return False

    def correct_answer(self, word_to_test, mastery_level, mastery):
        if mastery_level == 5:
            return
        else:
            mastery[f"mastery_{mastery_level}"].remove(int(word_to_test))
            mastery[f"mastery_{mastery_level + 1}"].append(int(word_to_test))
            with open("mastery.json", "w") as file3:
                json.dump(mastery, file3, indent=4, separators=(',', ': '))
            
    def incorrect_answer(self, word_to_test, mastery_level, mastery):
        if mastery_level == 0 or mastery_level == 5:
            return
        else:    
            mastery[f"mastery_{mastery_level}"].remove(int(word_to_test))
            mastery[f"mastery_{mastery_level - 1}"].append(int(word_to_test))
            with open("mastery.json", "w") as file3:
                json.dump(mastery, file3, indent=4, separators=(',', ': '))