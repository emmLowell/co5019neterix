#!/usr/bin/env/bin/python3
import base64
import re
from datetime import datetime
from os import getenv
from os.path import exists
from typing import Any, List

import nmap3
import vulners
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv
from sendgrid.helpers.mail import (
    Attachment,
    Disposition,
    FileContent,
    FileName,
    FileType,
    Mail,
)

load_dotenv()


class Main:
    ip_addresses: list
    service_versions: list
    confirmed_cves: list

    def __init__(self):
        self.ip_addresses = []
        self.service_versions = []
        self.confirmed_cves = []

        self.date = str(datetime.now().date())
        self.time = str(datetime.now().time().replace(microsecond=0))

    def readIp(self):
        with open("data/vulnscan_ip.txt", "r") as file:
            for line in file:
                self.ip_addresses.append(line.strip())

    def writeData(self, savefile: str, data: str, newline=True):
        with open("data/" + savefile, "a+") as file:
            file.write(data)
            if newline:
                file.write("\n")

    def scanPorts(self) -> List[str]:
        self.readIp()
        results = []
        for host in self.ip_addresses:
            nmap = nmap3.Nmap()
            results.append(str(nmap.nmap_version_detection(host, args="-sS")))
        return results

    def regex(self, expression: str, string: str) -> List[Any]:
        return re.findall(expression, string)

    def regexOutput(self):
        results = self.scanPorts()
        result = results[0]  # get first ip result (test purposes)
        ports = self.regex(r"\d+(?=\W+state\W+)|open(?=\W)", result)
        services = self.regex(r"(?<='name': ')[^']+(?=')", result)
        version = self.regex(r"(?<='product': ')[^']*|(?<='version': ')[^']*", result)
        old_ports = exists("data/open_ports.txt")
        if not old_ports:
            for each in ports:
                if each != "open":
                    self.writeData("open_ports.txt", each)
        else:
            for each in ports:
                if each != "open":
                    self.writeData("new_ports.txt", each)
        for all_services in services:
            self.writeData("open_services", all_services)
        for all_versions in version:
            self.service_versions.append(all_versions)
            self.writeData("versions.txt", all_versions)

    def versionVulnerbilities(self, exploits=""):
        vulners_api = vulners.VulnersApi(
            api_key=getenv("VULNERS_API_KEY", "VULNERS_API_KEY")
        )
        cves = self.confirmed_cves
        for each_version in range(len(self.service_versions)):
            cve = self.service_versions[each_version]
            exploits = str(vulners_api.find_exploit_all(cve))
            cve_reference = self.regex(r"CVE-\d+-\d+", exploits)
            cves.append(cve_reference)
        self.confirmed_cves = list(set(tuple(cve) for cve in cves))

    def sendEmail(self, sender: str, receiver: str):
        message = Mail(
            from_email=sender,
            to_emails=receiver,
            subject="New open ports found",
            html_content="<strong> New ports were found to be open from a scan result completed at "
            + self.date
            + "\t"
            + self.time
            + ".\t"
            "Please check attachment for further information.</strong>",
        )
        with open("data/open_ports.txt", "r") as f:
            data = f.read()
            encoded_file = base64.b64encode(data.encode()).decode()
        attachment = Attachment(
            FileContent(encoded_file),
            FileName("attachment.txt"),
            FileType("text/plain"),
            Disposition("attachment"),
        )
        message.attachment = attachment
        sg = SendGridAPIClient(api_key=getenv("SENDGRID_API_KEY", "SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def main(self):
        self.regexOutput()

        self.versionVulnerbilities()

        new_ports = exists("data/new_ports.txt")

        print(new_ports)
        if new_ports:
            self.sendEmail(
                getenv("SENDER_EMAIL", "SENDER_EMAIL"),
                getenv("TEST_RECIPENT_EMAIL", "TEST_RECIPENT_EMAIL"),
                # TODO - remove test recipient email
            )


if __name__ == "__main__":
    Main().main()
