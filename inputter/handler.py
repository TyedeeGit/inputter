from typing import Callable, TypeVar, TypeVarTuple, Generic

T = TypeVar('T')
Ts = TypeVarTuple('Ts')
Vs = TypeVarTuple('Vs')

class Handler(Generic[T, *Ts, *Vs]):
    def __init__(self, handle: Callable[[*Ts, *Vs], T], args: tuple[*Vs] = ()) -> None:
        self._handle = handle
        self._args = args

    def __call__(self, *args: *Vs) -> T:
        self._handle(*args, *self._args)