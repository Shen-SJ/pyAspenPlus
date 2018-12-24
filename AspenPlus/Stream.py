# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from AspenPlus import UserDifineException as UDE

# TODO: 我總覺得這堆重複性很高的程式碼可以用decorator，
#  不過我還不會，正在研究當中
class Stream:
    def __init__(self, master):
        # 應該是不用辨認輸入的master是否為帶有路徑的AspenPlus類別
        # ，因為在__init__.py裡的AP應該就會檢查過了。
        self.master = master
        self.aspen = master.aspen

    def MoleFlow(self, sname, component='', get_unit=False, unit_change_to=[]) -> float:
        """Get the  Moleflow of specified stream for Total or component .
                sname: Stream name
                component: If it is no given. the fct will give the total moleflow.
                                If you give the component name, the fct will give the component flowrate.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(sname) != str:
            raise TypeError("sname must be a 'String'!!!")
        if type(component) != str:
            raise TypeError("component must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(unit_change_to) != list and type(unit_change_to) != int:
            raise TypeError("unit_change must be a 'Integer'!!!")

        ## 把sname和component轉換成大寫，因為Aspen裡面的名稱都大寫
        sname = sname.upper()
        component = component.upper()

        ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤 (化合物辨認在後面
        if sname not in self.master.StreamsList():
            raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")

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

    def MoleFrac(self, sname, component) -> float:
        """Get the  Mole Fraction of specified component of specified stream.
                sname: Stream name
                component: component you want to know.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(sname) != str:
            raise TypeError("sname must be a 'String'!!!")
        if type(component) != str:
            raise TypeError("component must be a 'String'!!!")

        ## 把sname和component轉換成大寫，因為Aspen裡面的名稱都大寫
        sname = sname.upper()
        component = component.upper()

        ## 檢查輸入的物流與化合物名稱是否在檔案當中，如無回傳錯誤
        if sname not in self.master.StreamsList():
            raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")
        if component not in self.master.ComponentsList():
            raise UDE.AspenPlus_ComponentTypeError("Cannot Find " + component
                                                   + ' in the AspenFile. '
                                                   + "Please Check the name you type!!")

        # mole fraction這邊用算的
        mt = self.MoleFlow(sname)
        m = self.MoleFlow(sname, component=component)
        return m/mt

    def MassFlow(self, sname, component='', get_unit=False, unit_change_to=[]) -> float:
        """Get the  Massflow of specified stream for Total or component .
                sname: Stream name
                component: If it is no given. the fct will give the total massflow.
                                If you give the component name, the fct will give the component flowrate.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(sname) != str:
            raise TypeError("sname must be a 'String'!!!")
        if type(component) != str:
            raise TypeError("component must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(unit_change_to) != list and type(unit_change_to) != int:
            raise TypeError("unit_change must be a 'Integer'!!!")

        ## 把sname和component轉換成大寫，因為Aspen裡面的名稱都大寫
        sname = sname.upper()
        component = component.upper()

        ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤 (化合物辨認在後面
        if sname not in self.master.StreamsList():
            raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")

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

    def MassFrac(self, sname, component) -> float:
        """Get the  Mass Fraction of specified component of specified stream.
                sname: Stream name
                component: component you want to know.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(sname) != str:
            raise TypeError("sname must be a 'String'!!!")
        if type(component) != str:
            raise TypeError("component must be a 'String'!!!")

        ## 把sname和component轉換成大寫，因為Aspen裡面的名稱都大寫
        sname = sname.upper()
        component = component.upper()

        ## 檢查輸入的物流與化合物名稱是否在檔案當中，如無回傳錯誤
        if sname not in self.master.StreamsList():
            raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")
        if component not in self.master.ComponentsList():
            raise UDE.AspenPlus_ComponentTypeError("Cannot Find " + component
                                                   + ' in the AspenFile. '
                                                   + "Please Check the name you type!!")

        # mass fraction這邊用算的
        mt = self.MassFlow(sname)
        m = self.MassFlow(sname, component=component)
        return m/mt

    def Temperature(self, sname, get_unit=False, unit_change_to=[]) -> float:
        """Get the Temperature of specified stream.
                sname: Stream name in AspenPlus.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(sname) != str:
            raise TypeError("sname must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(unit_change_to) != list and type(unit_change_to) != int:
            raise TypeError("unit_change must be a 'Integer'!!!")

        ## 把sname轉換成大寫，因為Aspen裡面的名稱都大寫
        sname = sname.upper()

        ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤
        if sname not in self.master.StreamsList():
            raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")

        path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\TEMP\MIXED"

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

    def Pressure(self, sname, get_unit=False, unit_change_to=[]) -> float:
        """Get the Pressure of specified stream.
                sname: Stream name in AspenPlus.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(sname) != str:
            raise TypeError("sname must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(unit_change_to) != list and type(unit_change_to) != int:
            raise TypeError("unit_change must be a 'Integer'!!!")

        ## 把sname轉換成大寫，因為Aspen裡面的名稱都大寫
        sname = sname.upper()

        ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤
        if sname not in self.master.StreamsList():
            raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")

        path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\PRES\MIXED"

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

    def VaporFrac(self, sname) -> float:
        """Get the Vapor fraction of specified stream.
                sname: Stream name in AspenPlus.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(sname) != str:
            raise TypeError("sname must be a 'String'!!!")

        ## 把sname轉換成大寫，因為Aspen裡面的名稱都大寫
        sname = sname.upper()

        ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤
        if sname not in self.master.StreamsList():
            raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")

        path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\VFRAC\MIXED"
        return self.aspen.Tree.FindNode(path).Value

    def VolumeFlow(self, sname, get_unit=False, unit_change_to=[]) -> float:
        """Get the volumetric flowrate of specified stream.
                sname: Stream name in AspenPlus.
                get_unit: "True" to get the unit. "False" is a default value.
                unit_change_to: unit index in AspenFile for the changing unit.
        """
        ## 先檢查輸入的資料型態正確與否
        if type(sname) != str:
            raise TypeError("sname must be a 'String'!!!")
        if type(get_unit) != bool:
            raise TypeError("unit must be a 'Boolean'!!!")
        if type(unit_change_to) != list and type(unit_change_to) != int:
            raise TypeError("unit_change must be a 'Integer'!!!")

        ## 把sname轉換成大寫，因為Aspen裡面的名稱都大寫
        sname = sname.upper()

        ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤
        if sname not in self.master.StreamsList():
            raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")

        path = "\Data\Streams" + "\\" + sname + "\Output\STR_MAIN\VOLFLMX\MIXED"

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

    print(Aspen.Stream.MoleFlow('b1'))
    print(Aspen.Stream.MoleFlow('b1', component='ethanol', unit_change_to=3, get_unit=True))
    print(__name__)

    Aspen.Close()