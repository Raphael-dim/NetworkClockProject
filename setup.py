from setuptools import setup, find_packages

setup(
    name="NetworkClockProject",
    version="1.0.0",
    description="Network Clock application with privilege separation",
    packages=find_packages(),
    install_requires=[
        # List dependencies here
        "flask",
        "pytest",
        
    ],
    entry_points={
        "console_scripts": [
            "network-clock=nc.server:start_server",
        ],
    },
)
