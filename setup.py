from setuptools import find_packages, setup

# Function to parse requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

setup(
    name="personal_email_assistant",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        "console_scripts": [
            # If you have scripts to run from the command line, define them here
            # 'command_name = your_package.module:function',
        ],
    },
)
