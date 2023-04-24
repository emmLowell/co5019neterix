# Server Ping using Nmap and Vulcan

This is a Python script that utilizes Nmap and Vulcan to ping one or multiple servers. The script allows you to specify IP addresses or ranges, as well as ports to scan.

---

## Installation
To use this script, you must first install the required libraries. You can do this using pip:

```bash
pip install python-nmap vulcan
```

## Usage
To use the script, run the following command in your terminal:

```bash
python main.py
```

## Autopep Formatting
This project utilizes autopep8 for code formatting. To automatically format your code to conform to the PEP 8 style guide, you can run the following command in your terminal:

```bash
autopep8 --in-place --aggressive --aggressive <filename>
```
> This will apply PEP 8 formatting to the specified file,
> or use VSCode built in Format Document `ctrl` + `shift` + `p` -> Format Document


## Branches and Merging
To contribute to this project, please create a new branch for your changes. Once you have made your changes, create a pull request to merge your branch into the master branch.

Ensure branch names follow:
-  Feature branches: feature/[feature_name]
Used for developing new features or functionalities.

- Bugfix branches: bug/[bug_name]
Used for fixing bugs in the codebase.

- Suggestion branches: suggestion/[suggestion_name]
Used for implementing suggested changes or improvements.

```bash
git checkout -b <new_branch_name>
```

```bash
git add .
```

```bash
git commit -m "<commit_message>"
```

```bash
git push origin <new_branch_name>
```