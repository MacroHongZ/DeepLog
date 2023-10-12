from setuptools import setup, find_packages

setup(
    name="deeplog",
    version="1.1.8",
    author="MacroHongZ",
    author_email="wanghongzhunsix@qq.com",
    url='https://github.com/MacroHongZ/DeepLog',

    description="Log the deep learning project",

    packages=find_packages(),

    install_requires=[
        'matplotlib'
    ],
)
