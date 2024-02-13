from typing import List

class Student:
    def __init__(self, name:str) -> None:
        self.name = name
        self.test_scores = {}

    def add_course(self, course:str) -> None:
        self.test_scores[course] = []
    
    def add_test(self, course:str, test_scores:List[int]) -> None:
        self.test_scores[course].extend(test_scores)

    def get_average(self, course:str) -> float:
        return sum(self.test_scores[course])/len(self.test_scores[course])