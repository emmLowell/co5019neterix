# Server Ping using Nmap and Vulcan

This is a Python script that utilizes Nmap and Vulcan to ping one or multiple servers. The script allows you to specify IP addresses or ranges, as well as ports to scan.

---

## Installation
To use this script, you must first install the required libraries. You can do this using pip:

```bash
pip install -r requirements.txt
```

> Don't forget to edit configs in configs/ & website/Neterix/settings.py
> be sure to follow django's settings https://docs.djangoproject.com/en/4.2/topics/settings/

## Usage
To use the web script, run the following command in your terminal:

Development use only (not recommended for production):

```bash
python main.py
```

for production checkout https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/

<project_name> is wsgi.py is found in website/Neterix/wsgi.py


to run the background script run the following command in your terminal:

```bash
python main.py -s
```

