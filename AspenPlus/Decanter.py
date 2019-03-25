# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from AspenPlus import UserDifineException as UDE
from AspenPlus.Basic import check_name


class Decanter:
    def __init__(self, master):
        # 應該是不用辨認輸入的master是否為帶有路徑的AspenPlus類別
        # ，因為在__init__.py裡的AP應該就會檢查過了。
        self.master = master
        self.aspen = master.aspen

    @check_name(Type='block')
    def getVolume(self, bname, rtime=40, LF=1/2, get_unit=False):
        """Get the volume of decanter depends on the volume flowrate of inlet stream.
        The calculation condition is based on residual time (rtime) of decanter and liquid level fraction (LF)
        in the tank.

        :param bname: Block name.
        :param rtime: Residual time of decanter in minute. The default value is 40 min.
        :param LF: Liquid level fraction in the decanter. The default value is 1/2.
        :param get_unit: "True" to get the unit. "False" is a default value.
        :return: float. a calculated value.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(rtime) != int and type(rtime) != float:
            raise TypeError("rtime must be a Number!!!")
        if type(LF) != int and type(LF) != float:
            raise TypeError("LF must be a Number!!!")

        ## rtime 不能是負數
        if rtime < 0:
            raise ValueError("rtime should not be a negative number!!")
        ## LF 不能是負數
        if LF < 0:
            raise ValueError("LF should not be a negative number!!")

        ## 檢查bname是否為Decanter
        if self.master.BlockType(bname) != 'Decanter':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a Decanter,'
                                               + 'please check the name you type!!')

        ## 找出Decanter進料物流名稱
        dec_fstream = []
        for e in self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Connections").Elements:
            streamtype = self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Connections").Elements(e.Name).Value
            if streamtype == "F(IN)":
                dec_fstream.append(e.Name)

        ## 檢查Decanter所有進料物流都沒有氣體以避免體積計算誤差
        for fstream in dec_fstream:
            if self.master.Stream.getVaporFrac(fstream) != 0:
                raise UDE.AspenPlus_BlockError(f"The feed stream of decanter '{fstream}' " +
                                               "contains gas. The volume-calculation may " +
                                               " have a great deviation !!!")

        if get_unit:  # 取得單位
            return "cum"
        else:  # 取得數值
            v = 0
            for fstream in dec_fstream:
                v += self.master.Stream.getVolumeFlow(fstream, unit_change_to=20)
            return v*rtime/LF

    @check_name(Type='block')
    def getDiameter(self, bname, get_unit=False):
        """Get the diameter of decanter depends on the volume of decanter.

        :param bname: Block name.
        :param get_unit: "True" to get the unit. "False" is a default value.
        :return: float. a calculated value.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")

        ## 檢查bname是否為Decanter
        if self.master.BlockType(bname) != 'Decanter':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a Decanter,'
                                               + 'please check the name you type!!')

        v = self.getVolume(bname)

        if get_unit:  # 取得單位
            return "meter"
        else:  # 取得數值
            return (2*v/3.1415926)**(1/3)

    @check_name(Type='block')
    def getHeight(self, bname, AR=0.5, get_unit=False):
        """Get the height of decanter depends on the diameter of decanter.

        :param bname: Block name.
        :param AR: aspect ratio which is the ratio of diameter to height. The default value is 0.5.
        :param get_unit: "True" to get the unit. "False" is a default value.
        :return: float. a calculated value.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(AR) != int and type(AR) != float:
            raise TypeError("AR must be a Number!!!")

        ## AR 不能是負數
        if AR < 0:
            raise ValueError("AR should not be a negative number!!")

        ## 檢查bname是否為Decanter
        if self.master.BlockType(bname) != 'Decanter':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a Decanter,'
                                               + 'please check the name you type!!')

        d = self.getDiameter(bname)

        if get_unit:  # 取得單位
            return "meter"
        else:  # 取得數值
            return d/AR
