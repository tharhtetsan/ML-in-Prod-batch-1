from eg_Component import Component
from eg_ConcreteComponent import ConcreteComponent
from eg_Model_1 import Model_1
from eg_Model_2 import Model_2

def clint_code(component : Component):
    result = (component.operation())
    print(result)
    

simple = ConcreteComponent()
clint_code(simple)


print("############")

load_model_1 = Model_1(simple)
clint_code(load_model_1)
print("############")

load_model_2 = Model_2(load_model_1)
clint_code(load_model_2)
print("############")


