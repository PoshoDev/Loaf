import os
import sys
import json
import shutil
from rich import print

# Get the PyPI credentials.
creds = "pypi_creds.json"
if os.path.exists(creds):
    with open(creds, "r") as f:
        data = json.load(f)
else:
    print(f"[blink red]File '{creds}' does not exist!")
    sys.exit()
username = data["username"]
password = data["password"]
# Build the package.
try:
    os.system("python setup.py sdist bdist_wheel")
except Exception as e:
    print(f"[blink red]Error building package: {e}")
    sys.exit()
# Upload the package.
os.system(f"twine upload --username {username} --password {password} dist/*")
# Move the contents of the dist folder to "_Ignore/Builds".
dir_dest = "_Ignore/Builds"
dir_src = "dist"
if os.path.exists(dir_dest):
    for file in os.listdir(dir_src):
        shutil.move(os.path.join(dir_src, file), dir_dest)
else:
    print(f"[blink red]Directory '{dir_dest}' does not exist!")
    sys.exit()
# Remove the build and dist folders.
shutil.rmtree("build")
shutil.rmtree("dist")