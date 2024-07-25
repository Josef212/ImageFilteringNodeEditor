from abc import ABC, abstractmethod

class BaseNode(ABC):

    @abstractmethod
    def get_debug_name(self):
        pass

    @abstractmethod
    def get_all_attributes(self):
        pass

    @abstractmethod
    def get_input_attributes(self):
        pass

    @abstractmethod
    def get_output(self):
        pass
