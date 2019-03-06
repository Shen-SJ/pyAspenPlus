# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from AspenPlus import UserDifineException as UDE
from AspenPlus.Basic import check_name


class Heater:
    def __init__(self, master):
        # 應該是不用辨認輸入的master是否為帶有路徑的AspenPlus類別
        # ，因為在__init__.py裡的AP應該就會檢查過了。
        self.master = master
        self.aspen = master.aspen

    @check_name(Type='block')
    def getQ(self, bname, get_unit=False, unit_change_to=None):
        """Get the duty of Heat exchanger.
                bname: block name.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit. If you don't want to change
                the unit, unit_change_to should be 'None'(Default value is this).
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if unit_change_to is not None and type(unit_change_to) != int:
            raise TypeError("unit_change_to must be a 'Integer' or 'None'!!!")

        ## 檢查bname是否為Heater
        if self.master.BlockType(bname) != 'Heater':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a Heater,'
                                               + 'please check the name you type!!')

        path = "\Data\Blocks" + "\\" + bname + "\Output\QNET"

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
    def getArea(self, bname, exchanger_type, get_unit=False, U=None):
        """Get the theoretical area of  'Heater'. The available exchanger types are 'Condenser', 'Heater', 'Reboiler', and
        'Cooler'.

        :param bname: block name.
        :param exchanger_type: the type for calculating cost of heater. the available value are 'CONDENSER',
        'HEATER', 'REBOILER', ane 'COOLER'.
        :param get_unit: "True" to get the unit. "False" is a default value.
        :param U: Heat transfer coefficient of exchanger [kW/K-sqrm]. The value will be change to
        match the different condition. You can  specified the value you want.
        :return:
        """
        # 把heater當mixer用還沒有解決辦法

        from math import log
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")

        ## 檢查bname是否為Heater
        if self.master.BlockType(bname) != 'Heater':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a Heater,'
                                               + 'please check the name you type!!')
        ## 檢查Uc的輸入型態是否正確，如為數字檢查數字範圍是否正確
        if (U is not None) and type(U) != int and type(U) != float:
            raise TypeError("U must be a 'Number'!!!")
        elif U is not None:
            ## Ur不應該小於等於0，那...那是什麼設備??
            if U <= 0:
                raise ValueError("U shouldn't be equal to  or smaller than 0. " +
                                 "Please Check the Value you Type!!! ")

        duty = abs(self.getQ(bname, unit_change_to=14))  # kW

        ## 檢查 exchanger_type是否為三個選項之一，並執行個別的算法，都不是則回報錯誤
        if exchanger_type == 'CONDENSER':
            ## Uc 沒有定義設定值，就用condenser的預設值
            if U is None:
                U = 0.852

            ## 找出Heater出口的物流名稱，並取得其凱式溫度與適合公共流體
            outlet_name = None
            for e in self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements:
                streamtype = self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements(e.Name).Value
                if streamtype == "P(OUT)" and self.master.BlockType(bname) == 'Heater':
                    outlet_name = e.Name
            if outlet_name is None:
                raise UDE.AspenPlus_BlockTypeError("Please Connect the Developer!!!")
            To = self.master.Stream.getTemperature(outlet_name, unit_change_to=1)
            utility = self.master.Cost.WaterType(bname)

            ## 取得 deltaT
            deltaT = To - self.master.Cost.Water[utility]['Temperature']['Value']

        elif (exchanger_type == 'HEATER') or (exchanger_type == 'REBOILER'):
            ## Uc 沒有定義設定值，就用condenser的預設值
            if U is None:
                U = 0.568

            ## 找出Heater出口的物流名稱，並取得其凱式溫度與適合公共流體
            outlet_name = None
            for e in self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements:
                streamtype = self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements(e.Name).Value
                if streamtype == "P(OUT)" and self.master.BlockType(bname) == 'Heater':
                    outlet_name = e.Name
            if outlet_name is None:
                raise UDE.AspenPlus_BlockTypeError("Please Connect the Developer!!!")
            To = self.master.Stream.getTemperature(outlet_name, unit_change_to=1)
            utility = self.master.Cost.SteamType(bname)

            ## 取得 deltaT
            deltaT = self.master.Cost.Steam[utility]['Temperature']['Value'] - To

        elif exchanger_type == 'COOLER':
            if U is None:
                U = 0.852

            ## 找出Heater出口的物流名稱，並取得其凱式溫度與適合公共流體
            outlet_name = None
            inlet_name = None
            for e in self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements:
                streamtype = self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements(e.Name).Value
                if streamtype == "P(OUT)" and self.master.BlockType(bname) == 'Heater':
                    outlet_name = e.Name
                elif streamtype == "F(IN)" and self.master.BlockType(bname) == 'Heater':
                    inlet_name = e.Name
            if (outlet_name is None) or (inlet_name is None):
                raise UDE.AspenPlus_BlockTypeError("Please Connect the Developer!!!")
            To = self.master.Stream.getTemperature(outlet_name, unit_change_to=1)
            Ti = self.master.Stream.getTemperature(inlet_name, unit_change_to=1)
            utility = self.master.Cost.WaterType(bname)
            Tu = self.master.Cost.Water[utility]['Temperature']['Value']

            ## 取得 deltaT
            deltaT = (Ti - To) / log((Ti - Tu) / (To - Tu))

        else:
            raise TypeError('exchanger_type must be a String and ' +
                            "one of them that 'CONDENSER', 'HEATER', " +
                            "'REBOILER', and 'COOLER' !!!")

        A = duty / U / deltaT
        if get_unit:
            return 'sqrm'
        else:
            return A


if __name__ == "__main__":
    import AspenPlus

    path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
    Aspen = AspenPlus.AP(path)

    print(Aspen.Heater.getQ('c4-con'))
    # print(Aspen.Heater.getArea('c4-con', exchanger_type='CONDENSER'))
    print(Aspen.Heater.getArea('c4-con', exchanger_type='COOLER'))

    Aspen.Close()
