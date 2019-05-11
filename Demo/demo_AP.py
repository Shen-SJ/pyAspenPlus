import pyAspenPlus
import os
import time

path = os.path.join(os.path.abspath('.'), "TestFile", "DistillationColumn.apw")
# path = r'D:\Google Cloud\沈孝錚\Aspen\AllylAlcohol Dehydration\Ally Alcohol Dehydration by ED with EG.apw'
Aspen = pyAspenPlus.AP(path)
obj = Aspen.aspen.Tree.FindNode("\Data\Streams\B1\Output\TOT_FLOW")


def basic_function():
    print(Aspen.FileStatus())
    Aspen.Show(True)
    Aspen.Show(False)
    Aspen.Unit()
    Aspen.Unit([1])
    Aspen.Unit([1,1])
    Aspen.UnitFind(obj)
    Aspen.UnitChange(obj, 1)
    # 三種ListXXX()
    Aspen.ListBlocks()
    Aspen.ListStreams()
    Aspen.ListComponents()
    # 三種XXXList()
    print(Aspen.BlocksList())
    print(Aspen.StreamsList())
    print(Aspen.ComponentsList())
    Aspen.Connections('c1')
    print(Aspen.BlockType('c1'))


def stream_function():
    print(Aspen.Stream.getMoleFlow('b1'))
    print(Aspen.Stream.getMoleFlow('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getMoleFlow('b1', component='water'))
    print(Aspen.Stream.getMoleFrac('b1', 'water'))
    print(Aspen.Stream.getMassFlow('b1'))
    print(Aspen.Stream.getMassFlow('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getMassFlow('b1', component='water'))
    print(Aspen.Stream.getMassFrac('b1', 'water'))
    print(Aspen.Stream.getTemperature('b1'))
    print(Aspen.Stream.getTemperature('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getPressure('b1'))
    print(Aspen.Stream.getPressure('b1', get_unit=False, unit_change_to=1))
    print(Aspen.Stream.getVaporFrac('b1'))
    print(Aspen.Stream.getVolumeFlow('b1'))
    print(Aspen.Stream.getVolumeFlow('b1', get_unit=False, unit_change_to=1))


def distillation_function():
    print(Aspen.Distillation.getNStage('c1'))
    Aspen.Distillation.setNStage('c1', 40)
    print(Aspen.Distillation.getDiameter('c2-size'))
    print(Aspen.Distillation.getDiameter('c2-size', get_unit=False, unit_change_to=1))
    print(Aspen.Distillation.getHeight('c1'))
    print(Aspen.Distillation.getHeight('c1', get_unit=True))
    print(Aspen.Distillation.getQR('c2-size'))
    print(Aspen.Distillation.getQR('c2-size', get_unit=False, unit_change_to=1))
    print(Aspen.Distillation.getQC('c2-size'))
    print(Aspen.Distillation.getQC('c2-size', get_unit=False, unit_change_to=1))


def heater_test():
    print(Aspen.Heater.getQ('c4-con'))
    print(Aspen.Heater.getQ('c4-con', get_unit=True, unit_change_to=1))


Aspen.Close()
