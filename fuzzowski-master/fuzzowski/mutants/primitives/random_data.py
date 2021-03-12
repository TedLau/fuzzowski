import random
from ..mutant import Mutant


class RandomData(Mutant):
    def __init__(self, value: bytes, min_length: int, max_length: int, max_mutations: int = 25, fuzzable: bool = True,
                 step: int = None, name: str = None):
        """
        Generate a random chunk of data while maintaining a copy of the original. A random length range
        can be specified.
        For a static length, set min/max length to be the same.
        维护最初堆块的拷贝的同时生成一个充满数据的随机堆块。
        随机堆块的长度范围可以指定。

        Args:
            value:          Original value
            min_length:     Minimum length of random block
            max_length:     Maximum length of random block
            max_mutations:  (Optional, def=25) Number of mutations to make before reverting to default
            fuzzable:       (Optional, def=True) Enable/disable fuzzing of this primitive
            step:           (Optional, def=None) If not null, step count between min and max reps, otherwise random
            name:           (Optional, def=None) Specifying a name gives you direct access to a primitive
        """
        self.min_length = min_length
        self.max_length = max_length
        self.max_mutations = max_mutations
        self.step = step
        if self.step:
            self.max_mutations = (self.max_length - self.min_length) / self.step + 1

        # Lets generate some random mutations
        # 初始化随机的mutation
        mutations = []

        for _ in range(self.max_mutations):
            # select a random length for this string.
            # _ 临时变量，只使用一次，不再使用，只起到计数的作用。
            # 每一次为字符串选择一个长度
            if not self.step:
                length = random.randint(self.min_length, self.max_length)
                # 如果没有指定步长，那么便在最大最小值之间随机选择一个
            # select a length function of the mutant index and the step.
            else:
                length = self.min_length + self._mutant_index * self.step
                # 如果指定了步长，那么便从最小长度开始根据步长进行迭代

            # reset the value and generate a random string of the determined length.
            # 重置值并根据指定的长度生成随机的字符串，长度在0-255之间
            self._value = b""
            for i in range(length):
                self._value += bytes([random.randint(0, 255)])

            mutations.append(self._value)

        # The Mutant behaviour is perfect for this one :)
        super().__init__(value, name=name, fuzzable=fuzzable, mutations=mutations)
