import AspenPlus

path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
Aspen = AspenPlus.AP(path)
obj = Aspen.aspen.Tree.FindNode("\Data\Streams\B1\Output\TOT_FLOW")

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


## 測試用的兩個參數路徑
## Application.Tree.Data.Streams.B1.Output.TOT_FLOW
## Application.Tree.FindNode("\Data\Streams\B1\Output\TOT_FLOW")

# 測試Close()
Aspen.Close()

