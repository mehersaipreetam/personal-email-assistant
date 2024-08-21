from setuptools import find_packages, setup

setup(
    name="personal_email_assistant",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
        "console_scripts": [
            # If you have scripts to run from the command line, define them here
            # 'command_name = your_package.module:function',
        ],
    },
)
