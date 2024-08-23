from sg_BaseTemplate import BaseTemplate
from sg_template_1 import template_1
from sg_template_2 import template_2
def client_code(base_template : BaseTemplate) -> None:
    base_template.template_method()

tp_1 =  template_1()
client_code(tp_1)

print("###########")
tp_2 =  template_2()
client_code(tp_2)
