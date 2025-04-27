from dataclasses import dataclass

@dataclass
class Domain:
    domain: str
    source: str

    def to_dict(self):
        return {
            "domain": self.domain,
            "source": self.source
        }