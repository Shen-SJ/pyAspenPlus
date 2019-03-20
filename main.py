import AspenPlus
import os
import time

path = os.path.join(os.path.abspath('.'), "TestFile", "DistillationColumn.apw")
# path = r'D:\Google Cloud\沈孝錚\Aspen\AllylAlcohol Dehydration\Ally Alcohol Dehydration by ED with EG.apw'
Aspen = AspenPlus.AP(path)
obj = Aspen.aspen.Tree.FindNode("\Data\Streams\B1\Output\TOT_FLOW")

def basic_test():
    n = 0
    # 測試Error()
    print(Aspen.FileStatus())
    # 測試Show()
    Aspen.Show(True)
    Aspen.Show(False)
    try:
        Aspen.Show(123)
    except TypeError:
        n = 1
        print('Error' + str(n)) # 應為1
    # 測試Unit()
    Aspen.Unit()
    Aspen.Unit(table=True)
    Aspen.Unit([1])
    Aspen.Unit([1],table=True)
    Aspen.Unit([1,1])
    Aspen.Unit([1,1],table=True)
    try:
        Aspen.Unit(123)
    except TypeError:
        n += 1
        print('Error' + str(n)) # 應為2
    try:
        Aspen.Unit([],123)
    except TypeError:
        n += 1
        print('Error' + str(n)) # 應為3
    # 測試UnitFind()
    Aspen.UnitFind(obj)
    Aspen.UnitFind(obj, table=True)
    try:
        Aspen.UnitFind(123)
    except AttributeError:
        n += 1
        print('Error' + str(n)) # 應為4
    try:
        Aspen.UnitFind(obj,table=123)
    except TypeError:
        n += 1
        print('Error' + str(n)) # 應為5
    # 測試UnitChange()
    Aspen.UnitChange(obj, 1)
    try:
        Aspen.UnitChange(123,1)
    except AttributeError:
        n += 1
        print('Error' + str(n))  # 應為6
    try:
        Aspen.UnitChange(obj, '123')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為7
    # 測試三種ListXXX()
    Aspen.ListBlocks()
    Aspen.ListStreams()
    Aspen.ListComponents()
    # 測試三種XXXList()
    print(Aspen.BlocksList())
    print(Aspen.StreamsList())
    print(Aspen.ComponentsList())
    # 測試Connections()
    Aspen.Connections('c1')
    print(Aspen.Connections('C1',table=True))
    try:
        Aspen.Connections('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為8
    try:
        Aspen.Connections('c1',table=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為9
    try:
        Aspen.Connections(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為10
    # 測試BlockType()
    print(Aspen.BlockType('c1'))
    try:
        Aspen.BlockType('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為11
    try:
        Aspen.BlockType(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為12

def stream_test():
    n = 0
    # 測試MoleFlow()
    print(Aspen.Stream.getMoleFlow('b1'))
    print(Aspen.Stream.getMoleFlow('b1', get_unit=True))
    print(Aspen.Stream.getMoleFlow('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getMoleFlow('b1', get_unit=True, unit_change_to=1))
    print(Aspen.Stream.getMoleFlow('b1', component='water'))
    print(Aspen.Stream.getMoleFlow('b1', component='water', get_unit=True))
    print(Aspen.Stream.getMoleFlow('b1', component='water', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getMoleFlow('b1', component='water', get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.getMoleFlow('b11')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為1
    try:
        Aspen.Stream.getMoleFlow(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為2
    try:
        Aspen.Stream.getMoleFlow('b1', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為3
    try:
        Aspen.Stream.getMoleFlow('b1', get_unit=False, unit_change_to=True)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為4
    try:
        Aspen.Stream.getMoleFlow('b1', component=123, get_unit=False, unit_change_to=1)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為5

    # 測試MoleFrac()
    print(Aspen.Stream.getMoleFrac('b1', 'water'))
    try:
        Aspen.Stream.getMoleFrac('b11', 'water')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為6
    try:
        Aspen.Stream.getMoleFrac('b1', 'waterr')
    except AspenPlus.UserDifineException.AspenPlus_ComponentTypeError:
        n += 1
        print('Error' + str(n))  # 應為7
    try:
        Aspen.Stream.getMoleFrac(123, 'waterr')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為8
    try:
        Aspen.Stream.getMoleFrac('b1', 123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為9

    # 測試MassFlow()
    print(Aspen.Stream.getMassFlow('b1'))
    print(Aspen.Stream.getMassFlow('b1', get_unit=True))
    print(Aspen.Stream.getMassFlow('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getMassFlow('b1', get_unit=True, unit_change_to=1))
    print(Aspen.Stream.getMassFlow('b1', component='water'))
    print(Aspen.Stream.getMassFlow('b1', component='water', get_unit=True))
    print(Aspen.Stream.getMassFlow('b1', component='water', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getMassFlow('b1', component='water', get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.getMassFlow('b11')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為10
    try:
        Aspen.Stream.getMassFlow(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為11
    try:
        Aspen.Stream.getMassFlow('b1', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為12
    try:
        Aspen.Stream.getMassFlow('b1', get_unit=False, unit_change_to=True)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為13
    try:
        Aspen.Stream.getMassFlow('b1', component=123, get_unit=False, unit_change_to=1)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為14

    # 測試MassFrac()
    print(Aspen.Stream.getMassFrac('b1', 'water'))
    try:
        Aspen.Stream.getMassFrac('b11', 'water')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為15
    try:
        Aspen.Stream.getMassFrac('b1', 'waterr')
    except AspenPlus.UserDifineException.AspenPlus_ComponentTypeError:
        n += 1
        print('Error' + str(n))  # 應為16
    try:
        Aspen.Stream.getMassFrac(123, 'waterr')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為17
    try:
        Aspen.Stream.getMassFrac('b1', 123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為18

    # 測試Temperature()
    print(Aspen.Stream.getTemperature('b1'))
    print(Aspen.Stream.getTemperature('b1', get_unit=True))
    print(Aspen.Stream.getTemperature('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getTemperature('b1', get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.getTemperature('b11')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為19
    try:
        Aspen.Stream.getTemperature(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為20
    try:
        Aspen.Stream.getTemperature('b1', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為21
    try:
        Aspen.Stream.getTemperature('b1', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為22

    # 測試Pressure()
    print(Aspen.Stream.getPressure('b1'))
    print(Aspen.Stream.getPressure('b1', get_unit=True))
    print(Aspen.Stream.getPressure('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getPressure('b1', get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.getPressure('b11')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為23
    try:
        Aspen.Stream.getPressure(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為24
    try:
        Aspen.Stream.getPressure('b1', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為25
    try:
        Aspen.Stream.getPressure('b1', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為26

    # 測試VaporFrac()
    print(Aspen.Stream.getVaporFrac('b1'))
    try:
        Aspen.Stream.getVaporFrac('b11')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為27
    try:
        Aspen.Stream.getVaporFrac(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為28

    # 測試VolumeFlow()
    print(Aspen.Stream.getVolumeFlow('b1'))
    print(Aspen.Stream.getVolumeFlow('b1', get_unit=True))
    print(Aspen.Stream.getVolumeFlow('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getVolumeFlow('b1', get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.getVolumeFlow('b11')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為29
    try:
        Aspen.Stream.getVolumeFlow(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為30
    try:
        Aspen.Stream.getVolumeFlow('b1', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為31
    try:
        Aspen.Stream.getVolumeFlow('b1', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為32

def distillation_test():
    n = 0
    # 測試 getNStage()
    print(Aspen.Distillation.getNStage('c1'))
    print(Aspen.Distillation.getNStage('c1'))
    try:
        Aspen.Distillation.getNStage('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print("Error" + str(n)) # 應為1
    try:
        Aspen.Distillation.getNStage('c4-con')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print("Error" + str(n)) # 應為2
    try:
        Aspen.Distillation.getNStage(123)
    except TypeError:
        n += 1
        print("Error" + str(n))  # 應為3
    # 測試 setNStage
    Aspen.Distillation.setNStage('c1', 40)
    print(Aspen.Distillation.getNStage('c1'))
    try:
        Aspen.Distillation.setNStage('c2', 40)
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print("Error" + str(n))  # 應為4
    try:
        Aspen.Distillation.setNStage('c1', 40.1)
    except TypeError:
        n += 1
        print("Error" + str(n))  # 應為5
    try:
        Aspen.Distillation.setNStage('c1', '')
    except TypeError:
        n += 1
        print("Error" + str(n))  # 應為6
    try:
        Aspen.Distillation.setNStage(123, 40)
    except TypeError:
        n += 1
        print("Error" + str(n))  # 應為7
    # 測試Diameter()
    print(Aspen.Distillation.getDiameter('c2-size'))
    print(Aspen.Distillation.getDiameter('c2-size', get_unit=True))
    print(Aspen.Distillation.getDiameter('c2-size', get_unit=False, unit_change_to=1))
    print(Aspen.Distillation.getDiameter('c2-size', get_unit=True, unit_change_to=1))
    try:
        Aspen.Distillation.getDiameter('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為8
    try:
        Aspen.Distillation.getDiameter('c4-con')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為9
    try:
        Aspen.Distillation.getDiameter(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為10
    try:
        Aspen.Distillation.getDiameter('c2-size', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為11
    try:
        Aspen.Distillation.getDiameter('c2-size', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為12
    try:
        Aspen.Distillation.getDiameter('c1')
    except AspenPlus.UserDifineException.AspenPlus_SizingError:
        n += 1
        print('Error' + str(n))  # 應為13
    # 測試Height()
    print(Aspen.Distillation.getHeight('c1'))
    print(Aspen.Distillation.getHeight('c1', get_unit=True))
    try:
        Aspen.Distillation.getHeight('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為14
    try:
        Aspen.Distillation.getHeight('c4-con')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為15
    try:
        Aspen.Distillation.getHeight(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為16
    try:
        Aspen.Distillation.getHeight('c1', get_unit='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為17
    # 測試QR()
    print(Aspen.Distillation.getQR('c2-size'))
    print(Aspen.Distillation.getQR('c2-size', get_unit=True))
    print(Aspen.Distillation.getQR('c2-size', get_unit=False, unit_change_to=1))
    print(Aspen.Distillation.getQR('c2-size', get_unit=True, unit_change_to=1))
    print(Aspen.Distillation.getQR('c3'))
    print(Aspen.Distillation.getQR('c4'))
    try:
        Aspen.Distillation.getQR('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為18
    try:
        Aspen.Distillation.getQR('c4-con')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為19
    try:
        Aspen.Distillation.getQR(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應20
    try:
        Aspen.Distillation.getQR('c2-size', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為21
    try:
        Aspen.Distillation.getQR('c2-size', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為22
    # 測試QC()
    print(Aspen.Distillation.getQC('c2-size'))
    print(Aspen.Distillation.getQC('c2-size', get_unit=True))
    print(Aspen.Distillation.getQC('c2-size', get_unit=False, unit_change_to=1))
    print(Aspen.Distillation.getQC('c2-size', get_unit=True, unit_change_to=1))
    print(Aspen.Distillation.getQC('c3'))
    print(Aspen.Distillation.getQC('c4'))
    try:
        Aspen.Distillation.getQC('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為23
    try:
        Aspen.Distillation.getQC('c4-con')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為24
    try:
        Aspen.Distillation.getQC(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應25
    try:
        Aspen.Distillation.getQC('c2-size', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為26
    try:
        Aspen.Distillation.getQC('c2-size', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為27

def heater_test():
    n = 0
    ## 測試Q()
    print(Aspen.Heater.getQ('c4-con'))
    print(Aspen.Heater.getQ('c4-con', get_unit=True))
    print(Aspen.Heater.getQ('c4-con', unit_change_to=1))
    print(Aspen.Heater.getQ('c4-con', get_unit=True, unit_change_to=1))
    try:
        Aspen.Heater.getQ('c44-con')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print("Error" + str(n))  # 應為1
    try:
        Aspen.Heater.getQ(123)
    except TypeError:
        n += 1
        print("Error" + str(n))  # 應為2
    try:
        Aspen.Heater.getQ('c4-con', get_unit=123)
    except TypeError:
        n += 1
        print("Error" + str(n))  # 應為3
    try:
        Aspen.Heater.getQ('c4-con', unit_change_to='')
    except TypeError:
        n += 1
        print("Error" + str(n))  # 應為4


# basic_test()
# stream_test()
# distillation_test()
heater_test()

## 測試用的兩個參數路徑
## Application.Tree.Data.Streams.B1.Output.TOT_FLOW
## Application.Tree.FindNode("\Data\Streams\B1\Output\TOT_FLOW")
## Application.Tree.FindNode("\Data\Blocks\C1\Comments\#0") 列出單元的comment

# 測試Close()
# print(Aspen.Cost.SteamType('c1'))
# print(Aspen.Cost.WaterType('c1'))
# print(Aspen.Distillation.getNF('c1'))
# print(Aspen.Distillation.getNF('c1', sname='f1'))
Aspen.Unit([1])

print(Aspen.Decanter.getVolume('dec'), Aspen.Decanter.getVolume('dec', get_unit=True))
print(Aspen.Decanter.getDiameter('dec'), Aspen.Decanter.getDiameter('dec', get_unit=True))
print(Aspen.Decanter.getHeight('dec'), Aspen.Decanter.getHeight('dec', get_unit=True))
Aspen.Close()

