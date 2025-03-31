from setuptools import setup, find_packages

setup(
    name="checkson",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.7.0",
        "httpx>=0.27.0",
        "typer>=0.9.0",
        "asyncio>=3.4.3",
        "aiohttp>=3.9.3",
        "python-dotenv>=1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "checkson=checkson.cli.main:app",
        ],
    },
    author="Nipicoco",
    description="A tool to check for available usernames and domain names",
    keywords="username, domain, availability, checker",
    python_requires=">=3.7",
) 