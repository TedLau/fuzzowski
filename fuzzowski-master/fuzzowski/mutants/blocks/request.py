import collections
import re

from fuzzowski.exception import FuzzowskiRuntimeError
from ..mutant import Mutant
from .block import Block
from .. import blocks
from fuzzowski.responses.response import Response


class Request(Block):
    _mutant_name = Mutant.name_re.pattern.strip("^$")
    _path_name_re = re.compile(f'^(?P<request>{_mutant_name})(?:[.](?P<mutant>{_mutant_name}))?$')

    def __init__(self, name):
        """
        Top level container instantiated by s_initialize(). Can hold any block structure or primitive.
        It is basically a Block, with some special arguments and functions, but behaves exactly like a block
        由s_initialize()实例化的顶级容器。可以保存任何块结构或原语。
        它基本上是一个块，有一些特殊的参数和函数，但行为完全像块
        Args:
            name: Name of the Request
        """
        super().__init__(name, self)  # A Request is a Block without a Request parent! 请求是一个没有父级请求的块
        self.id = None
        self.callbacks = collections.defaultdict(list)
        self.names = {}  # dictionary of directly accessible mutants  可以直接获取的变种词典
        self.mutant = None  # current primitive being mutated 正在被变异的原语
        self.block_stack = []  # list of open blocks, -1 is last open block
        # self._element_mutant_index = None  # index of current mutant element within self.stack
        self._mutation_gen = self.mutation_generator()
        # self.variables: Mapping[str, int] = dict()
        self.variables = blocks.VARIABLES
        self.responses = []

    def push(self, item: Mutant):
        """
        Push a Mutable item in the Request stack. This function maintains the stack of open blocks,
        and it will push the item inside the last open block, or inside the Request stack if no blocks are open.
        压入 一个可以进行突变的item到请求堆栈中。该函数维持了一个开放块的栈并且它会将item压入到最后一个开放的块或者如果没有开放块，就将其
        压入请求栈
        Also, it maintains a dictionary with the names of all items inside the request.
        另外，它也维护了一个包含有所有请求中item名字的字典。
        """
        # if the item has a name, add it to the internal dictionary of names.
        # 如果item有名字，那么将其加入至内部名字字典中。
        if hasattr(item, "name") and item.name:
            # ensure the name doesn't already exist.
            if item.name in self.names.keys():
                raise FuzzowskiRuntimeError(f"BLOCK NAME ALREADY EXISTS: {item.name}")

            self.names[item.name] = item

            # # do the same for the global dictionary of named mutants:
            # if item.name in blocks.NAMED_MUTANTS:
            #     raise FuzzowskiRuntimeError(f"BLOCK NAME ALREADY EXISTS IN OTHER REQUEST: {item.name}. "
            #                                 f"Please, make them unique!")
            # blocks.NAMED_MUTANTS[item.name] = item

        # if there are no open blocks, the item gets pushed onto the request stack.
        # 如果没有开放的块，就将item压入至请求栈中
        # otherwise, the pushed item goes onto the stack of the last opened block.
        # 否则，将item压入至最后一个开放的块中
        if not self.block_stack:  # No blocks open in block_stack
            self.stack.append(item)  # Adds the item to the Request stack
        else:
            self.block_stack[-1].push(item)  # Adds the item to the last opened block

        # add the opened block to the block stack.
        if isinstance(item, Block):
            self.block_stack.append(item)

    def pop(self):
        """
        The last open block was closed, so pop it off of the block stack.
        最后一个块关闭了，就将其弹出栈
        """
        if not self.block_stack:  # len(block_stack) == 0
            raise FuzzowskiRuntimeError("BLOCK STACK OUT OF SYNC")

        self.block_stack.pop()

    def get_mutant(self, name: str) -> Mutant:
        """
        Get a mutant by its name if it is in this request, or by the full path if it is not found here
        如果变体在请求中根据名字查找，或者如果没有找到就根据路径来查找。
        Args:
            name: The mutant name

        Returns: the Mutant
        """
        if name in self.names:
            return self.names[name]
        else:
            return Request.get_mutant_by_path(name)

    @staticmethod
    def get_mutant_by_path(path_name: str) -> Mutant:
        """
        Search a mutant by its path, the path is the request name, followed by a dot (.) and the mutant name
        根据路径来查找，路径就是请求名，伴随着点和变体名。
         For example: request1.string1
        Args:
            path_name: The path to search. It can be a request_name, or a request_name.mutant_name
        Returns: The Mutant found
        Raises: FuzzowskiRuntimeException, if the mutant is not found
        """
        m = Request._path_name_re.search(path_name)
        if m is None:
            raise FuzzowskiRuntimeError(f'Invalid path name: {path_name}')

        # 1. Search request
        if m['request'] in blocks.REQUESTS:
            request = blocks.REQUESTS[m['request']]
        else:
            raise FuzzowskiRuntimeError(f'Invalid path name: {path_name}. Request {m["request"]} not found')

        if m['mutant'] is None:  # Search for a request
            return request
        else:  # Search for a request.mutant
            if m['mutant'] in request.names:
                return request.names[m['mutant']]
            else:
                raise FuzzowskiRuntimeError(f'Invalid path name: {path_name}. Mutant {m["mutant"]} not found')

    def add_response(self, response: Response):
        # 在response队列中追加当前的response
        if response not in self.responses:
            self.responses.append(response)

    def parse_response(self, data: bytes) -> Response or None:
        if len(self.responses) == 0:
            return None
        for response in self.responses:
            try:
                response_str = response.parse(data)
                return response_str
            except FuzzowskiRuntimeError:
                pass
        raise FuzzowskiRuntimeError('Responses defined did not match with the data')
