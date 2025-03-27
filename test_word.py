import json
from create_word import Creator
import random

class Tester:
    def __init__(self):
        pass

    def get_initial_word(self, mastery, words_list, words_created):
        creator = Creator()
        while len(mastery["mastery_0"]) < 3:
            print(f"creating initial word")
            print(f"length mastery_0: {len(mastery['mastery_0'])}")
            mastery, words_created = creator.create_word(mastery, words_list, words_created)

        return random.choice(mastery["mastery_0"]), mastery, words_created
    
    def pick_mastery(self):
        testing_probability = [0,0,0,0,0,1,1,1,2,2,3,4,5]
        mastery_level = random.choice(testing_probability)

        return mastery_level

    def get_word(self, mastery, words_list, words_created):
        creator = Creator() 
        while len(mastery["mastery_0"]) < 3:
            print(f"current length of mastery_0: {len(mastery['mastery_0'])}")
            mastery, words_created = creator.create_word(mastery, words_list, words_created)

        mastery_level = self.pick_mastery()
        while mastery[f"mastery_{mastery_level}"] == []:
            mastery_level = self.pick_mastery()
                
        print(f"chosen mastery_level: {mastery_level}")
        word_to_test = random.choice(mastery[f"mastery_{mastery_level}"])
        
        return word_to_test, mastery_level, mastery, words_created

    def check_answer(self, answer, mastery, words_created, word_to_test, mastery_level):
        word_data = words_created[word_to_test]
        if answer == word_data['translation_decoded'] or answer == word_data['synonyms'][0] or answer == word_data['synonyms'][1] or answer == word_data['synonyms'][2]:
            mastery = self.correct_answer(word_to_test, mastery_level, mastery)
            return True, mastery
        else:
            mastery = self.incorrect_answer(word_to_test, mastery_level, mastery)
            return False, mastery

    def correct_answer(self, word_to_test, mastery_level, mastery):
        if mastery_level == 5:
            return mastery
        else:
            mastery[f"mastery_{mastery_level}"].remove(int(word_to_test))
            mastery[f"mastery_{mastery_level + 1}"].append(int(word_to_test))
            with open("mastery.json", "w") as file3:
                json.dump(mastery, file3, indent=4, separators=(',', ': '))
            return mastery
            
    def incorrect_answer(self, word_to_test, mastery_level, mastery):
        if mastery_level == 0 or mastery_level == 5:
            return mastery
        else:    
            mastery[f"mastery_{mastery_level}"].remove(int(word_to_test))
            mastery[f"mastery_{mastery_level - 1}"].append(int(word_to_test))
            with open("mastery.json", "w") as file3:
                json.dump(mastery, file3, indent=4, separators=(',', ': '))
            return mastery