# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from AspenPlus import UserDifineException as UDE
from AspenPlus.Basic import check_name

class Stream:
    def __init__(self, master):
        self.master = master
        self.aspen = master.aspen

    @check_name(Type='stream')
    def getMoleFlow(self, sname, component='', get_unit=False, unit_change_to=None) -> float:
        """Get the  Moleflow of specified stream for Total or component .
                sname: Stream name
                component: If it is no given. the fct will give the total moleflow.
                                If you give the component name, the fct will give the component flowrate.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit. If you don't want to change
                the unit, unit_change_to should be 'None'(Default value is this).
        """
        ## 先檢查輸入的資料型態正確與否
        if type(component) != str:
            raise TypeError("component must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if unit_change_to is not None and type(unit_change_to) != int:
            raise TypeError("unit_change_to must be a 'Integer' or 'None'!!!")

        ## 把component轉換成大寫，因為Aspen裡面的名稱都大寫
        component = component.upper()

        ## 辨認是要輸出總流量還是化合物流量
        if component != '':
            ## 辨認化合物有沒有在檔案當中，如無回傳錯誤
            if component not in self.master.ComponentsList():
                raise UDE.AspenPlus_ComponentTypeError("Cannot Find " + component
                                                       + " in the AspenFile. "
                                                       + "Please Check the name you type!!")

            path = '\Data\Streams' + '\\' + sname + '\Output\MOLEFLOW\MIXED' + '\\' + component
        elif component == '':
            path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\MOLEFLMX\MIXED"

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

    @check_name(Type='stream')
    def getMoleFrac(self, sname, component) -> float:
        """Get the  Mole Fraction of specified component of specified stream.
                sname: Stream name
                component: component you want to know.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(component) != str:
            raise TypeError("component must be a 'String'!!!")

        ## 把component轉換成大寫，因為Aspen裡面的名稱都大寫
        component = component.upper()

        ## 檢查輸入的化合物名稱是否在檔案當中，如無回傳錯誤
        if component not in self.master.ComponentsList():
            raise UDE.AspenPlus_ComponentTypeError("Cannot Find " + component
                                                   + ' in the AspenFile. '
                                                   + "Please Check the name you type!!")

        # mole fraction這邊用算的
        mt = self.getMoleFlow(sname)
        m = self.getMoleFlow(sname, component=component)
        return m/mt

    @check_name(Type='stream')
    def getMassFlow(self, sname, component='', get_unit=False, unit_change_to=None) -> float:
        """Get the  Massflow of specified stream for Total or component .
                sname: Stream name
                component: If it is no given. the fct will give the total massflow.
                                If you give the component name, the fct will give the component flowrate.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit. If you don't want to change
                the unit, unit_change_to should be 'None'(Default value is this).
        """
        ## 先檢查輸入的資料型態正確與否
        if type(component) != str:
            raise TypeError("component must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if unit_change_to is not None and type(unit_change_to) != int:
            raise TypeError("unit_change_to must be a 'Integer' or 'None'!!!")

        ## 把component轉換成大寫，因為Aspen裡面的名稱都大寫
        component = component.upper()

        ## 辨認是要輸出總流量還是化合物流量
        if component != '':
            ## 辨認化合物有沒有在檔案當中，如無回傳錯誤
            if component not in self.master.ComponentsList():
                raise UDE.AspenPlus_ComponentTypeError("Cannot Find " + component
                                                       + " in the AspenFile. "
                                                       + "Please Check the name you type!!")

            path = '\Data\Streams' + '\\' + sname + '\Output\MASSFLOW3' + '\\' + component
        elif component == '':
            path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\MASSFLMX\MIXED"

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

    @check_name(Type='stream')
    def getMassFrac(self, sname, component) -> float:
        """Get the  Mass Fraction of specified component of specified stream.
                sname: Stream name
                component: component you want to know.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(component) != str:
            raise TypeError("component must be a 'String'!!!")

        ## 把component轉換成大寫，因為Aspen裡面的名稱都大寫
        component = component.upper()

        ## 檢查輸入的化合物名稱是否在檔案當中，如無回傳錯誤
        if component not in self.master.ComponentsList():
            raise UDE.AspenPlus_ComponentTypeError("Cannot Find " + component
                                                   + ' in the AspenFile. '
                                                   + "Please Check the name you type!!")

        # mass fraction這邊用算的
        mt = self.getMassFlow(sname)
        m = self.getMassFlow(sname, component=component)
        return m/mt

    @check_name(Type='stream')
    def getTemperature(self, sname, get_unit=False, unit_change_to=None) -> float:
        """Get the Temperature of specified stream.
                sname: Stream name in AspenPlus.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit. If you don't want to change
                the unit, unit_change_to should be 'None'(Default value is this).
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if unit_change_to is not None and type(unit_change_to) != int:
            raise TypeError("unit_change_to must be a 'Integer' or 'None'!!!")

        path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\TEMP\MIXED"

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

    @check_name(Type='stream')
    def getPressure(self, sname, get_unit=False, unit_change_to=None) -> float:
        """Get the getPressure of specified stream.
                sname: Stream name in AspenPlus.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit. If you don't want to change
                the unit, unit_change_to should be 'None'(Default value is this).
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if unit_change_to is not None and type(unit_change_to) != int:
            raise TypeError("unit_change_to must be a 'Integer' or 'None'!!!")

        path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\PRES\MIXED"

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

    @check_name(Type='stream')
    def getVaporFrac(self, sname) -> float:
        """Get the Vapor fraction of specified stream.
                sname: Stream name in AspenPlus.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\VFRAC\MIXED"
        return self.aspen.Tree.FindNode(path).Value

    @check_name(Type='stream')
    def getVolumeFlow(self, sname, get_unit=False, unit_change_to=None) -> float:
        """Get the volumetric flowrate of specified stream.
                sname: Stream name in AspenPlus.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit. If you don't want to change
                the unit, unit_change_to should be 'None'(Default value is this).
        """
        ## 先檢查輸入的資料型態正確與否
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if unit_change_to is not None and type(unit_change_to) != int:
            raise TypeError("unit_change_to must be a 'Integer' or 'None'!!!")

        path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\VOLFLMX\MIXED"

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

if __name__ == "__main__":
    import AspenPlus

    path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
    Aspen = AspenPlus.AP(path)

    # print(Aspen.Stream.getMoleFlow('b1'))
    # print(Aspen.Stream.getMoleFlow('b1', component='ethanol', unit_change_to=3, get_unit=True))
    # print(__name__)

    print(Aspen.Stream.getVaporFrac('b1'))

    Aspen.Close()