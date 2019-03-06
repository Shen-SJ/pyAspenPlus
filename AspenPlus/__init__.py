#############################################################
############                                      ###########
##########            我的設計理念哈哈哈            #########
############                                      ###########
#############################################################
#############################################################
####   還要再創造distillation的sub-class，裡面包含板數   ####
####    、塔徑、冷凝器(可選有或無)、再沸器(可選有或無)   ####
####    ，再來是冷卻器的duty，萃取塔的板數、塔徑(需擷取  ####
####    兩進料物流體積流率計算)。如果行有餘力，把蒸餾塔  ####
####    (包含再沸器、冷凝器)、冷卻器的TAC公式也弄一弄吧！####
####                                                     ####
####    之後再搞個 Get_nstage與 Set_nstage !! 就可以     ####
####    進行我偉大的OPT自動化了!!!                       ####
####                                                     ####
#############################################################
#############################################################

def AP(path):
    # 匯入兩個重要模組，此函數主要是輸出AP類別用
    # ，不過在輸出前添加了Stream類別
    from AspenPlus import Basic
    from AspenPlus import Stream
    from AspenPlus import Distillation
    from AspenPlus import Heater
    from AspenPlus import Extract
    from AspenPlus import Cost

    A = Basic.AP(path)
    A.Stream = Stream.Stream(A)
    A.Distillation = Distillation.Distillation(A)
    A.Heater = Heater.Heater(A)
    A.Extractor = Extract.Extractor(A)
    A.Cost = Cost.Cost(A)

    return A

if __name__ == '__main__':
    print("in __init__.py")
    path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
    Aspen = AP(path)

    Aspen.Close()

