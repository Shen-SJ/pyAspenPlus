# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from pyAspenPlus import UserDifineException as UDE
from functools import wraps

# 最基本的Aspen類別功能，首次執行此封包要先設定這個類別。
# 裡面包含一些基本功能，像是列出檔案所含的所有單元、物流、化合物...等等


class AP:
    def __init__(self, path, version=None):
        import os
        import win32com.client as win32
        if version is not None:
            self.aspen = win32.Dispatch(f'Apwn.Document.{version}.0')
        else:
            self.aspen = win32.Dispatch('Apwn.Document')

        ## 檢查檔案是否存在
        if not os.path.isfile(path):
            raise UDE.FileNotExist(
                "File cannot find at designated dictionary!!" +
                " Please check the dic you  input.")

        self.aspen.InitFromArchive(path)

        # Apwn36.0 == AspenPlus V10.0

    def __del__(self):
        """Close the AspenFile when AP class is destroyed."""
        try:
            self.Close()
        except:
            pass

    def FileStatus(self):
        """Determine the status of AspenFile. if the file is

        :return: if file is available, return 'Available'. if file has waring, return 'Warning'.
        if file has error, return 'Error'.
        """
        status_code = self.aspen.Tree.Elements("Data").Elements("Results Summary").Elements("Run-Status").AttributeValue(12)
        if (status_code & 1) == 1:      # 位元運算，1 為 results available
            return 'Available'
        elif (status_code & 4) == 4:    # 位元運算，4 為 results with warning
            return 'Warning'
        elif (status_code & 32) == 32:  # 位元運算，32 為 results with error
            return 'Error'
        else:
            raise UDE.AspenPlus_FileStatusError("File Status recognized error. " +
                                                "Please Connect Programmer !!!")

    def Show(self, log):
        """Show Aspen GUI or not.

        :param log: a Boolean value. True for Show the GUI, False for close the GUI.
        :return: None
        """
        ## 檢查log是否為布林值
        if type(log) != bool:
            raise TypeError("table must be 'Boolen' value.")

        self.aspen.Visible = log

    def Close(self):
        """Close AspenPlus COM object. After execute the AspenPlus, the function must be call.

        :return: None
        """
        self.aspen.Close()

    def Unit(self, item=None, table=False):
        """Show the Unit Table or specified category or specified unit in AspenPlus.

        :param item: if [], list the supported Unit category in AspenPlus.
        if [integer], list the supported Unit in specified Unit category in AspenPlus.
        if [integer, integer], show the Unit for specified parameters.
        :param table: a boolen value. default is False for print the result on the screen. If table=True,
        return result in  dictionary type.
        """
    ## 輸入變數檢查
        ## 檢查item是否為list格式或是None(預設值)
        if (type(item) != list) and (item is not None):
            raise TypeError("item has to be a 'None' or "
                            + "'List' with 1 integer parameter or "
                            + "'List' with 2 integer parameters!!")
        ## 檢查table是否為布林值
        if type(table)!= bool:
            raise TypeError("table must be 'Boolen' value.")

        ## 列出整數參數對應的單位類別
        if item is None:
            UT = {}
            for index, e in enumerate(self.aspen.Tree.Elements("Unit Table").Elements, start=1):
                if table:
                    UT[index] = e.Name
                elif not table:
                    print("{0:3d}{1:>15s}".format(index, e.Name))
        ## 列出選定單位類別的所有支援單位
        elif (type(item[0]) is int) and (len(item) == 1):   # 如果是空list應該會報錯
            ## 檢查第一參數不能超過設定值 (146)
            if item[0] > len(self.aspen.Tree.Elements("Unit Table").Elements):
                raise IndexError('The 1st index is out of range !!!')

            UT = {}
            ename = self.aspen.Tree.Elements("Unit Table").Elements.Item(item[0]-1).Name
            for index, e in enumerate(self.aspen.Tree.Elements("Unit Table").Elements(ename).Elements, start=1):
                if table:
                    UT[index] = e.Name
                elif not table:
                    print("{0:3d}{1:>15s}".format(index, e.Name))
        ## 顯示兩個整數參數所代表的單位
        elif (type(item[0]) is int) and (type(item[1]) is int) and (len(item) == 2):
            ## 檢查第二參數不能超過設定值
            if item[1] > len(self.aspen.Tree.Elements("Unit Table").Elements.Item(item[0]-1).Elements):
                raise IndexError('The 2nd index is out of range !!!')

            ename = self.aspen.Tree.Elements("Unit Table").Elements.Item(item[0]-1).Elements.Item(item[1]-1).Name
            if table:
                UT = ename
            elif not table:
                print(ename)
        else:
            raise TypeError("item has to be a 'None' or "
                            + "'List' with 1 integer parameter or "
                            + "'List' with 2 integer parameters!!")

        ## 如果table==True，就回傳一個字典，不然就印在畫面而已
        if table:
            return UT
        elif not table:
            return

    def UnitFind(self, obj, table=False):
        """Get the unit of physics property in AspenFile for the current unit setting.

        :param obj: an Aspen COMObject for the physics properties.
        :param table: a boolen value. default is False for print the result on the screen.
        :return: If table=True, return result in  string.
        """
        ## 檢查table是否為布林值
        if type(table) != bool:
            raise TypeError("table must be 'Boolen' value.")

        pq = obj.AttributeValue(2)
        um = obj.AttributeValue(3)
        return self.Unit([pq,um], table=table)

    def UnitChange(self, obj, unit_index):
        """Change the Unit in AspenFile for the physics properties.

        :param obj: an Aspen COMObject for the physics property.
        :param unit_index: index for the specified physics property in AspenPlus.
        It can be  search by the 'Unit()'  for what index for the desired unit.
        :return: float. a value with changing unit.
        """
        ## 將數值兩個單位引數分別記錄起來
        pq = obj.AttributeValue(2)
        um = unit_index

        ## 確認輸入引數是否為整數。確認obj輸入正確
        if type(um) != int:
            raise TypeError("unit_index must be integer")
        if type(pq) != int:
            raise IOError("obj doesn't has the unit. "
                          + "Please Check the input of obj.")

        ## 檢查um參數不能超過設定值
        if um > len(self.aspen.Tree.Elements("Unit Table").Elements.Item(pq - 1).Elements):
            raise IndexError('The um index is out of range !!!')

        return obj.ValueForUnit(pq, um)

    def ListBlocks(self):
        """Show all of the blocks in AspenFile.

        :return: None
        """
        print("{0[0]:11s}{0[1]:11s}".format(["Block_Name","Block_Type"]))
        print("======================")
        for e in self.aspen.Tree.Elements("Data").Elements("Blocks").Elements:
            ## 可以讀取所選物件的"Type"
            blocktype = self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(e.Name).AttributeValue(6)
            print("{0:11s}{1:11s}".format(e.Name,blocktype))
        print("(These are all of the blocks.)")

    def ListStreams(self):
        """Show all of the streams in AspenFile.

        :return: None
        """
        print("Streams_Name")
        print("============")
        for e in self.aspen.Tree.Elements("Data").Elements("Streams").Elements:
            print(e.Name)
        print("(These are all of the streams.)")

    def ListComponents(self):
        """Show all of the components in AspenFile.

        :return: None
        """
        print("Components_Name")
        print("===============")
        for e in self.aspen.Tree.Elements("Data").Elements("Components").Elements("Comp-Lists").Elements("GLOBAL").Elements("Input").Elements("CID").Elements:
            print(e.Value)
        print("(These are all of the components.)")

    def BlocksList(self) -> list:
        """Get the block-list in AspenFile with 'List Type'.

        :return: List. a list with all blocks name in AspenFile.
        """
        a_list = []
        for e in self.aspen.Tree.Elements("Data").Elements("Blocks").Elements:
            a_list.append(e.Name)
        return a_list

    def StreamsList(self) -> list:
        """Get the streams-list in AspenFile with 'List Type'.

        :return: List. a list with all streams name in AspenFile.
        """
        a_list = []
        for e in self.aspen.Tree.Elements("Data").Elements("Streams").Elements:
            a_list.append(e.Name)
        return a_list

    def ComponentsList(self) -> list:
        """Get the components-list in AspenFile with 'List Type'.

        :return: List. a list with all components name in AspenFile.
        """
        a_list = []
        for e in self.aspen.Tree.Elements("Data").Elements("Components").Elements("Comp-Lists").Elements("GLOBAL").Elements("Input").Elements("CID").Elements:
            a_list.append(e.Value)
        return a_list

    def Connections(self, bname, table=False):
        """Show the connected stream of the desired block.

        :param bname: block name in 'Str-Type'.
        :param table: a boolen value. default is False for print the result on the screen. If table=True,
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
            for e in self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Connections").Elements:
                streamtype = self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Connections").Elements(e.Name).Value
                print("{0:13s}{1:13s}".format(e.Name,streamtype))
        ## 將結果以列表輸出
        elif table:
            a_list = []
            for e in self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).Elements("Connections").Elements:
                a_list.append(e.Name)
            return a_list

    def BlockType(self, bname) -> str:
        """Get the block type of the bname in string.

        :param bname: Block name in AspenFile.
        :return: Sting. a string in block type for specified block.
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

        return self.aspen.Tree.Elements("Data").Elements("Blocks").Elements(bname).AttributeValue(6)


