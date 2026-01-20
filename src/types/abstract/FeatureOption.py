from dataclasses import dataclass, field

from typing import Union, Callable

from argparse import Namespace

from src.types.abstract.Shortenable import Shortenable
from src.types.abstract.Choices import Choices
from src.types.abstract.Range import Range

# This is a base class for FeatureParameter (a feature's unique, characteristic traits)
# And FeatureSetting (options shared across all features : enable intervals, alpha, etc.)

@dataclass
class FeatureOption(Shortenable):
    name: str
    default: any = 0
    unit: Union[
        str,
        Callable[[Namespace], str],
        Callable[[Namespace, str], str]
    ] = ""

    type: any = int

    include_in_filename: Union[
        bool, # used for all parameters for now
        Callable[[any], bool], # option_value => bool
        Callable[[Namespace, str, any], bool] # args, feature_name, option_value => bool
    ] = True

    # Normally, choices and a range should not coexist...but who knows.

    choices: Choices = None # ...and not an empty set of choices, otherwise argparse will accept no values.
    range: Range = None # ...so that if a range is instantiated, it will always mean something.

    desc: str = ""

    renamed_values: dict[any, str] = field(default_factory = dict)
    value_format: Union[
        Callable[[Namespace, any], str],
        Callable[[Namespace, str, any], str]
    ] = lambda x, y: y

    # FIXME : those line breaks are not preserved in the help message.
    # This is probably due to the built-in formatter.

    @property
    def help(self):
        return f'''
        {self.desc}
        Type : {str(self.type.__name__)}
        {f'Range : {self.range}' if self.range is not None else ''}
        {f'Possible choices : {self.choices}' if self.choices is not None else ''}
        '''
