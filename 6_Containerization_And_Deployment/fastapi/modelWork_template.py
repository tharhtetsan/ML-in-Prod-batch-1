from abc import ABC, abstractmethod


class BaseTemplate(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def _predict(self):
        pass

