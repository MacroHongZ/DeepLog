from setuptools import setup, find_packages

setup(
    name="deeplog",
    version="1.0",
    author="MacroHongZ",
    author_email="anghongzhunsix@qq.com",

    description="Log the deep learning project",

    packages=find_packages(),

    install_requires=[
        'matplotlib'
    ],
)
