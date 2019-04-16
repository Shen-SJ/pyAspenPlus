from setuptools import setup
from os import path

# 目前的資料夾位置
pwd = path.abspath(path.dirname(__file__))

# with open(path.join(pwd, 'README.md')) as f:
#     Readme = f.read()

with open(path.join(pwd, 'LICENSE')) as f:
    License = f.read()

setup(
    name='pyAspenPlus',
    version='8.0',
    packages=['pyAspenPlus', 'pyAspenPlus.Visio'],
    url='https://github.com/Shen-SJ/pyAspenPlus',
    license=License,
    author='Shen, Shiau-Jeng',
    author_email='johnson840205@gmail.com',
    description='',
    # long_description=Readme,
    classifiers=[
            'Environment :: Win32 (MS Windows)',
            'Operating System :: Microsoft',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6'],
    install_requires=['pypiwin32'],
    include_package_data=True
)
