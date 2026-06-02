from typing import Union

from geopandas import GeoDataFrame

from .ollama import OllamaResolver
from .statistical import StatisticalResolver


class Resolver:
    def __init__(
        self,
        language: str,
        library: Union[str, None],
        model: Union[str, None],
    ) -> None:
        if library == "ollama":
            self.resolver = OllamaResolver(model if model else "")
        else:
            self.resolver = StatisticalResolver()

    def __call__(self, text: str, candidates: GeoDataFrame):
        result = self.resolver(text, candidates)
        return result
