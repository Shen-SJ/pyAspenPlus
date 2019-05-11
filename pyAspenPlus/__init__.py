

def AP(path, version=None):
    # 匯入兩個重要模組，此函數主要是輸出AP類別用
    # ，不過在輸出前添加了Stream類別
    from pyAspenPlus import Basic
    from pyAspenPlus import Stream
    from pyAspenPlus import Distillation
    from pyAspenPlus import Heater
    from pyAspenPlus import Extract
    from pyAspenPlus import Decanter
    from pyAspenPlus import Cost

    A = Basic.AP(path, version=version)
    A.Stream = Stream.Stream(A)
    A.Distillation = Distillation.Distillation(A)
    A.Heater = Heater.Heater(A)
    A.Extractor = Extract.Extractor(A)
    A.Decanter = Decanter.Decanter(A)
    A.Cost = Cost.Cost(A)

    return A


if __name__ == '__main__':
    print("in __init__.py")
    path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
    Aspen = AP(path)

    Aspen.Close()

