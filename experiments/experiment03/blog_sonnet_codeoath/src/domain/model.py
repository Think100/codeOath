from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Post:
    slug: str
    title: str
    date: date
    tags: list[str]
    content_md: str  # raw Markdown source
    content_html: str  # rendered HTML

    @property
    def tag_list(self) -> list[str]:
        return self.tags
