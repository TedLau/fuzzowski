from abc import ABCMeta, abstractmethod
from typing import Generator


class IMutant(object, metaclass=ABCMeta):
    """
    Generic Mutant Interface. Defines all public methods that should be overridden
    泛型变种接口。定义所有应该被重写的类

    """

    @abstractmethod
    def __init__(self):
        """
        Initializes the Mutant class, most Primitives and Blocks should override this
        初始化变种类，大部分的原语以及块应该重写这个

        """
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __len__(self):
        """
        Length of field. May vary if mutate() changes the length.
        区域的长度，如果mutable改变长度，那么长度就会变化

        Returns:
            int: Length of element (length of mutated element if mutated).
            整形， 如果可以变化。那么返回其长度

        """
        pass

    # @property 装饰器把读值方法标记为特性
    @property
    @abstractmethod
    def name(self) -> str:
        """Element name, should be specific for each instance.
        元素名，对于每一个实例都应该确定

        Returns:
            str: Name of the mutant
            名字

        """
        pass

    @property
    @abstractmethod
    def original_value(self) -> bytes:
        """
        Original value of the element without any fuzzing
        不进行fuzz时的初始值

        Returns:
            bytes: Original value
            字节类型，初始值

        """
        pass

    @property
    @abstractmethod
    def mutant_index(self) -> int:
        """
        Index of current mutation. 0 => original value. 1 => first mutation.
        第几次变化，1：第一次，2：第二次

        Returns:
            int: Index of current mutation
            整形：表示当前的变异次数

        """
        pass

    @property
    @abstractmethod
    def num_mutations(self) -> int:
        """
        Total number of mutations for this element.
        该元素的全部的变异次数

        Returns:
            int: Number of mutated forms this primitive can take
            整形：该原语可以进行的变异形式的数量

        """
        pass

    @property
    @abstractmethod
    def fuzzable(self) -> bool:
        """
        If False, this element should not be mutated in normal fuzzing.
        bool类型，如果假，那么就不应该进行正常的fuzz

        Returns:
            bool: If the element is fuzzable or not
            bool: 返回值为是否可以进行fuzz

        """
        pass

    @property
    @abstractmethod
    def disabled(self) -> bool:
        """
        If disabled, the mutations should be discarded
        确认是否应该使用该变种，不应该则进行舍弃

        Returns:
            bool: If the mutant was disabled or not
            bool: 是否使用该mutant进行fuzz
        """
        pass

    @disabled.setter
    @abstractmethod
    def disabled(self, value: bool):
        """
        Setter for disabled
        上述方法的setter属性，setter是一个装饰器将读取与设定值的方法绑定在一起

        可以理解为，setter属性可以设置是否disabled @author: TedLau

        Args:
            value (bool): True or False
            bool: 返回值表示是否进行disabled

        """
        pass

    @abstractmethod
    def mutation_generator(self, mutant_index: int = 0) -> Generator[bytes, None, None]:
        """
        Creates a generator that will change the Mutant and return the mutated value
        创建一个可以改变Mutant以及返回mutated后值的生成器

        Args:
            mutant_index: It initializes the mutant_index at the specified value
            mutant_index: 参数是进行mutate的下标

        Returns:
            Generator: The mutations generator
            Generator: 变化生成器

        """
        pass

    @abstractmethod
    def goto(self, mutant_index: int):
        """
        Moves the state of the mutant to the specified mutant_index
        将某一变种的状态转移至特定的变种下标

        Args:
            mutant_index (int): The mutant_index
            mutant_index (int): 返回值是移动后的变种下标

        """
        pass

    @abstractmethod
    def render(self, replace_node: str = None, replace_value: str = None, original: bool = False) -> bytes:
        """
        Renders the value of the actual state
        呈现实际状态的值，展示更好一些

        Args:
            replace_node: If replace node is set, instead of the value it will use the replace_value
            replace_node: 如果设置了替换节点，那么便使用replace_value，而不是value。TODO:还是我英语不够啊

            replace_value: Value to be used
            replace_value: 将要被使用的值

            original: If the original value is to be used instead of the actual value TODO: Is this necessary?
            original: 如果使用原值，那么便步使用实际的值。 TODO:necessary?不清楚，如果使用original，那么render的作用就没有了。

        Returns:
            bytes: The rendered value
            bytes: 将要呈现的值
        """
        pass

    @abstractmethod
    def reset(self):
        """
            Reset element to pre-mutation state.
            将元素设置为突变前状态
        """
        pass
