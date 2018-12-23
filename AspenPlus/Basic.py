# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from AspenPlus import UserDifineException as UDE

# 最基本的Aspen類別功能，首次執行此封包要先設定這個類別。
# 裡面包含一些基本功能，像是列出檔案所含的所有單元、物流、化合物...等等
class AP:
    import win32com.client as win32
    aspen = win32.Dispatch('Apwn.Document')
    def __init__(self, path):
        import os
        global a  ## 錯誤測試用變數，程式完成後最好刪除

        ## 檢查檔案是否存在
        if not os.path.isfile(path):
            raise UDE.FileNotExist(
                "File cannot find at designated dictionary!!" +
                " Please check the dic you  input.")

        self.aspen.InitFromArchive(path)
        # self.Stream = Stream.Stream(AP)
        a = self.aspen  ## 錯誤測試用變數，程式完成後最好刪除

        '''
        Apwn36.0 == AspenPlus V10.0
        '''

    def Error(self):
        """Determine the file has error or not.
        If yes return 'True', or return 'False'.
        """
        ErrorPath = 'Data/Results Summary/Run-Status/Output/PER_ERROR/1'
        if self.aspen.Tree.FindNode(ErrorPath) == None:
            return False
        else:
            return True

        # TODO: 只能查看Error值是否為空，為空其實不代表一定error
        # 也有可能"run not yet", "input not complete"`,看看是
        # 否有其他寫法

    def Show(self, log):
        """Show Aspen GUI or not.
        log: a Boolean value. True for Show the GUI, False for close the GUI.
        """
        ## 檢查log是否為布林值
        if type(log) != bool:
            raise TypeError("table must be 'Boolen' value.")

        self.aspen.Visible = log

    def Close(self):
        """Close AspenPlus COM object.
        After execute the AspenPlus, the function must be call.
        """
        self.aspen.Close()

    def Unit(self, item=[], table=False):
        """Show the Unit Table or specified category or specified unit in AspenPlus.
        item: if [], list the supported Unit category in AspenPlus.
                if [integer], list the supported Unit in specified Unit category in AspenPlus.
                if [integer, integer], show the Unit for specified parameters.
        table: a boolen value. default is False for print the result on the screen. If table=True,
                return result in  dictionary type.
        """
        # TODO: 檢查輸入引數是否在範圍內
    ## 輸入變數檢查
        ## 檢查item是否為list格式
        if type(item) != list:
            raise TypeError("item has to be a 'Blank List' or "
                            + "'List' with 1 integer parameter or "
                            + "'List' with 2 integer parameters!!")
        ## 檢查table是否為布林值
        if type(table)!= bool:
            raise TypeError("table must be 'Boolen' value.")

        ## 列出整數參數對應的單位類別
        if item == []:
            UT = {}
            for index, e in enumerate(self.aspen.Tree.Elements("Unit Table").Elements, start=1):
                if table:
                    UT[index] = e.Name
                elif not table:
                    print("{0:3d}{1:>15s}".format(index, e.Name))
        ## 列出選定單位類別的所有支援單位
        elif (type(item[0]) is int) and (len(item) == 1):
            UT = {}
            ename = self.aspen.Tree.Elements("Unit Table").Elements[item[0]-1].Name
            for index, e in enumerate(self.aspen.Tree.Elements("Unit Table").Elements(ename).Elements, start=1):
                if table:
                    UT[index] = e.Name
                elif not table:
                    print("{0:3d}{1:>15s}".format(index, e.Name))
        ## 顯示兩個整數參數所代表的單位
        elif (type(item[0]) is int) and (type(item[1]) is int) and (len(item) == 2):
            ename = self.aspen.Tree.Elements("Unit Table").Elements[item[0]-1].Elements[item[1]-1].Name
            if table:
                UT = ename
            elif not table:
                print(ename)
        else:
            raise TypeError("item has to be a 'Blank List' or "
                            + "'List' with 1 integer parameter or "
                            + "'List' with 2 integer parameters!!")

        ## 如果table==True，就回傳一個字典，不然就印在畫面而已
        if table:
            return UT
        elif not table:
            return

    def UnitFind(self, obj, table=False):
        """Get the unit of physics property in AspenFile for the current unit setting.
        obj: an Aspen COMObject for the physics properties.
        table: a boolen value. default is False for print the result on the screen. If table=True,
                return result in  string.
        """
        ## 檢查table是否為布林值
        if type(table) != bool:
            raise TypeError("table must be 'Boolen' value.")

        pq = obj.AttributeValue(2)
        um = obj.AttributeValue(3)
        return self.Unit([pq,um], table=table)

        # TODO: 找看看能不能判斷obj是否為合法輸入

    def UnitChange(self, obj, unit_index):
        """Change the Unit in AspenFile for the physics properties.
        obj: an Aspen COMObject for the physics property.
        unit_index: index for the specified physics property in AspenPlus.
                        It can be  search by the 'Unit()'  for what index for the desired unit.
        """
        # TODO: 檢查引數是否在範圍內

        ## 將數值兩個單位引數分別記錄起來
        pq = obj.AttributeValue(2)
        um = unit_index

        ## 確認輸入引數是否為整數。確認obj輸入正確
        if type(um) != int:
            raise TypeError("unit_index must be integer")
        if type(pq) != int:
            raise IOError("obj doesn't has the unit. "
                          + "Please Check the input of obj.")

        return obj.ValueForUnit(pq, um)

    def ListBlocks(self):
        """Show all of the blocks in AspenFile.
        """
        print("{0[0]:11s}{0[1]:11s}".format(["Block_Name","Block_Type"]))
        print("======================")
        for e in self.aspen.Tree.Data.Blocks.Elements:
            ## 可以讀取所選物件的"Type"
            blocktype = self.aspen.Tree.Data.Blocks.Elements(e.Name).AttributeValue(6)
            print("{0:11s}{1:11s}".format(e.Name,blocktype))
        print("(These are all of the blocks.)")

    def ListStreams(self):
        """Show all of the streams in AspenFile.
        """
        print("Streams_Name")
        print("============")
        for e in self.aspen.Tree.Data.Streams.Elements:
            print(e.Name)
        print("(These are all of the streams.)")

    def ListComponents(self):
        """Show all of the components in AspenFile.
        """
        print("Components_Name")
        print("===============")
        for e in self.aspen.Tree.Data.Components.Elements("Comp-Lists").GLOBAL.Input.CID.Elements:
            print(e.Value)
        print("(These are all of the components.)")

    def BlocksList(self) -> list:
        """Get the block-list in AspenFile with 'List Type'.
        """
        a_list = []
        for e in self.aspen.Tree.Data.Blocks.Elements:
            a_list.append(e.Name)
        return a_list

    def StreamsList(self) -> list:
        """Get the streams-list in AspenFile with 'List Type'.
        """
        a_list = []
        for e in self.aspen.Tree.Data.Streams.Elements:
            a_list.append(e.Name)
        return a_list

    def ComponentsList(self) -> list:
        """Get the components-list in AspenFile with 'List Type'.
        """
        a_list = []
        for e in self.aspen.Tree.Data.Components.Elements("Comp-Lists").GLOBAL.Input.CID.Elements:
            a_list.append(e.Value)
        return a_list

    def Connections(self, bname, table=False):
        """Show the connected stream of the desired block.
        bname: block name in 'Str-Type'.
        table: a boolen value. default is False for print the result on the screen. If table=True,
                return result in  list type.
        """
        ## 先檢查輸入的資料型態是否正確
        if type(bname) is not str:
            raise TypeError("bname must be a 'String'!!!")
        if type(table) is not bool:
            raise TypeError("table must be a 'Boolen' value!!!")

        ## 將輸入的字串全部大寫，因為Aspen的單元名稱都是大寫
        bname = bname.upper()

        ## 檢查輸入的單元名稱是否在檔案當中，如無回傳錯誤
        if bname not in self.BlocksList():
            raise UDE.AspenPlus_BlockTypeError("Cannot Find " + bname
                                               + " in the AspenFile. "
                                               + "Please Check the name you type!!")

        ## 在屏幕上輸出指定單元所連接的物流名稱
        if not table:
            print("{0[0]:13s}{0[1]:13s}".format(["Stream_Name","Streams_Type"]))
            print("==========================")
            for e in self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements:
                streamtype = self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements(e.Name).Value
                print("{0:13s}{1:13s}".format(e.Name,streamtype))
        ## 將結果以列表輸出
        elif table:
            a_list = []
            for e in self.aspen.Tree.Data.Blocks.Elements(bname).Connections.Elements:
                a_list.append(e.Name)
            return a_list

    def BlockType(self, bname) -> str:
        """Get the block type of the bname in string.
        bname: Block name in AspenFile.
        """
        ## 先檢查輸入的資料型態是否正確
        if type(bname) is not str:
            raise TypeError("bname must be a 'String'!!!")

        ## 將輸入的字串全部大寫，因為Aspen的單元名稱都是大寫
        bname = bname.upper()

        ## 檢查輸入的單元名稱是否在檔案當中，如無回傳錯誤
        if bname not in self.BlocksList():
            raise UDE.AspenPlus_BlockTypeError("Cannot Find " + bname
                                                + " in the AspenFile. "
                                                + "Please Check the name you type!!")

        return self.aspen.Tree.Data.Blocks.Elements(bname).AttributeValue(6)
