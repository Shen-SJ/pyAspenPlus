# pyAspenPlus
> This is a Python package for AspenPlus manipulating.
>It contains basic operation like read stream data, block data, 
>get the equipment sizing data. Additionally, it include some 
>function for connecting the data from AspenPlus file to MS Visio file, 
>but it have to built the Visio file first. 

## Table of contents
* [General info](#general-info)
* [Code Examples](#code-examples)
* [Features](#features)
* [Status](#status)
* [Inspiration](#inspiration)
* [License](#license)
* [Contact](#contact)

## General info
It is a very time-consuming procedure for copying the data from the AspenFile to VisioFile and 
optimization the process hand by hand. I want to build the program can automatic do these kind 
of things.

## Code Examples
#### Starting using pyAspenPlus
After installing the pyAspenPlus package, the package should be imported:
```python
import pyAspenPlus
```
and you have to built the Aspen instance and give the AspenFile path to them:
```python
Aspen = pyAspenPlus.AP(path)
```
You can start to use this package now!!!
#### Get the stream, column, heater... data from AspenFile
The later part will let you now how to get the data from AspnFile.  
If you want to know the temperature of **stream FF**, you should:
```python
Aspen.Stream.getTemperature('FF')
```
If you want to know the unit of this data:
```python
Aspen.Stream.getTemperature('FF', get_unit=True)
```

## Features
* Could get the **stream data** like moleflow, molefraction, temperature... etc.
* Could get the **distillation column data** like total number of stages, 
diameter, height... etc.
* Could get the **decanter data** like diameter, height, volume.
* Could get the **extractor data** like total number of stages, diameter, height.
* Could get the **heater data** like area, heat transfer duty.

To-do list:
* TAC calculation
* Automatically optimization procedure.

## Status
Project is: _in progress_.  
In the future, it may add a new feature of TAC calculation and 
automatically optimization function.

## Inspiration
These code are based on the AspenPlus V10 user guide and 
[MS Visio VBA reference](https://docs.microsoft.com/zh-tw/office/vba/api/overview/visio).

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

## Contact
Created by [@Shen, Shiau-Jeng](https://www.facebook.com/profile.php?id=100002730226702) - feel free to contact me!