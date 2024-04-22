import datetime
import re
from constants import *

class Highscore:
    def __init__(self):
        self.last_line = ""
        self.last_scores = []

    @classmethod
    def save_results(cls, score):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(FILE_PATH, "a", newline="") as file:
            file.write(f"Highscore: {score} Date: {current_date}\n")

    def get_last_line(self):
        with open(FILE_PATH, "r") as file:
            lines = file.readlines()

            for i, line in enumerate(lines):
                if i + 1 == len(lines):
                    self.last_line = line
                    break
    
    def extract_score(self):
        match = re.search(r"Highscore: (\d*) Date:", self.last_line)
        return match.group(1)

    def get_last_scores(self, scores_number):
        with open(FILE_PATH, "r") as file:
            for line in file:
                if len(self.last_scores) < scores_number:
                    self.last_scores.append(line)
        
        return self.last_scores

