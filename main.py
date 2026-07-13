import requests
import sys


class EchoAgentMock:
    '''
    This is echo agent mock. You can ask it questions about the image of the user.

    Assumptions:
    * We are assuming echo agent knows about images of client and he is our source of truth
    * We are assuming the question asked gonna be about the cve and if it is relevant for the image
    '''
    @classmethod
    def ask_about_image(cls, question):
        return "windows" in question.lower() or ".exe" in question.lower()


def get_deps(deps_path):
    #with open(deps_path, 'r') as f:
    #   deps_raw = f.read().split()

    deps_raw = ["Pillow==12.0.0"]

    return [package.split("==") for package in deps_raw]


def request_cve(package_name, package_version, echosystem="PyPI"):
    # The official OSV query endpoint
    url = "https://api.osv.dev/v1/query"

    # Construct the payload according to the OSV schema
    payload = {
        "version": package_version,
        "package": {
            "name": package_name,
            "ecosystem": echosystem
        }
    }

    try:
        # Send the POST request
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # The API returns a 'vulns' array if it finds matches
        return data.get("vulns", [])
    
    except requests.exceptions.RequestException as e:
        print(f"[!] Error connecting to the OSV API: {e}")
        sys.exit(1)


def is_image_vulnerable_by_cve(cve):
    return EchoAgentMock.ask_about_image(cve.get("details"))


if __name__ == '__main__':
    deps = get_deps(".\\requirements.txt")
    cves = []
    for package_name, package_version in deps:
        cves += request_cve(package_name, package_version)
    for cve in cves:
        if cve.get("database_specific", "") == "":
            continue
        if is_image_vulnerable_by_cve(cve) and cve.get("database_specific").get("severity", "HIGH") in ["HIGH", "CRITICAL"]:
            print("[!] DANGER - You are vulnerable to {}".format(cve["id"]))
        elif not is_image_vulnerable_by_cve(cve) and cve.get("database_specific").get("severity", "HIGH") in ["HIGH", "CRITICAL"]:
            print("[+] Severity downgraded to low (ID: {})".format(cve["id"]))
        else:
            # Do nothing
            pass
