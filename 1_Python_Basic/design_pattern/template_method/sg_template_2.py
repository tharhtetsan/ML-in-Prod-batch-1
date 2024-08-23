from sg_BaseTemplate import BaseTemplate
class template_2(BaseTemplate):
    def required_operations1(self) -> None:
        print("template_2 : Implemented Operation1")

    def required_operations2(self) -> None:
        print("template_2 : Implemented Operation2")

    def hook1(self) -> None:
        print("template_2 : Overridden Hook1")