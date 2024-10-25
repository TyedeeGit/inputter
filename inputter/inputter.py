from typing import Any, Optional, Callable
from .condition import Condition, null_condition
from dataclasses import dataclass

def loop() -> None:
    """
    An infinite loop generator.
    :return:
    """
    while True:
        yield

@dataclass
class Inputter:
    """
    Implements user input processing.
    """

    conditions: tuple[Condition] = ()
    """
    A tuple of conditions to handle inputs. Each condition is applied sequentially until one catches an input.
    """

    prompt: str = ""
    """
    The initial prompt to ask the user for input.
    """

    no_input_msg: str = ""
    """
    The message displayed when no valid input is provided.
    """

    no_input_val: Any = None
    """
    The value returned when no valid input is provided.
    """

    attempts: int = 0
    """
    The number of attempts to give the user before giving up. Setting to zero or a negative number will give unlimited
    attempts.
    """

    def get(self,
            prompt: str = "",
            no_input_msg: str = "",
            no_input_val: Optional[Any] = None,
            attempts: Optional[int] = None,
            getter: Callable[[str], str] = input) -> tuple[Any, Optional[Condition]]:
        """
        Process a user input.
        :param prompt: Override the ``prompt`` parameter.
        :param no_input_msg: Override the ``no_input_msg`` parameter.
        :param no_input_val: Override the ``no_input_val`` parameter.
        :param attempts: Override the ``attempts`` parameter.
        :param getter: Function to get the input from the user. Uses builtin ``input`` by default.
        :return:
        """
        if not prompt:
            prompt = self.prompt
        if not no_input_msg:
            no_input_msg = self.no_input_msg
        if no_input_val is None:
            no_input_val = self.no_input_val
        if attempts is None:
            attempts = self.attempts
        attempts_iter = range(attempts) if attempts > 0 else loop()
        current_prompt = prompt
        for i in attempts_iter:
            string = getter(current_prompt)
            for cond in self.conditions + (null_condition(new_prompt=prompt, is_error=True),):
                if cond.cond(string):
                    if cond.is_error:
                        if cond.new_prompt:
                            current_prompt = cond.new_prompt.format(string=string)
                        break
                    else:
                        return cond.handle(string), cond
        if no_input_msg:
            print(no_input_msg)
        return no_input_val, None
