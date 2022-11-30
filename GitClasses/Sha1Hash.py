from dataclasses import dataclass, field


@dataclass
class Sha1Hash(object):
    sha1_hash: str
    dir: str = field(default='')

    def __post_init__(self):
        self.dir = self.sha1_hash[:2]

    def __str__(self) -> str:
        return self.sha1_hash
