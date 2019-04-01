# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from AspenPlus import UserDifineException as UDE
from AspenPlus.Basic import check_name


class Extractor:
    def __init__(self, master):
        # 應該是不用辨認輸入的master是否為帶有路徑的AspenPlus類別
        # ，因為在__init__.py裡的AP應該就會檢查過了。
        self.master = master
        self.aspen = master.aspen

    @check_name(Type='block')
    def getNStage(self, bname):
        """Get the number of stage for the specified Extractor block.

        :param bname: Block name.
        :return: Integer. total number stages of extractor.
        """
        ## 檢查bname是否為Extract
        if self.master.BlockType(bname) != 'Extract':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a Extract,'
                                               + 'please check the name you type!!')

        path = "\Data\Blocks" + "\\" + bname + r"\Input\NSTAGE"
        return self.aspen.Tree.FindNode(path).Value

    @check_name(Type='block')
    def setNStage(self, bname, set_value):
        """Get the number of stage for the specified Extract block.

        :param bname: Block name.
        :param set_value: an Integer which you want to change the NSTAGE of extractor to.
        :return: None
        """
        ## 檢查輸入的資料型態正確與否
        if type(set_value) != int:
            raise TypeError("set_value must be a 'Integer'!!!")
        ## 檢查set_value 是否為正整數
        if set_value < 0:
            raise ValueError("set_value must be a 'Positive' number!!!")

        ## 檢查bname是否為Extract
        if self.master.BlockType(bname) != 'Extract':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a Extract,'
                                               + 'please check the name you type!!')

        path = "\Data\Blocks" + "\\" + bname + r"\Input\NSTAGE"
        self.aspen.Tree.FindNode(path).Value = set_value
        return

    @check_name(Type='block')
    def getHeight(self, bname, get_unit=False):
        """Get the Extractor's height. it is a  calculated value.
                Total number of trays(NT) with 4ft HETP plus additional 3ft at the top and 3ft at the bottom.
                It means  H[ft] = 4×NT+3×2 which is equal to H[m] = 0.3048×(4×NT+3×2)
                Reference: Seider, W. D.; Seader, J. D.; Lewin, D. R.; Widagdo, S.
                                , Product and Process Design Principles Synthesis, Analysis, and Evaluation
                                . Wiley: Hoboken, NJ: 2010.

        :param bname: Block name
        :param get_unit: True" to get the unit. "False" is a default value.
        :return: float. a calculated value.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")

        ## 檢查bname是否為Extract
        if self.master.BlockType(bname) != 'Extract':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a Extract,'
                                               + 'please check the name you type!!')

        n = self.getNStage(bname)
        if get_unit:
            return "meter"
        else:
            return 0.3048*(4*n+3+3)

    @check_name(Type='block')
    def getDiameter(self, bname, get_unit=False):
        """Get the Extractor's diameter. it is a  calculated value.
        Volumetric flowrate of inlet liquid(Q) = simulation result [ft3/hr].
        D[ft] = 4Q/120/0.6/pi)0.5 With Maximum total liquid throughput=120 ft3 /hr-ft2 and safety factor f=0.6.
        The final result will be changed in 'meter'.

        :param bname: Block name.
        :param get_unit: "True" to get the unit. "False" is a default value.
        :return: float. a calculated value.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")

        ## 檢查bname是否為Extract
        if self.master.BlockType(bname) != 'Extract':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a Extract,'
                                               + 'please check the name you type!!')

        ## 確認萃取塔只有兩個進料物流
        index = 0
        sname_arr = []
        for e in self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Input").Elements("FEED_STAGE").Elements:
            sname_arr.append(e.Name)
            index += 1
        if index > 2:
            raise UDE.AspenPlus_BlockTypeError("You have more than 2 Feed streams! for "
                                               "Extractor. The function cannot work!")
        sname1 = sname_arr[0]
        sname2 = sname_arr[1]

        ## 確認萃取塔進料物流都沒有氣體(影響體積計算)
        if self.master.Stream.getVaporFrac(sname1) == 0 and self.master.Stream.getVaporFrac(sname2) == 0 :
            if get_unit:
                return "meter"
            else:
                ## 確保單位為cuft/h
                vtotal = self.master.Stream.getVolumeFlow(sname1, unit_change_to=2) + \
                         self.master.Stream.getVolumeFlow(sname2, unit_change_to=2)
                return 0.3048*(vtotal*4/120/0.6/3.1415926)**0.5
        else:
            raise UDE.AspenPlus_BlockTypeError("The feed streams of extractor have vapor!!")
