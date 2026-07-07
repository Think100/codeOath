"""Contract between the domain and the outside world.

The web layer depends on this Protocol, not on a concrete storage
implementation. Any class with a matching load_all() counts as a
repository (structural typing), which also makes testing with fakes trivial.
"""

from __future__ import annotations

from typing import Protocol

from src.domain.models import Post, PostLoadError


class PostRepository(Protocol):
    def load_all(self) -> tuple[list[Post], list[PostLoadError]]:
        """Load every readable post plus a report of sources that failed.

        A single broken post must not take the whole blog down: it is
        returned as a PostLoadError instead of raising.
        """
        ...
