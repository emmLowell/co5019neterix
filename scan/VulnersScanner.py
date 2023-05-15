from dataclasses import dataclass
from datetime import datetime
from os import getenv
from typing import Dict, List, Optional
from vulners import VulnersApi
from vulners.base import ResultSet


@dataclass
class Vulnerability:
    lastseen: datetime
    description: str
    published: datetime
    type: str
    title: str
    bulletinFamily: str
    cvelist: List[str]
    modified: datetime
    id: str
    href: str
    sourceData: Optional[str]
    cvss: Dict[str, float]
    sourceHref: Optional[str]
    vhref: str

    @staticmethod
    def from_dict(data: Dict) -> "Vulnerability":
        return Vulnerability(
            lastseen=datetime.fromisoformat(data["lastseen"]),
            description=data["description"],
            published=datetime.fromisoformat(data["published"]),
            type=data["type"],
            title=data["title"],
            bulletinFamily=data["bulletinFamily"],
            cvelist=data["cvelist"],
            modified=datetime.fromisoformat(data["modified"]),
            id=data["id"],
            href=data["href"],
            sourceData=data["sourceData"] if "sourceData" in data else None,
            cvss=data["cvss"],
            sourceHref=data["sourceHref"] if "sourceHref" in data else None,
            vhref=data["vhref"],
        )


class VulnersScanner:
    api: VulnersApi

    def __init__(self):
        self.api = VulnersApi(api_key=getenv("VULNERS_API_KEY"))

    def find_all_exploits(self, software: str, version: str) -> List[Vulnerability]:
        vulnerabilities: ResultSet = self.api.find_exploit_all(f"{software} {version}")

        result = []

        for vulnerability in vulnerabilities:
            result.append(Vulnerability.from_dict(vulnerability))

        return result
