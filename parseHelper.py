# Typing imports

from typing import Union, List, Dict

# Type aliases

PathType = Union[str, List[Union[int, float]]]
SettingType = Dict[str, Union[int, str, bool]]
EventType = Dict[str, Union[int, str, float]]

MapType = Dict[str, Union[PathType, SettingType, List[EventType]]]

# pre-defined Exceptions

class ParseException(Exception):
    pass

class UnExpectedParseException(ParseException):
    def __init__(self, err: str):
        # TODO: Fill Username & Tag with yours
        super().__init__(err + '디스코드에 {Username}#{Tag}으로 해당 오류를 제보해주시기 바랍니다')

class ExpectedParseException(UnExpectedParseException):
    def __init__(self, err: str, suggest: str):
        super().__init__(err + suggest + '한 후에도 오류가 지속된다면 ')

# Define Helper Functions & Variables...
