# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from AspenPlus import UserDifineException as UDE
from AspenPlus.Basic import check_name


# TODO: 把算設備的成本公式參考文獻附在類別當中
class Distillation:
    def __init__(self, master):
        self.master = master
        self.aspen = master.aspen

    @check_name(Type='block')
    def getNStage(self, bname):
        """Get the number of stage for the specified RadFrac block.
                bname: Block name.
        """
        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        path = "\Data\Blocks" + "\\" + bname + r"\Input\NSTAGE"
        return self.aspen.Tree.FindNode(path).Value

    @check_name(Type='block')
    def setNStage(self, bname, set_value):
        """Get the number of stage for the specified RadFrac block.
                bname: Block name.
        """
        ## 檢查輸入的資料型態正確與否
        if type(set_value) != int:
            raise TypeError("set_value must be a 'Integer'!!!")
        ## 檢查set_value 是否為正整數
        if set_value < 0:
            raise ValueError("set_value must be a 'Positive' number!!!")

        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        path = "\Data\Blocks" + "\\" + bname + r"\Input\NSTAGE"
        self.aspen.Tree.FindNode(path).Value = set_value
        return

    @check_name(Type='block')
    def getNF(self, bname, *, sname=None):
        """Get the number of  feed stage for the specified RadFrac block and feed stream or
        Get the all feed stream for the specified RadFrac block in a list-type.

        :param bname: Block name.
        :param sname: Feed stream name.
        :return: if sname is None, return a feed stream list for specified block.
        if sname is specified, return the NF of specified block and feed stream.
        """
        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        ## 對sname進行檢查並處理
        if sname is None:
            pass
        elif type(sname) is str:
            ## 把sname轉換成大寫，因為Aspen裡面的名稱都大寫
            sname = sname.upper()

            ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤
            if sname not in self.master.StreamsList():
                raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                    + " in the AspenFile. "
                                                    + "Please Check the name you type!!")
        else:
            raise TypeError("sname must be a 'String'!!!")

        ## 指定塔的進料物流 物件
        obj = self.aspen.Tree.Data.Blocks.Elements(bname).Input.FEED_STAGE

        ## 列出指定塔的進料物流有哪些
        nlist = []
        for e in obj.Elements:
            nlist.append(e.Name)

        if sname is None:           # 沒輸入sname就回傳進料物流列表
            return nlist
        elif sname is not None:     # 有輸入sname且為特定塔的進料物流的話，輸出進料板
            if sname not in nlist:
                raise UDE.AspenPlus_StreamTypeError(sname + " is not a feed stream"
                                                + " for " + bname + ". "
                                                + "Please Check the name you type!!")
            return obj.Elements(sname).Value

    @check_name(Type='block')
    def setNF(self, bname, sname, set_value):
        """Set the number of  feed stage for the specified RadFrac block and feed stream.

        :param bname: Block name.
        :param sname: Feed stream name.
        :param set_value: feed stage you want to specify.
        :return: None
        """
        ## 檢查輸入的資料型態正確與否
        if type(set_value) != int:
            raise TypeError("set_value must be a 'Integer'!!!")
        ## 檢查set_value 是否為正整數
        if set_value < 0:
            raise ValueError("set_value must be a 'Positive' number!!!")

        ## 對sname進行檢查並處理
        if sname is None:
            pass
        elif type(sname) is str:
            ## 把sname轉換成大寫，因為Aspen裡面的名稱都大寫
            sname = sname.upper()

            ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤
            if sname not in self.master.StreamsList():
                raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                    + " in the AspenFile. "
                                                    + "Please Check the name you type!!")
        else:
            raise TypeError("sname must be a 'String'!!!")

        ## 指定塔的進料物流 物件
        obj = self.aspen.Tree.Data.Blocks.Elements(bname).Input.FEED_STAGE

        ## 列出指定塔的進料物流有哪些
        nlist = []
        for e in obj.Elements:
            nlist.append(e.Name)

        # 有輸入sname且為特定塔的進料物流的話，輸出進料板
        if sname not in nlist:
            raise UDE.AspenPlus_StreamTypeError(sname + " is not a feed stream"
                                                + " for " + bname + ". "
                                                + "Please Check the name you type!!")

        obj.Elements(sname).Value = set_value   # 輸入超過總板數會報有用的錯誤

    @check_name(Type='block')
    def getDiameter(self, bname, get_unit=False, unit_change_to=None):
        """Get the Column's diameter. Before using this function. you have to turn on the
                'Sizaing' or 'Rating' function in AspenPlus.
                bname: Block name.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit. If you don't want to change
                the unit, unit_change_to should be 'None'(Default value is this).
        """
        ## 此功能只能取sizing的結果不是取rating的結果
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if unit_change_to is not None and type(unit_change_to) != int:
            raise TypeError("unit_change_to must be a 'Integer' or 'None'!!!")

        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        ## 檢查是否有開啟Sizing功能
        if self.aspen.Tree.FindNode(
                "\Data\Blocks" + "\\" + bname + "\Subobjects\Column Internals").AttributeValue(38) == 0:  # 用是否有子代判斷
            raise UDE.AspenPlus_SizingError("'Sizing' function dosen't open!!!")

        ## 確認是否為 Apwn36.0(V10)
        if self.aspen.Name.find('36.0') != -1:  # 第十版的直徑路徑
            path = "\Data\Blocks" + "\\" + bname + "\Subobjects\Column Internals\INT-1\Subobjects\Sections\CS-1\Input\CA_DIAM\INT-1\CS-1"
        else:  # V8.8以前的的直徑路徑
            path = "\Data\Blocks" + "\\" + bname + "\Subobjects\Tray Sizing\\1\Output\DIAM4\\1"

        ## 看看有沒有要改單位
        if unit_change_to is None:  # 沒有要改單位
            ## 是要取得數值還是單位
            if get_unit:  # 取得單位
                return self.master.UnitFind(self.aspen.Tree.FindNode(path), table=True)
            else:  # 取得數值
                return self.aspen.Tree.FindNode(path).Value
        elif unit_change_to is not None:  # 要改單位的話
            if get_unit:  # 取得單位
                pq = self.aspen.Tree.FindNode(path).AttributeValue(2)
                return self.master.Unit(item=[pq, unit_change_to], table=True)
            else:  # 取得數值
                return self.master.UnitChange(self.aspen.Tree.FindNode(path), unit_change_to)

    @check_name(Type='block')
    def getHeight(self, bname, get_unit=False):
        """Get the Column's height. it is a  calculated value.
                Total number of trays(NT) with 2-ft spacing plus 20% extra length.
                It means  H[ft] = 2.4×(NT-1) which is equal to H[m] = 0.73152×(NT-1).
                Reference: Luyben, W. L.
                                , Comparison of extractive distillation and pressure-swing distillation for acetone/chloroform separation
                                . Comput Chem Eng 2013, 50, 1-7.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")

        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        ## 取得指定蒸餾塔的總板數
        n = self.getNStage(bname)

        ## 是要取得數值還是單位
        if get_unit:  # 取得單位
            return "meter"
        else:  # 取得數值
            return 0.73152 * (n - 1)

    @check_name(Type='block')
    def getQR(self, bname, get_unit=False, unit_change_to=None):
        """Get the reboiler duty of specified column.
                If it is not reboiler, the return value is 'None'.
                bname: Block name.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit. If you don't want to change
                the unit, unit_change_to should be 'None'(Default value is this).
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if unit_change_to is not None and type(unit_change_to) != int:
            raise TypeError("unit_change_to must be a 'Integer' or 'None'!!!")

        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        ## 檢查指定蒸餾塔有沒有reboiler
        path = "\Data\Blocks" + "\\" + bname + "\Input\REBOILER"
        if self.aspen.Tree.FindNode(path).Value == "NONE":
            return

        path = "\Data\Blocks" + "\\" + bname + "\Output\REB_DUTY"

        ## 看看有沒有要改單位
        if unit_change_to is None:  # 沒有要改單位
            ## 是要取得數值還是單位
            if get_unit:  # 取得單位
                return self.master.UnitFind(self.aspen.Tree.FindNode(path), table=True)
            else:  # 取得數值
                return self.aspen.Tree.FindNode(path).Value
        elif unit_change_to is not None:  # 要改單位的話
            if get_unit:  # 取得單位
                pq = self.aspen.Tree.FindNode(path).AttributeValue(2)
                return self.master.Unit(item=[pq, unit_change_to], table=True)
            else:  # 取得數值
                return self.master.UnitChange(self.aspen.Tree.FindNode(path), unit_change_to)

    @check_name(Type='block')
    def getReboilerArea(self, bname, get_unit=False, Ur=0.568):
        """Get the reboiler area of specified column.
                If it is not reboiler, the return value is 'None'.
                bname: Block name.
                get_unit: "True" to get the unit. "False" is a default value.
                Ur: Heat transfer coefficient of reboiler [kW/K-sqrm]. The default value is 0.568.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(Ur) != int and type(Ur) != float:
            raise TypeError("unit must be a 'Number'!!!")

        ## Ur不應該小於等於0，那...那是什麼設備??
        if Ur <= 0:
            raise ValueError("Ur shouldn't be equal to  or smaller than 0. " +
                             "Please Check the Value you Type!!!")

        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        ## 檢查指定蒸餾塔有沒有reboiler
        path = "\Data\Blocks" + "\\" + bname + "\Input\REBOILER"
        if self.aspen.Tree.FindNode(path).Value == "NONE":
            return

        bottom_name = None
        ## 找出再沸器的出口物流名稱後取得其溫度
        for e in self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements:
            streamtype = self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements(e.Name).Value
            if streamtype == "B(OUT)":
                bottom_name = e.Name
        Temp = self.master.Stream.getTemperature(bottom_name, unit_change_to=4)

        utility = self.master.Cost.SteamType(bname)
        DeltaT = self.master.Cost.Steam[utility]['Temperature']['Value'] - Temp
        Qr = self.getQR(bname)

        ## 溫差不該小於等於0，那應該就不是reboiler了
        if DeltaT <= 0:
            raise ValueError("DeltaT shouldn't be equal to  or smaller than 0. " +
                             "Please connect to the programmer!!!")

        ## 是要取得數值還是單位
        if get_unit:  # 取得單位
            return "sqrm"
        else:  # 取得數值
            return Qr / Ur / DeltaT

    @check_name(Type='block')
    def getQC(self, bname, get_unit=False, unit_change_to=None):
        """Get the condenser duty of specified column.
                If it is not condenser, the return value is 'None'.
                bname: Block name.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit. If you don't want to change
                the unit, unit_change_to should be 'None'(Default value is this).
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if unit_change_to is not None and type(unit_change_to) != int:
            raise TypeError("unit_change_to must be a 'Integer' or 'None'!!!")

        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        ## 檢查指定蒸餾塔有沒有condenser
        path = "\Data\Blocks" + "\\" + bname + "\Input\CONDENSER"
        if self.aspen.Tree.FindNode(path).Value == "NONE":
            return

        path = "\Data\Blocks" + "\\" + bname + "\Output\COND_DUTY"

        ## 看看有沒有要改單位
        if unit_change_to is None:  # 沒有要改單位
            ## 是要取得數值還是單位
            if get_unit:  # 取得單位
                return self.master.UnitFind(self.aspen.Tree.FindNode(path), table=True)
            else:  # 取得數值
                return self.aspen.Tree.FindNode(path).Value
        elif unit_change_to is not None:  # 要改單位的話
            if get_unit:  # 取得單位
                pq = self.aspen.Tree.FindNode(path).AttributeValue(2)
                return self.master.Unit(item=[pq, unit_change_to], table=True)
            else:  # 取得數值
                return self.master.UnitChange(self.aspen.Tree.FindNode(path), unit_change_to)

    @check_name(Type='block')
    def getCondenserArea(self, bname, get_unit=False, Uc=0.852):
        """Get the condenser area of specified column.
                If it is not condenser, the return value is 'None'.
                bname: Block name.
                get_unit: "True" to get the unit. "False" is a default value.
                Ur: Heat transfer coefficient of reboiler [kW/K-sqrm]. The default value is 0.852.
        """
        # TODO: 不知道需不需要考慮LMTD，需要的話在增加判斷式

        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(Uc) != int and type(Uc) != float:
            raise TypeError("unit must be a 'Number'!!!")

        ## Ur不應該小於等於0，那...那是什麼設備??
        if Uc <= 0:
            raise ValueError("Uc shouldn't be equal to  or smaller than 0. " +
                             "Please Check the Value you Type!!!")

        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        ## 檢查指定蒸餾塔有沒有condenser
        path = "\Data\Blocks" + "\\" + bname + "\Input\CONDENSER"
        if self.aspen.Tree.FindNode(path).Value == "NONE":
            return

        bottom_name = None
        ## 找出冷凝器的出口物流名稱後取得其溫度
        for e in self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements:
            streamtype = self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements(e.Name).Value
            if streamtype == "LD(OUT)":
                bottom_name = e.Name
        Temp = self.master.Stream.getTemperature(bottom_name, unit_change_to=1)

        utility = self.master.Cost.WaterType(bname)
        DeltaT = Temp - self.master.Cost.Water[utility]['Temperature']['Value']
        Qr = -self.getQC(bname)

        ## 溫差不該小於等於0，那應該就不是condenser了
        if DeltaT <= 0:
            raise ValueError("DeltaT shouldn't be equal to  or smaller than 0. " +
                             "Please connect to the programmer!!!")

        ## 是要取得數值還是單位
        if get_unit:  # 取得單位
            return "sqrm"
        else:  # 取得數值
            return Qr / Uc / DeltaT

    @check_name(Type='block')
    def getRefluxRatio(self, bname) -> float:
        """Get the reflux ratio of specified column.

        :param bname: Block name.
        :return: float.
        """
        ## 檢查bname是否為RadFrac
        if self.master.BlockType(bname) != 'RadFrac':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac,'
                                               + 'please check the name you type!!')

        path = "\Data\Blocks" + "\\" + bname + r"\Output\MOLE_RR"
        return self.aspen.Tree.FindNode(path).Value


if __name__ == "__main__":
    import AspenPlus

    path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
    Aspen = AspenPlus.AP(path)

    print(Aspen.Distillation.getNStage('c1'))
    Aspen.Distillation.setNStage('c1', 40)
    print(Aspen.Distillation.getNStage('c1'))

    Aspen.Close()
