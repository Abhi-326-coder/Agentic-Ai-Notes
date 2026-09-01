from abc import ABC, abstractclassmethod

class LLM(ABC):
    
    @abstractclassmethod
    def generate(self, contents, tools):
        pass