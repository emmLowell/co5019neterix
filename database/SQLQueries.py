from enum import Enum, auto


class Tables(Enum):
    IP = (auto(), "ip")
    PORT = (auto(), "port")
    CVE = (auto(), "cve")
    SCAN = (auto(), "scan")
    IP_PORT = (auto(), "ip_port")
    IP_CVE = (auto(), "ip_cve")


SQL_TABLE_EXISTS = "SHOW TABLES LIKE :table_name;"
SQLITE_TABLE_EXISTS = (
    "SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name;"
)

CREATE_TABLES = {
    Tables.IP: """CREATE TABLE ip (
  id INT PRIMARY KEY,
  ip_address VARCHAR(45) NOT NULL,
  alias VARCHAR(45) NOT NULL
);""",
    Tables.PORT: """CREATE TABLE port (
  id INT PRIMARY KEY,
  port_number INT NOT NULL,
  service VARCHAR(45) NOT NULL
);""",
    Tables.CVE: """CREATE TABLE cve (
  id INT PRIMARY KEY,
  cve VARCHAR(45) NOT NULL
);""",
    Tables.SCAN: """CREATE TABLE scan (
  id INT PRIMARY KEY,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL,
  os VARCHAR(45) NOT NULL,
  ip_id INT,
  FOREIGN KEY (ip_id) REFERENCES ip(id)
);""",
    Tables.IP_PORT: """CREATE TABLE ip_port (
  scan_id INT,
  ip_id INT,
  port_id INT,
  FOREIGN KEY (scan_id) REFERENCES scan(id),
  FOREIGN KEY (ip_id) REFERENCES ip(id),
  FOREIGN KEY (port_id) REFERENCES port(id),
  PRIMARY KEY (scan_id, ip_id, port_id)
);
""",
    Tables.IP_CVE: """CREATE TABLE ip_cve (
  scan_id INT,
  ip_id INT,
  cve_id INT,
  FOREIGN KEY (scan_id) REFERENCES scan(id),
  FOREIGN KEY (ip_id) REFERENCES ip(id),
  FOREIGN KEY (cve_id) REFERENCES cve(id),
  PRIMARY KEY (scan_id, ip_id, cve_id)
);
""",
}
