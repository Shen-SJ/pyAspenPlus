def AP(path):
    # 匯入兩個重要模組，此函數主要是輸出AP類別用
    # ，不過在輸出前添加了Stream類別
    from AspenPlus import Basic
    from AspenPlus import Stream
    from AspenPlus import Distillation

    A = Basic.AP(path)
    A.Stream = Stream.Stream(A)
    A.Distillation = Distillation.Distillation(A)

    return A

if __name__ == '__main__':
    print("in __init__.py")
    path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
    Aspen = AP(path)

    Aspen.Close()

