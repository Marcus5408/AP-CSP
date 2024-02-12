class Student:
    def __init__(self, name:str) -> None:
        self.name = name
        self.test_scores = []
    
    def add_test(self, test_score:int) -> None:
        self.test_scores.append(test_score)

    def get_average(self) -> float:
        return sum(self.test_scores) / len(self.test_scores)