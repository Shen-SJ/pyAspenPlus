# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from AspenPlus import UserDifineException as UDE
from AspenPlus.Basic import check_name


class Cost:
    def __init__(self, master):
        # 應該是不用辨認輸入的master是否為帶有路徑的AspenPlus類別
        # ，因為在__init__.py裡的AP應該就會檢查過了。
        self.master = master
        self.aspen = master.aspen

        ## 蒸氣與公用水的價錢與其物理性質資訊
        self.Steam = {'LP': {'Temperature': {'Value': 160, 'Unit': 'C'},
                             'Pressure': {'Value': 5, 'Unit': 'barg'},
                             'Price': {'Value': 7.78, 'Unit': 'USD/GJ'}},
                      'MP': {'Temperature': {'Value': 184, 'Unit': 'C'},
                             'Pressure': {'Value': 10, 'Unit': 'barg'},
                             'Price': {'Value': 8.22, 'Unit': 'USD/GJ'}},
                      'HP': {'Temperature': {'Value': 254, 'Unit': 'C'},
                             'Pressure': {'Value': 41, 'Unit': 'barg'},
                             'Price': {'Value': 9.88, 'Unit': 'USD/GJ'}}}

        self.Water = {'Cooling': {'Temperature': {'Value': 315, 'Unit': 'K'},
                                  'Price': {'Value': 0.354, 'Unit': 'USD/GJ'}},
                      'Chill': {'Temperature': {'Value': 278, 'Unit': 'K'},
                                'Price': {'Value': 4.43, 'Unit': 'USD/GJ'}}}

    @check_name(Type='block')
    def SteamType(self, bname, minDeltaT=20):
        """Recognize the steam type of the block. The rule to do that is based on
                the temperature difference of outlet stream temperature  and utility temperature.
                The default minimum temperature difference is 20 celsius degree.
                bname: Block name. The block type  have to be a 'RadFrac' or  'Heater' or 'Flash2'.
                minDeltaT: minimum temperature difference between utility and outlet stream of heating-unit.
                The default value is 20 C.
        """
        # 用蒸氣的加熱單元可以是:再沸器(蒸餾塔裡面)、熱交換器、閃蒸塔
        # 目前不支援HeatX
        ## 先檢查輸入的資料型態正確與否
        if type(minDeltaT) != int and type(minDeltaT) != float:
            raise TypeError("minDeltaT must be a Number!!!")

        ## minDeltaT 不能是負數
        if minDeltaT < 0:
            raise ValueError("minDeltaT should not be a negative number!!")

        ## 檢查bname是否為RadFrac或Heater或Flash2
        if self.master.BlockType(bname) != 'RadFrac' and\
                self.master.BlockType(bname) != 'Heater' and\
                self.master.BlockType(bname) != 'Flash2':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac or a Heater or a Flash2,'
                                               + 'please check the name you type!!')

        ## 檢查指定蒸餾塔有沒有reboiler
        path = "\Data\Blocks" + "\\" + bname + "\Input\REBOILER"
        if self.master.BlockType(bname) == 'RadFrac':
            if self.aspen.Tree.FindNode(path).Value == "NONE":
                raise UDE.AspenPlus_BlockTypeError("The specified column doesn't have reboiler." +
                                                   " Please check the name you type!!!")

        ## 檢查指定Heater是否為加熱器
        if (self.master.BlockType(bname) == 'Heater') and (self.master.Heater.getQ(bname) <= 0):
            raise UDE.AspenPlus_BlockTypeError("The duty of specified Heater is equal or smaller than Zero." +
                                               " It is no need to use steam !!!")

        # TODO: flash的檢查等建立flash再說

        bottom_name = None
        ## 找出加熱單元的出口物流名稱
        for e in self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Connections").Elements:
            streamtype = self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Connections").Elements(e.Name).Value
            ## 是蒸餾塔的話
            if streamtype == "B(OUT)" and self.master.BlockType(bname) == 'RadFrac':
                bottom_name = e.Name
            ## 是加熱器的話
            elif streamtype == "P(OUT)" and self.master.BlockType(bname) == 'Heater':
                bottom_name = e.Name
            ## 是閃蒸槽的話
            elif streamtype == "L(OUT)" and self.master.BlockType(bname) == 'Flash2':
                bottom_name = e.Name
        if bottom_name is None:
            raise UDE.AspenPlus_BlockTypeError("The block-type may not be supported." +
                                               " Please Connect the Developer!!!")

        ## 取得加熱單元出口物流之溫度並確保單位是攝氏溫標
        Temp = self.master.Stream.getTemperature(bottom_name, unit_change_to=4)

        if Temp + minDeltaT <= self.Steam['LP']['Temperature']['Value']:
            return 'LP'
        elif Temp + minDeltaT <= self.Steam['MP']['Temperature']['Value']:
            return 'MP'
        elif Temp + minDeltaT <= self.Steam['HP']['Temperature']['Value']:
            return 'HP'
        else:
            raise UDE.AspenPlus_SteamError("The temperature difference between " +
                                           "outlet stream and utility cannot " +
                                           "match the required minimum value." +
                                           " Please Check your design detail !!!")

    @check_name(Type='block')
    def WaterType(self, bname):
        """Recognize the water type of the block. The rule to do that is based on
                the outlet stream temperature. If the temperature of outlet stream is higher than 320K,
                Cooling water can be used. If it is lower than 320K but higher than 298K,  Chill water can be used.
                bname: Block name. The block type  have to be a 'RadFrac' or  'Heater'.
        """
        # 用水的冷卻單元可以是:冷凝器(蒸餾塔裡面)、熱交換器
        # 目前不支援HeatX

        ## 檢查bname是否為RadFrac或Heater
        if self.master.BlockType(bname) != 'RadFrac' and\
                self.master.BlockType(bname) != 'Heater':
            raise UDE.AspenPlus_BlockTypeError(bname + ' is not a RadFrac or a Heater,'
                                               + 'please check the name you type!!')

        ## 檢查指定蒸餾塔有沒有condenser
        path = "\Data\Blocks" + "\\" + bname + "\Input\CONDENSER"
        if self.master.BlockType(bname) == 'RadFrac':
            if self.aspen.Tree.FindNode(path).Value == "NONE":
                raise UDE.AspenPlus_BlockTypeError("The specified column doesn't have condenser." +
                                                   " Please check the name you type!!!")

        ## 檢查指定Heater是否為冷卻器
        if (self.master.BlockType(bname) == 'Heater') and (self.master.Heater.getQ(bname) >= 0):
            raise UDE.AspenPlus_BlockTypeError("The duty of specified Heater is equal or greater than Zero." +
                                               " It is no need to use water !!!")

        bottom_name = None
        ## 找出冷卻單元的出口物流名稱
        for e in self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Connections").Elements:
            streamtype = self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Connections").Elements(e.Name).Value
            ## 是蒸餾塔的話
            if streamtype == "LD(OUT)" and self.master.BlockType(bname) == 'RadFrac':
                bottom_name = e.Name
            ## 是加熱器的話
            elif streamtype == "P(OUT)" and self.master.BlockType(bname) == 'Heater':
                bottom_name = e.Name
        if bottom_name is None:
            raise UDE.AspenPlus_BlockTypeError("The block-type may not be supported." +
                                               " Please Connect the Developer!!!")

        ## 取得冷卻單元出口物流之溫度並確保單位是凱氏溫標
        Temp = self.master.Stream.getTemperature(bottom_name, unit_change_to=1)

        if Temp >= 320:
            return 'Cooling'
        elif Temp < 320 and Temp >= 298:
            return 'Chill'
        else:
            raise UDE.AspenPlus_WaterError("The temperature of outlet stream" +
                                           " may be too low. Please Check your " +
                                           "design detail !!!")


if __name__ == "__main__":
    pass
