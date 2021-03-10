from typing import Union, Mapping

from .block import Block
from .checksum import Checksum
from .request import Request
from .size import Size
from .repeat import Repeat
from .variable import Variable

# __all__ = [Block, Request, Size, Checksum, Repeat, Variable]

REQUESTS: Mapping[str, Request] = {}    # Variable where all requests created with s_initialize will be
# 所有用s_initialize创建的请求的变量都将在其中
CURRENT: Union[Request, None] = None    # Current Request
# 当前的请求
VARIABLES: Mapping[str, bytes] = {}     # It contains all variables set by requests or callbacks
# 由请求或回调设置的所有变量
