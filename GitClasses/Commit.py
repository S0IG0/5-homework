from GitClasses.Sha1Hash import Sha1Hash
from dataclasses import dataclass


@dataclass
class Commit(object):
    parents: list[Sha1Hash]
    sha1_hash: Sha1Hash
    tree: Sha1Hash
    author: str
    committer: str
    commit: str

    def __str__(self) -> str:
        return f'Commit{{\n' \
               f'\tparents: {self.parents}\n' \
               f'\tsha1_hash: {self.sha1_hash}\n' \
               f'\ttree: {self.tree}\n' \
               f'\tauthor: {self.author}\n' \
               f'\tcommitter: {self.committer}\n' \
               f'\tcommit: {self.commit}\n' \
               f'}}'
