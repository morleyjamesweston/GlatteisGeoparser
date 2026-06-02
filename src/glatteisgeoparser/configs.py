from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class OutputConfigs:
    output_format: str
    output_path: Optional[str] = None


@dataclass
class RecognizerConfigs:
    language: str
    method: str
    model: str


default_recognizer_configs = RecognizerConfigs(
    language="de",
    method="spacy",
    model="de_core_news_sm",
)


@dataclass
class ResolverConfigs:
    method: str | None
    model: Optional[str] = None


default_resolver_configs = ResolverConfigs(method="statistical")


@dataclass
class GazetteerConfigs:
    name: str
    index_col: str
    names_col: str
    admin_rank: Union[str, int]
    population_column: str | None = None
    is_contextual: bool = False
