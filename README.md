
# Context-Aware CVE Dependency Scanner

This Python script is a proof-of-concept vulnerability scanner. It checks project dependencies against the [OSV (Open Source Vulnerability) API](https://osv.dev/) and intelligently adjusts the severity of discovered vulnerabilities based on the specific context of the target deployment image (simulated here via a mock agent).

By evaluating whether a CVE is actually exploitable in the target environment (e.g., checking if the vulnerability is Windows-specific), the script helps reduce alert fatigue by downgrading the severity of irrelevant threats.

## Features

* **Automated OSV Integration:** Queries the official `api.osv.dev` endpoint to retrieve real-time vulnerability data for Python packages.
* **Context-Aware Evaluation (`EchoAgentMock`):** Simulates an agent that knows the target deployment environment. It parses CVE details and determines if the vulnerability is relevant (currently checks for Windows/`.exe` specific language).
* **Smart Severity Adjustment:** Retains `HIGH` or `CRITICAL` alerts for relevant vulnerabilities, but actively downgrades severity for vulnerabilities that do not affect the target image.

## Prerequisites

* Python 3.6+
* `requests` library

You can install the required dependency using pip:

```bash
pip install requests

```

## Usage

Simply run the script from your terminal:

```bash
python scanner.py

```

### Expected Output

The script will output alerts based on the severity and relevance of the findings:

* `[!] DANGER - You are vulnerable to <CVE-ID>` (If the CVE is High/Critical and relevant to the image).
* `[+] Severity downgraded to low (ID: <CVE-ID>)` (If the CVE is High/Critical but deemed irrelevant to the deployment environment).

## Code Structure

* **`EchoAgentMock`**: A mock class acting as the source of truth for the deployment environment. Its `ask_about_image` method returns `True` if the CVE text mentions "windows" or ".exe".
* **`get_deps(deps_path)`**: Parses a dependency file (like `requirements.txt`) to extract package names and versions.
* **`request_cve(package_name, package_version, echosystem)`**: Posts a query to the OSV API and returns a list of matched vulnerabilities.
* **`is_image_vulnerable_by_cve(cve)`**: Helper function to pass CVE details to the mock agent for contextual evaluation.

## ⚠️ Important Development Notes

If you are transitioning this code into a broader production environment, please note the following hardcoded elements currently active in the script:

1. **Hardcoded Dependencies:** The `get_deps` function currently bypasses reading the actual `requirements.txt` file and has hardcoded `["Pillow==12.0.0"]` for testing purposes. You will need to uncomment the file-reading logic to scan a real requirements file.
2. **Ecosystem Default:** The `request_cve` function defaults to the `PyPI` ecosystem. If you intend to scan non-Python packages in the future, you will need to make this parameter dynamic based on the parsed file.

---

Would you like me to help write the code to parse a real `requirements.txt` file instead of using the hardcoded `Pillow` dependency, or were you looking for a different kind of review for this updated version?