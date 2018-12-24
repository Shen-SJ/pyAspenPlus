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

# TODO: 先把檔案從AspenFile全部讀進來會快速很多，
#  像是用字典儲存所有東西。
#  果真聽均一席話勝過十年書！！ 2018.12.24

def AP(path):
    # 匯入兩個重要模組，此函數主要是輸出AP類別用
    # ，不過在輸出前添加了Stream類別
    from AspenPlus import Basic
    from AspenPlus import Stream

    A = Basic.AP(path)
    A.Stream = Stream.Stream(A)

    return A

if __name__ == '__main__':
    print("in __init__.py")
    path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
    Aspen = AP(path)
    Aspen.Close()

##### 我她媽找到的aspen參數讀取啊!!!(其實把滑鼠移到此參數名稱上面，就會顯示對應index)
## aspen.Tree.Data.Blocks.Elements("C1").AttributeValue(0)
## 讀取Value
## aspen.Tree.Data.Blocks.Elements("C1").AttributeValue(2)
## 讀取Physical Quantity.
## aspen.Tree.Data.Blocks.Elements("C1").AttributeValue(3)
## 讀取Unit of Measure.
## aspen.Tree.Data.Blocks.Elements("C1").AttributeValue(6)
## 讀取Record Type. ex:RadFrac
## aspen.Tree.Data.Blocks.Elements("C1").AttributeValue(12)
## 讀取Completion Status.這個看例子比較懂
## 上面的函式輸出為9345，aspen上面顯示(0x00002481 = HAP_RE  \\
## SULTS_SUCCESS|HAP_INPUT_COMPLETE|HAP_UNRECONCILED|HAP_ENABLED)
## 9345為十進位，轉換成16進位就是2481了
## aspen.Tree.Data.Blocks.Elements("C1").AttributeValue(13)
## 讀取Basis. Ex:MOLE
## aspen.Tree.Data.Blocks.Elements("C1").AttributeValue(18)
## 讀取Output
## aspen.Tree.Data.Blocks.Elements("C1").AttributeValue(24)
## 讀取Name. ex:C1

##### For 萃取塔
## aspen.Tree.FindNode("\Data\Blocks\EXTOWER\Input\TRAY_OPTION")
## 選擇密度差是否顯示。有三種value,"BRIEF","INCL-TRAYS","ALL-TRAYS"

