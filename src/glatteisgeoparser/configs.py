from dataclasses import dataclass
from typing import Union


@dataclass
class GlatteisConfigs:
    language: str
    library: str
    model: str


@dataclass
class GazetteerConfigs:
    name: str
    index_col: str
    names_col: str
    admin_rank: Union[str, int]
    population_column: str | None = None
    is_contextual: bool = False


default_configs = GlatteisConfigs(
    language="de",
    library="spacy",
    model="de_core_news_sm",
)
