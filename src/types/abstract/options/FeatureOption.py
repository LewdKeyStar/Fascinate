from dataclasses import dataclass, field

from typing import Union, Callable

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
        Callable # exact callable signatures are not provided, but defined in inheritance
    ] = ""

    type: any = int # Cannot be made variable, the ArgumentParser wouldn't understand it

    include_in_filename: Union[
        bool,
        Callable
    ] = True

    # Normally, choices and a range should not coexist...but who knows.

    choices: Choices = None # ...and not an empty set of choices, otherwise argparse will accept no values.
    range: Range = None # ...so that if a range is instantiated, it will always mean something.

    desc: str = ""

    # Since type cannot vary, the formatters use conditional value reformatting instead.

    renamed_values: dict[any, str] = field(default_factory = dict)
    value_format: Callable = None # Default has to be provided, but will be overriden in inheritance

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
