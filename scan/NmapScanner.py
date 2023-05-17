from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import nmap3


@dataclass
class RuntimeResult:
    time: datetime
    summary: str
    exitStatus: str

    @staticmethod
    def from_dict(data: dict):
        return RuntimeResult(
            time=datetime.fromtimestamp(int(data["time"])),
            summary=data["summary"],
            exitStatus=data["exit"],
        )


@dataclass
class StatResult:
    scanner: str
    args: str
    start: datetime
    version: str
    xmloutputversion: str

    @staticmethod
    def from_dict(data: dict):
        return StatResult(
            scanner=data["scanner"],
            args=data["args"],
            start=datetime.fromtimestamp(int(data["start"])),
            version=data["version"],
            xmloutputversion=data["xmloutputversion"],
        )


@dataclass
class TaskResult:
    task: str
    time: datetime
    extrainfo: Optional[str]

    @staticmethod
    def from_dict(data: dict):
        return TaskResult(
            task=data["task"],
            time=datetime.fromtimestamp(int(data["time"])),
            extrainfo=data["extrainfo"] if "extrainfo" in data else None,
        )


@dataclass
class HostResult:
    ip: str
    type: str


@dataclass
class Service:
    name: str
    product: Optional[str]
    version: Optional[str]
    extrainfo: Optional[str]
    tunnel: Optional[str]
    method: Optional[str]
    conf: str

    @staticmethod
    def from_dict(data: dict):
        return Service(
            name=data["name"],
            product=data["product"] if "product" in data else None,
            version=data["version"] if "version" in data else None,
            extrainfo=data["extrainfo"] if "extrainfo" in data else None,
            tunnel=data["tunnel"] if "tunnel" in data else None,
            method=data["method"] if "method" in data else None,
            conf=data["conf"],
        )


@dataclass
class PortDetailResult:
    protocol: str
    portid: str
    state: str
    reason: str
    reason_ttl: str
    service: Service
    cpe: List[dict]
    scripts: List[dict]

    @staticmethod
    def from_dict(data: dict):
        return PortDetailResult(
            protocol=data["protocol"],
            portid=data["portid"],
            state=data["state"],
            reason=data["reason"],
            reason_ttl=data["reason_ttl"],
            service=Service.from_dict(data["service"]),
            cpe=data["cpe"],
            scripts=data["scripts"],
        )


@dataclass
class StateResult:
    state: str
    reason: str
    reason_ttl: str


@dataclass
class PortResult:
    osmatch: dict
    ports: List[PortDetailResult]
    hostname: List[HostResult]
    macaddress: Optional[str]
    state: dict

    @staticmethod
    def from_dict(data: dict):
        return PortResult(
            osmatch=data["osmatch"],
            ports=[PortDetailResult.from_dict(port) for port in data["ports"]],
            hostname=[
                HostResult(ip=host["name"], type=host["type"])
                for host in data["hostname"]
            ],
            macaddress=data["macaddress"] if "macaddress" in data else None,
            state=StateResult(
                state=data["state"]["state"],
                reason=data["state"]["reason"],
                reason_ttl=data["state"]["reason_ttl"],
            ),
        )


@dataclass
class NmapScanResult:
    ip: str
    ports: PortResult
    stats: StatResult
    task_results: List[TaskResult]
    runtime: RuntimeResult

    def all_services(self) -> List[Service]:
        print(self.ports.ports)
        return [port.service for port in self.ports.ports]

    def all_service_names(self) -> List[str]:
        return [port.service.name for port in self.ports.ports]

    def all_service_products(self) -> List[str]:
        return [
            f"{port.service.product} {port.service.version if port.service.version is not None else ''}"
            for port in self.ports.ports
            if port.service.product is not None
        ]

    def all_ports(self) -> List[PortDetailResult]:
        return self.ports.ports

    def all_hosts(self) -> List[HostResult]:
        return self.ports.hostname

    @staticmethod
    def from_dict(ip: str, data: dict):
        return NmapScanResult(
            ip=ip,
            ports=PortResult.from_dict(data[ip]),
            stats=StatResult.from_dict(data["stats"]),
            task_results=[TaskResult.from_dict(task) for task in data["task_results"]],
            runtime=RuntimeResult.from_dict(data["runtime"]),
        )


class NmapScanner:
    @staticmethod
    def scan(self, target, options="-sS") -> NmapScanResult:
        """
        Scan a target with Nmap.

        :param target: The target to scan.
        :param options: The options to use.
        :return: The scan result.
        """
        nmap = nmap3.Nmap()
        result = nmap.nmap_version_detection(target=target, args=options)
        return NmapScanResult.from_dict(target, result)
