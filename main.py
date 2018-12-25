import AspenPlus

path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
Aspen = AspenPlus.AP(path)
obj = Aspen.aspen.Tree.FindNode("\Data\Streams\B1\Output\TOT_FLOW")

def basic_test():
    n = 0
    # 測試Error()
    print(Aspen.Error())
    # 測試Show()
    Aspen.Show(True)
    Aspen.Show(False)
    try:
        Aspen.Show(123)
    except TypeError:
        n = 1
        print('Error' + str(n)) # 應為1
    # 測試Unit()
    Aspen.Unit([])
    Aspen.Unit([],table=True)
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
    print(Aspen.Stream.MoleFlow('b1'))
    print(Aspen.Stream.MoleFlow('b1',get_unit=True))
    print(Aspen.Stream.MoleFlow('b1',get_unit=False,unit_change_to=1))
    print(Aspen.Stream.MoleFlow('b1', get_unit=True, unit_change_to=1))
    print(Aspen.Stream.MoleFlow('b1', component='water'))
    print(Aspen.Stream.MoleFlow('b1', component='water',get_unit=True))
    print(Aspen.Stream.MoleFlow('b1', component='water',get_unit=False, unit_change_to=1))
    print(Aspen.Stream.MoleFlow('b1', component='water',get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.MoleFlow('b2')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為1
    try:
        Aspen.Stream.MoleFlow(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為2
    try:
        Aspen.Stream.MoleFlow('b1',get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為3
    try:
        Aspen.Stream.MoleFlow('b1',get_unit=False,unit_change_to=True)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為4
    try:
        Aspen.Stream.MoleFlow('b1',component=123, get_unit=False, unit_change_to=1)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為5

    # 測試MoleFrac()
    print(Aspen.Stream.MoleFrac('b1','water'))
    try:
        Aspen.Stream.MoleFrac('b2','water')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為6
    try:
        Aspen.Stream.MoleFrac('b1','waterr')
    except AspenPlus.UserDifineException.AspenPlus_ComponentTypeError:
        n += 1
        print('Error' + str(n))  # 應為7
    try:
        Aspen.Stream.MoleFrac(123,'waterr')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為8
    try:
        Aspen.Stream.MoleFrac('b1',123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為9

    # 測試MassFlow()
    print(Aspen.Stream.MassFlow('b1'))
    print(Aspen.Stream.MassFlow('b1',get_unit=True))
    print(Aspen.Stream.MassFlow('b1',get_unit=False,unit_change_to=1))
    print(Aspen.Stream.MassFlow('b1', get_unit=True, unit_change_to=1))
    print(Aspen.Stream.MassFlow('b1', component='water'))
    print(Aspen.Stream.MassFlow('b1', component='water',get_unit=True))
    print(Aspen.Stream.MassFlow('b1', component='water',get_unit=False, unit_change_to=1))
    print(Aspen.Stream.MassFlow('b1', component='water',get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.MassFlow('b2')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為10
    try:
        Aspen.Stream.MassFlow(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為11
    try:
        Aspen.Stream.MassFlow('b1',get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為12
    try:
        Aspen.Stream.MassFlow('b1',get_unit=False,unit_change_to=True)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為13
    try:
        Aspen.Stream.MassFlow('b1',component=123, get_unit=False, unit_change_to=1)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為14

    # 測試MassFrac()
    print(Aspen.Stream.MassFrac('b1','water'))
    try:
        Aspen.Stream.MassFrac('b2','water')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為15
    try:
        Aspen.Stream.MassFrac('b1','waterr')
    except AspenPlus.UserDifineException.AspenPlus_ComponentTypeError:
        n += 1
        print('Error' + str(n))  # 應為16
    try:
        Aspen.Stream.MassFrac(123,'waterr')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為17
    try:
        Aspen.Stream.MassFrac('b1',123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為18

    # 測試Temperature()
    print(Aspen.Stream.Temperature('b1'))
    print(Aspen.Stream.Temperature('b1', get_unit=True))
    print(Aspen.Stream.Temperature('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.Temperature('b1', get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.Temperature('b2')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為19
    try:
        Aspen.Stream.Temperature(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為20
    try:
        Aspen.Stream.Temperature('b1',get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為21
    try:
        Aspen.Stream.Temperature('b1',get_unit=False,unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為22

    # 測試Pressure()
    print(Aspen.Stream.Pressure('b1'))
    print(Aspen.Stream.Pressure('b1', get_unit=True))
    print(Aspen.Stream.Pressure('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.Pressure('b1', get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.Pressure('b2')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為23
    try:
        Aspen.Stream.Pressure(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為24
    try:
        Aspen.Stream.Pressure('b1', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為25
    try:
        Aspen.Stream.Pressure('b1', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為26

    # 測試VaporFrac()
    print(Aspen.Stream.VaporFrac('b1'))
    try:
        Aspen.Stream.VaporFrac('b2')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為27
    try:
        Aspen.Stream.VaporFrac(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為28

    # 測試VolumeFlow()
    print(Aspen.Stream.VolumeFlow('b1'))
    print(Aspen.Stream.VolumeFlow('b1', get_unit=True))
    print(Aspen.Stream.VolumeFlow('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.VolumeFlow('b1', get_unit=True, unit_change_to=1))
    try:
        Aspen.Stream.VolumeFlow('b2')
    except AspenPlus.UserDifineException.AspenPlus_StreamTypeError:
        n += 1
        print('Error' + str(n))  # 應為29
    try:
        Aspen.Stream.VolumeFlow(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為30
    try:
        Aspen.Stream.VolumeFlow('b1', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為31
    try:
        Aspen.Stream.VolumeFlow('b1', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為32

def disillation_test():
    n = 0
    # 測試NStage()
    print(Aspen.Distillation.NStage('c1'))
    Aspen.Distillation.NStage('c1',40)
    print(Aspen.Distillation.NStage('c1'))
    try:
        Aspen.Distillation.NStage('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print("Error" + str(n)) # 應為1
    try:
        Aspen.Distillation.NStage(123)
    except TypeError:
        n += 1
        print("Error" + str(n))  # 應為2
    # 測試Diameter()
    print(Aspen.Distillation.Diameter('c2-size'))
    print(Aspen.Distillation.Diameter('c2-size', get_unit=True))
    print(Aspen.Distillation.Diameter('c2-size', get_unit=False, unit_change_to=1))
    print(Aspen.Distillation.Diameter('c2-size', get_unit=True, unit_change_to=1))
    try:
        Aspen.Distillation.Diameter('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為3
    try:
        Aspen.Distillation.Diameter(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為4
    try:
        Aspen.Distillation.Diameter('c2-size', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為5
    try:
        Aspen.Distillation.Diameter('c2-size', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為6
    try:
        Aspen.Distillation.Diameter('c1')
    except AspenPlus.UserDifineException.AspenPlus_SizingError:
        n += 1
        print('Error' + str(n))  # 應為7
    # 測試Height()
    print(Aspen.Distillation.Height('c1'))
    print(Aspen.Distillation.Height('c1',get_unit=True))
    try:
        Aspen.Distillation.Height('c2',get_unit=True)
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為8
    try:
        Aspen.Distillation.Height(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為9
    try:
        Aspen.Distillation.Height('c1',get_unit='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為10
    # 測試QR()
    print(Aspen.Distillation.QR('c2-size'))
    print(Aspen.Distillation.QR('c2-size', get_unit=True))
    print(Aspen.Distillation.QR('c2-size', get_unit=False, unit_change_to=1))
    print(Aspen.Distillation.QR('c2-size', get_unit=True, unit_change_to=1))
    print(Aspen.Distillation.QR('c3'))
    print(Aspen.Distillation.QR('c4'))
    try:
        Aspen.Distillation.QR('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為11
    try:
        Aspen.Distillation.QR(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應12
    try:
        Aspen.Distillation.QR('c2-size', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為13
    try:
        Aspen.Distillation.QR('c2-size', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為14
    # 測試QC()
    print(Aspen.Distillation.QC('c2-size'))
    print(Aspen.Distillation.QC('c2-size', get_unit=True))
    print(Aspen.Distillation.QC('c2-size', get_unit=False, unit_change_to=1))
    print(Aspen.Distillation.QC('c2-size', get_unit=True, unit_change_to=1))
    print(Aspen.Distillation.QC('c3'))
    print(Aspen.Distillation.QC('c4'))
    try:
        Aspen.Distillation.QC('c2')
    except AspenPlus.UserDifineException.AspenPlus_BlockTypeError:
        n += 1
        print('Error' + str(n))  # 應為15
    try:
        Aspen.Distillation.QC(123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應16
    try:
        Aspen.Distillation.QC('c2-size', get_unit=123)
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為17
    try:
        Aspen.Distillation.QC('c2-size', get_unit=False, unit_change_to='')
    except TypeError:
        n += 1
        print('Error' + str(n))  # 應為18


# basic_test()
# stream_test()
disillation_test()

## 測試用的兩個參數路徑
## Application.Tree.Data.Streams.B1.Output.TOT_FLOW
## Application.Tree.FindNode("\Data\Streams\B1\Output\TOT_FLOW")
## Application.Tree.FindNode("\Data\Blocks\C1\Comments\#0") 列出單元的comment

# 測試Close()
Aspen.Close()

