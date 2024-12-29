from setuptools import setup, find_packages

setup(
    name="currency_exchange",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.1.0",
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "currency-exchange=currency_exchange.cli:cli",
        ],
    },
)
