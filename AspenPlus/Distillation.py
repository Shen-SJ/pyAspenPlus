# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from AspenPlus import UserDifineException as UDE

class Distillation:
    def __init__(self, master):
        self.master = master
        self.aspen = master.aspen

    def NStage(self, bname, *set_value):
        """Get the number of stage for the specified RadFrac block.
                bname: Block name.
        """
        input_value = False
        ## 檢查set_value是否只有一個參數
        if len(set_value) > 1:
            raise TypeError("Only 1 value to be need for set_value !!!")

        ## 檢查輸入的資料型態正確與否
        if type(bname) != str:
            raise TypeError("bname must be a 'String'!!!")
        if len(set_value) == 1:
            if type(set_value[0]) != int:
                raise TypeError("set_value must be a 'Integer'!!!")
            else:   # 有輸入數值的話就啟動輸入模式
                input_value = True

        ## 把bname轉換成大寫，因為Aspen裡面的名稱都大寫
        bname = bname.upper()

        ## 檢查輸入的單元名稱是否在檔案當中，如無回傳錯誤
        if bname not in self.master.BlocksList():
            raise UDE.AspenPlus_BlockTypeError("Cannot Find " + bname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")

        path = "\Data\Blocks"+"\\"+bname+r"\Input\NSTAGE"
        if input_value is True:
            self.aspen.Tree.FindNode(path).Value = set_value[0]
        else:
            return self.aspen.Tree.FindNode(path).Value

    def Diameter(self, bname, get_unit=False, unit_change_to=[]):
        """Get the Column's diameter. Before using this function. you have to turn on the
                'Sizaing' or 'Rating' function in AspenPlus.
                bname: Block name.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        ## 此功能只能取sizing的結果不是取rating的結果
        ## 先檢查輸入的資料型態正確與否
        if type(bname) != str:
            raise TypeError("bname must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(unit_change_to) != list and type(unit_change_to) != int:
            raise TypeError("unit_change must be a 'Integer'!!!")

        ## 把bname轉換成大寫，因為Aspen裡面的名稱都大寫
        bname = bname.upper()

        ## 檢查輸入的單元名稱是否在檔案當中，如無回傳錯誤
        if bname not in self.master.BlocksList():
            raise UDE.AspenPlus_BlockTypeError("Cannot Find " + bname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")

        ## 檢查是否有開啟Sizing功能
        if self.aspen.Tree.FindNode(
                "\Data\Blocks" + "\\" + bname + "\Subobjects\Column Internals").AttributeValue(38) == 0:  # 用是否有子代判斷
            raise UDE.AspenPlus_SizingError("'Sizing' function dosen't open!!!")

        ## 確認是否為 Apwn36.0(V10)
        if self.aspen.Name.find('36.0') != -1:  # 第十版的直徑路徑
            path = "\Data\Blocks"+"\\"+bname+"\Subobjects\Column Internals\INT-1\Subobjects\Sections\CS-1\Input\CA_DIAM\INT-1\CS-1"
        else:   # V8.8以前的的直徑路徑
            path = "\Data\Blocks"+"\\"+bname+"\Subobjects\Tray Sizing\\1\Output\DIAM4\\1"

        ## 看看有沒有要改單位
        if unit_change_to == []:  # 沒有要改單位
            ## 是要取得數值還是單位
            if get_unit:  # 取得單位
                return self.master.UnitFind(self.aspen.Tree.FindNode(path), table=True)
            else:  # 取得數值
                return self.aspen.Tree.FindNode(path).Value
        elif unit_change_to != []:  # 要改單位的話
            if get_unit:  # 取得單位
                pq = self.aspen.Tree.FindNode(path).AttributeValue(2)
                return self.master.Unit(item=[pq, unit_change_to], table=True)
            else:  # 取得數值
                return self.master.UnitChange(self.aspen.Tree.FindNode(path), unit_change_to)

    def Height(self, bname, get_unit=False):
        """Get the Column's height. it is a  calculated value.
                Total number of trays(NT) with 2-ft spacing plus 20% extra length.
                It means  H[ft] = 2.4×(NT-1) which is equal to H[m] = 0.73152×(NT-1).
                Reference: Luyben, W. L.
                                , Comparison of extractive distillation and pressure-swing distillation for acetone/chloroform separation
                                . Comput Chem Eng 2013, 50, 1-7.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(bname) != str:
            raise TypeError("bname must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")

        ## 把bname轉換成大寫，因為Aspen裡面的名稱都大寫
        bname = bname.upper()

        ## 檢查輸入的單元名稱是否在檔案當中，如無回傳錯誤
        if bname not in self.master.BlocksList():
            raise UDE.AspenPlus_BlockTypeError("Cannot Find " + bname
                                               + " in the AspenFile. "
                                               + "Please Check the name you type!!")

        ## 取得指定蒸餾塔的總板數
        n = self.NStage(bname)

        ## 是要取得數值還是單位
        if get_unit:  # 取得單位
            return "meter"
        else:  # 取得數值
            return 0.73152*(n-1)

    def QR(self,bname, get_unit=False, unit_change_to=[]):
        """Get the reboiler duty of specified column.
                If it is not reboiler, the return value is 'None'.
                bname: Block name.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(bname) != str:
            raise TypeError("bname must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(unit_change_to) != list and type(unit_change_to) != int:
            raise TypeError("unit_change must be a 'Integer'!!!")

        ## 把bname轉換成大寫，因為Aspen裡面的名稱都大寫
        bname = bname.upper()

        ## 檢查輸入的單元名稱是否在檔案當中，如無回傳錯誤
        if bname not in self.master.BlocksList():
            raise UDE.AspenPlus_BlockTypeError("Cannot Find " + bname
                                               + " in the AspenFile. "
                                               + "Please Check the name you type!!")

        ## 檢查指定蒸餾塔有沒有reboiler
        path = "\Data\Blocks" + "\\" + bname + "\Input\REBOILER"
        if self.aspen.Tree.FindNode(path).Value == "NONE":
            return

        path = "\Data\Blocks" + "\\" + bname + "\Output\REB_DUTY"

        ## 看看有沒有要改單位
        if unit_change_to == []:  # 沒有要改單位
            ## 是要取得數值還是單位
            if get_unit:  # 取得單位
                return self.master.UnitFind(self.aspen.Tree.FindNode(path), table=True)
            else:  # 取得數值
                return self.aspen.Tree.FindNode(path).Value
        elif unit_change_to != []:  # 要改單位的話
            if get_unit:  # 取得單位
                pq = self.aspen.Tree.FindNode(path).AttributeValue(2)
                return self.master.Unit(item=[pq, unit_change_to], table=True)
            else:  # 取得數值
                return self.master.UnitChange(self.aspen.Tree.FindNode(path), unit_change_to)

    def QC(self,bname, get_unit=False, unit_change_to=[]):
        """Get the condenser duty of specified column.
                If it is not condenser, the return value is 'None'.
                bname: Block name.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(bname) != str:
            raise TypeError("bname must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(unit_change_to) != list and type(unit_change_to) != int:
            raise TypeError("unit_change must be a 'Integer'!!!")

        ## 把bname轉換成大寫，因為Aspen裡面的名稱都大寫
        bname = bname.upper()

        ## 檢查輸入的單元名稱是否在檔案當中，如無回傳錯誤
        if bname not in self.master.BlocksList():
            raise UDE.AspenPlus_BlockTypeError("Cannot Find " + bname
                                               + " in the AspenFile. "
                                               + "Please Check the name you type!!")

        ## 檢查指定蒸餾塔有沒有condenser
        path = "\Data\Blocks" + "\\" + bname + "\Input\CONDENSER"
        if self.aspen.Tree.FindNode(path).Value == "NONE":
            return

        path = "\Data\Blocks" + "\\" + bname + "\Output\COND_DUTY"

        ## 看看有沒有要改單位
        if unit_change_to == []:  # 沒有要改單位
            ## 是要取得數值還是單位
            if get_unit:  # 取得單位
                return self.master.UnitFind(self.aspen.Tree.FindNode(path), table=True)
            else:  # 取得數值
                return self.aspen.Tree.FindNode(path).Value
        elif unit_change_to != []:  # 要改單位的話
            if get_unit:  # 取得單位
                pq = self.aspen.Tree.FindNode(path).AttributeValue(2)
                return self.master.Unit(item=[pq, unit_change_to], table=True)
            else:  # 取得數值
                return self.master.UnitChange(self.aspen.Tree.FindNode(path), unit_change_to)

if __name__ == "__main__":
    import AspenPlus

    path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
    Aspen = AspenPlus.AP(path)

    print(Aspen.Distillation.NStage('c1'))
    Aspen.Distillation.NStage('c1',40)
    print(Aspen.Distillation.NStage('c1'))

    Aspen.Close()