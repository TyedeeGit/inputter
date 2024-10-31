from typing import Any, Optional, Callable

from . import nonempty_condition
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
                        cond.handle(string)
                        if cond.new_prompt:
                            current_prompt = cond.new_prompt.format(string=string)
                        break
                    else:
                        return cond.handle(string), cond
        if no_input_msg:
            print(no_input_msg)
        return no_input_val, None

def yes_no_inputter(prompt: str, err_prompt: str, yes: set[str] = frozenset({'y', 'yes', 'yep'}),
                    no: set[str] = frozenset({'n', 'no', 'nope'}),
                    no_input_msg="", no_input_val: bool = False, attempts: int = 0) -> Inputter:
    """
    Inputter for yes/no decisions.
    :param prompt: The initial prompt to ask the user for input.
    :param err_prompt: The error prompt if the user does not input a yes or no.
    :param yes: The set of strings considered as a yes.
    :param no: The set of strings considered as a no.
    :param no_input_msg: The message displayed when no valid input is provided.
    :param no_input_val: The value returned when no valid input is provided.
    :param attempts: The number of attempts to give the user before giving up. Setting to zero or a negative number will give unlimited attempts.
    :return:
    """
    conditions = (
        Condition(lambda x: x.lower() in yes, lambda x: True),
        Condition(lambda x: x.lower() in no, lambda x: False),
        nonempty_condition(new_prompt=err_prompt, is_error=True)
    )
    return Inputter(conditions, prompt, no_input_msg, no_input_val, attempts)