def check_name(Type):
    """Check the input variable-type for the name is correct or not, and whether the name is in the file or not .
        Finally, return the upper name to the program. The available name-type: block, stream.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Inner function for this decorator
            def name_up_and_arg_change(name, args):
                """將name變大寫並且回傳回args"""

                name = name.upper()
                args = list(args)   # 要把args第一個參數(name)變成大寫
                args[0] = name      # 但是args是tuple不能修改，所以要先
                args = tuple(args)  # 變成list，修改過後再轉回tuple
                return name, args

            if Type == 'stream':
                sname = args[0]

                ## 先檢查輸入的資料型態正確與否
                if type(sname) != str:
                    raise TypeError("sname must be a 'String'!!!")

                # 把sname變大寫並回傳回args
                sname, args = name_up_and_arg_change(sname, args)

                ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤
                if sname not in self.master.StreamsList():
                    raise UDE.AspenPlus_StreamTypeError("Cannot Find " + sname
                                                        + " in the AspenFile. "
                                                        + "Please Check the name you type!!")
            elif Type == 'block':
                bname = args[0]

                ## 先檢查輸入的資料型態正確與否
                if type(bname) != str:
                    raise TypeError("bname must be a 'String'!!!")

                # 把bname變大寫並回傳回args
                bname, args = name_up_and_arg_change(bname, args)

                ## 檢查輸入的物流名稱是否在檔案當中，如無回傳錯誤
                if bname not in self.master.BlocksList():
                    raise UDE.AspenPlus_BlockTypeError("Cannot Find " + bname
                                                        + " in the AspenFile. "
                                                        + "Please Check the name you type!!")
            else:
                raise TypeError('No Match Value for Type, '
                                + 'Please Check the value you type !!!')

            return func(self, *args, **kwargs)
        return wrapper
    return decorator
