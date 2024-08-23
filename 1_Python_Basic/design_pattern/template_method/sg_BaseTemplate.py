from abc import ABC, abstractmethod

class BaseTemplate(ABC):
    """
    The Abstract Class defines a template method that contains a skeleton of algorithm.
    Concrete subclasses should implement these operations, but leave the
    template method itself.
    """

    def template_method(self) -> None:
        self.base_operation1()
        self.required_operations1()
        self.base_operation2()

        self.hook1()
        self.required_operations2()
        self.base_operation3()
        self.hook2()

    def base_operation1(self) -> None:
        print("AbstractClass says: base_operation1. ")

    def base_operation2(self) -> None:
        print("AbstractClass says: base_operation2.")

    def base_operation3(self) -> None:
        print("AbstractClass says: base_operation3.")

    @abstractmethod
    def required_operations1(self) -> None:
        pass

    @abstractmethod
    def required_operations2(self) -> None:
        pass

    """Hooks are optional. So these are not abstractmethod"""
    def hook1(self) -> None:
        print("original hook1")
        pass

    def hook2(self) -> None:
        pass
