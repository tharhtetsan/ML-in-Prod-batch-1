from eg_Component import Component
from eg_Decorator import Decorator

class Model_2(Decorator):
    def __init__(self, component: Component) -> None:
        super().__init__(component)

        self.model_path = "model_2"


    def operation(self) -> str:
        print(self.model_path)
        return self.component.operation()
    
    