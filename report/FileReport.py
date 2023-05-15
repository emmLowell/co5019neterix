
class FileReport:
    
    def send_report(self, report: str, user) -> bool:
        with open(f"report-{user.email}.txt", "w") as f:
            f.write(report)
        return True