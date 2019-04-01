# 匯入自定義錯誤，不然有些函式會找不到哪裡raise錯誤
from .. import UserDifineException as aspen_UDE
from . import UserDifineException as visio_UDE


class AspenConnector:
    """Some functions can connect the data from AspenFile."""
    def __init__(self, visio_master):
        self.visio_master = visio_master
        self.visio = visio_master.visio
        self.aspen_master = self.visio_master.aspen_master
        self.aspen = self.aspen_master.aspen

    def hello(self):
        print('hello AspenConnector!!!')

    def join_stream(self, aspen_name, visio_name, component, effdg):
        """Past the stream data to Visio file from AspenFile.

        :param aspen_name: the stream name in AspenFile.
        :param visio_name: the stream name in VisioFile.
        :param component: the component name in AspenFile.
        :param effdg: a list contains 4 integer which representing [Temperature, Pressure, Flowrate, Composition]
        :return: None.
        """
        ## 先檢查資料輸入型態是否正確
        if type(aspen_name) is not str:
            raise TypeError("aspen_name must be a 'String' !!!")
        if type(visio_name) is not str:
            raise TypeError("visio_name must be a 'String' !!!")
        if type(component) is not list:
            raise TypeError("component must be a 'List' !!!")
        if type(effdg) is not list:
            raise TypeError("effdg must be a 'List' !!!")

        ##將aspen_name變大寫
        aspen_name = aspen_name.upper()
        for i in range(len(component)):
            component[i] = component[i].upper()

        ##檢查輸入資料不存在
        if aspen_name not in self.aspen_master.StreamsList():
            raise aspen_UDE.AspenPlus_StreamTypeError(f"Cannot Find {aspen_name}"
                                                      + " in the AspenFile. "
                                                      + "Please Check the name you type!!")
        for i in component:
            if i not in self.aspen_master.ComponentsList():
                raise aspen_UDE.AspenPlus_ComponentTypeError(f"Cannot Find {i}"
                                                             + " in the AspenFile. "
                                                             + "Please Check the name you type!!")
        if len(effdg) != 4:
            raise IndexError("effgd must have 4 parameters exactly!!!")
        for i in range(4):
            if type(effdg[i]) is not int:
                raise TypeError("The elements in effdg must be 'Integer'!!!")
            if effdg[i] < 0:
                raise ValueError("The elements should not be a negative number!!")

        ## 匯入個物性之有效位數
        Tefdg = "{:." + str(effdg[0]) + "f}"
        Pefdg = "{:." + str(effdg[1]) + "f}"
        Fefdg = "{:." + str(effdg[2]) + "f}"
        Xefdg = "{:." + str(effdg[3]) + "f}"

        ## 從Aspen讀取物流資訊並帶入有效位數
        comp = []
        for i in component: # 讀取分率
            comp.append(i + ' ' + Xefdg.format(self.aspen_master.Stream.getMoleFrac(aspen_name, i)))
        FFTemp = ' '.join([Tefdg.format(self.aspen_master.Stream.getTemperature(aspen_name)),
                          self.aspen_master.Stream.getTemperature(aspen_name, get_unit=True)])
        FFPres = ' '.join([Pefdg.format(self.aspen_master.Stream.getPressure(aspen_name)),
                          self.aspen_master.Stream.getPressure(aspen_name, get_unit=True)])
        FFmol = ' '.join([Fefdg.format(self.aspen_master.Stream.getMoleFlow(aspen_name)),
                          self.aspen_master.Stream.getMoleFlow(aspen_name, get_unit=True)])

        TPconfig = '; '.join([FFTemp, FFPres])  # 將溫度壓力合在一起變一行

        textbox = '\n'.join([visio_name, TPconfig, FFmol] + comp)   # 變成visio裡面要打印出來的格式

        ## 找尋指定visio_name是在visio裡的哪個visio index物件
        visio_object = None
        for visio_id in self.visio_master.num_arr:
            if self.visio_master.item_with_index(visio_id).Text.find(visio_name) != -1:
                visio_object = self.visio_master.item_with_index(visio_id)
                break
        if visio_object is None:   # 在VisioFile找不到visio_name就回報錯誤
            raise visio_UDE.Visio_ItemNotExist(f"Cannot Find '{visio_name}' in VisioFile." +
                                               "Please check the name you type!!!")

        ## 對文字框修改內容與其性質(顏色、大小...)
        visio_object.Text = textbox     # 將從Aspen得到的資訊貼到visio物件
        visio_object.CharProps(1, 0)    # 將文字框的顏色先全部變成黑色

        begin_TPconfig = visio_object.Text.find(TPconfig)   # 這邊是一個定位visio文字框某些位置的指令，要先用Begin找到
        end_TPconfig = begin_TPconfig + len(TPconfig)       # 文字框的第一字母，再用End找到文字框的最後一個字母，如此一
        visio_object.Begin = begin_TPconfig                 # 來之後對相同文字框物件修改性質只會改到指定範圍內的字母。
        visio_object.End = end_TPconfig

        visio_object.CharProps(1,4)     # 將指定文字改成藍色

    def join_cooled_duty(self, aspen_name, visio_name, effdg):
        """Past the cooled_duty data to Visio file from AspenFile.

        :param aspen_name: the block name which must be a RadFrac or Heater in AspenFile.
        :param visio_name:  the block name in VisioFile.
        :param effdg: the effective digit of duty display.
        :return:  None.
        """
        ## 先檢查資料輸入型態是否正確
        if type(aspen_name) is not str:
            raise TypeError("aspen_name must be a 'String' !!!")
        if type(visio_name) is not str:
            raise TypeError("visio_name must be a 'String' !!!")
        if type(effdg) is not int:
            raise TypeError("effdg must be a 'Integer' !!!")
        if effdg < 0:
            raise ValueError("The elements should not be a negative number!!")

        ##將aspen_name變大寫
        aspen_name = aspen_name.upper()

        ##檢查輸入資料不存在
        if aspen_name not in self.aspen_master.BlocksList():
            raise aspen_UDE.AspenPlus_BlockTypeError(f"Cannot Find {aspen_name}"
                                                      + " in the AspenFile. "
                                                      + "Please Check the name you type!!")

        ## 檢查bname是否為RadFrac或Heater並進行duty讀取
        duty = None
        dutyunit = None
        if self.aspen_master.BlockType(aspen_name) == 'RadFrac':
            duty = self.aspen_master.Distillation.getQC(aspen_name)
            dutyunit = self.aspen_master.Distillation.getQC(aspen_name, get_unit=True)
        elif self.aspen_master.BlockType(aspen_name) == 'Heater':
            duty = self.aspen_master.Heater.getQ(aspen_name)
            dutyunit = self.aspen_master.Heater.getQ(aspen_name, get_unit=True)
        else:
            raise aspen_UDE.AspenPlus_BlockTypeError(aspen_name + ' is not a RadFrac or Heater,'
                                                     + 'please check the name you type!!')
        ## 匯入個物性之有效位數
        efdg = "{:." + str(effdg) + "f}"
        textbox = ' '.join([visio_name, '=', efdg.format(duty), dutyunit])  # 變成visio裡面要打印出來的格式

        ## 找尋指定visio_name是在visio裡的哪個visio index物件
        visio_object = None
        for visio_id in self.visio_master.num_arr:
            if self.visio_master.item_with_index(visio_id).Text.find(visio_name) != -1:
                visio_object = self.visio_master.item_with_index(visio_id)
                break
        if visio_object is None:  # 在VisioFile找不到visio_name就回報錯誤
            raise visio_UDE.Visio_ItemNotExist(f"Cannot Find '{visio_name}' in VisioFile." +
                                               "Please check the name you type!!!")

        # 將從Aspen得到的資訊貼到visio物件
        visio_object.Text = textbox

    def join_heat_duty(self, aspen_name, visio_name, effdg):
        """Past the cooled_duty data to Visio file from AspenFile.

        :param aspen_name: the block name which must be a RadFrac or Heater in AspenFile.
        :param visio_name:  the block name in VisioFile.
        :param effdg: the effective digit of duty display.
        :return:  None.
        """
        ## 先檢查資料輸入型態是否正確
        if type(aspen_name) is not str:
            raise TypeError("aspen_name must be a 'String' !!!")
        if type(visio_name) is not str:
            raise TypeError("visio_name must be a 'String' !!!")
        if type(effdg) is not int:
            raise TypeError("effdg must be a 'Integer' !!!")
        if effdg < 0:
            raise ValueError("The elements should not be a negative number!!")

        ##將aspen_name變大寫
        aspen_name = aspen_name.upper()

        ##檢查輸入資料不存在
        if aspen_name not in self.aspen_master.BlocksList():
            raise aspen_UDE.AspenPlus_BlockTypeError(f"Cannot Find {aspen_name}"
                                                      + " in the AspenFile. "
                                                      + "Please Check the name you type!!")

        ## 檢查bname是否為RadFrac或Heater並進行duty讀取
        duty = None
        dutyunit = None
        if self.aspen_master.BlockType(aspen_name) == 'RadFrac':
            duty = self.aspen_master.Distillation.getQR(aspen_name)
            dutyunit = self.aspen_master.Distillation.getQR(aspen_name, get_unit=True)
        elif self.aspen_master.BlockType(aspen_name) == 'Heater':
            duty = self.aspen_master.Heater.getQ(aspen_name)
            dutyunit = self.aspen_master.Heater.getQ(aspen_name, get_unit=True)
        else:
            raise aspen_UDE.AspenPlus_BlockTypeError(aspen_name + ' is not a RadFrac or Heater,'
                                                     + 'please check the name you type!!')
        ## 匯入個物性之有效位數
        efdg = "{:." + str(effdg) + "f}"
        textbox = ' '.join([visio_name, '=', efdg.format(duty), dutyunit])  # 變成visio裡面要打印出來的格式

        ## 找尋指定visio_name是在visio裡的哪個visio index物件
        visio_object = None
        for visio_id in self.visio_master.num_arr:
            if self.visio_master.item_with_index(visio_id).Text.find(visio_name) != -1:
                visio_object = self.visio_master.item_with_index(visio_id)
                break
        if visio_object is None:  # 在VisioFile找不到visio_name就回報錯誤
            raise visio_UDE.Visio_ItemNotExist(f"Cannot Find '{visio_name}' in VisioFile." +
                                               "Please check the name you type!!!")

        # 將從Aspen得到的資訊貼到visio物件
        visio_object.Text = textbox

    def join_distillation_data(self, aspen_name, visio_name, effdg, RR_force_show=None):
        """Past the distillation data to Visio file from AspenFile.

        :param aspen_name: the distillation name in AspenFile.
        :param visio_name: the distillation name in VisioFile.
        :param effdg: a list contains 2 integer which representing [Reflux Ratio, Diameter]
        :return: None.
        """
        ## 先檢查資料輸入型態是否正確
        if type(aspen_name) is not str:
            raise TypeError("aspen_name must be a 'String' !!!")
        if type(visio_name) is not str:
            raise TypeError("visio_name must be a 'String' !!!")
        if type(effdg) is not list:
            raise TypeError("effdg must be a 'List' !!!")

        ##將aspen_name變大寫
        aspen_name = aspen_name.upper()

        ##檢查輸入單元名稱不存在AspenFile中
        if aspen_name not in self.aspen_master.BlocksList():
            raise aspen_UDE.AspenPlus_BlockTypeError(f"Cannot Find {aspen_name}"
                                                      + " in the AspenFile. "
                                                      + "Please Check the name you type!!")
        ## 檢查bname是否為RadFrac
        if self.aspen_master.BlockType(aspen_name) != 'RadFrac':
            raise aspen_UDE.AspenPlus_BlockTypeError(aspen_name + ' is not a RadFrac,'
                                               + 'please check the name you type!!')
        ## 檢查有效位數參數是否無效
        if len(effdg) != 2:
            raise IndexError("effgd must have 2 parameters exactly!!!")
        for i in range(2):
            if type(effdg[i]) is not int:
                raise TypeError("The elements in effdg must be 'Integer'!!!")
            if effdg[i] < 0:
                raise ValueError("The elements should not be a negative number!!")

        ## 匯入個物性之有效位數
        Refdg = "{:." + str(effdg[0]) + "f}"
        Defdg = "{:." + str(effdg[1]) + "f}"

        ## 從Aspen讀取物流資訊並帶入有效位數
        Ndata = ' '.join(['NT =', str(self.aspen_master.Distillation.getNStage(aspen_name))])
        Rdata = ' '.join(['RR =', Refdg.format(self.aspen_master.Distillation.getRefluxRatio(aspen_name))])
        Ddata = ' '.join(['D =', Defdg.format(self.aspen_master.Distillation.getDiameter(aspen_name)),
                          self.aspen_master.Distillation.getDiameter(aspen_name, get_unit=True)])

        textbox = None
        if RR_force_show is None:   # 沒強制show RR，就用我的判斷
            if self.aspen_master.Distillation.getQC(aspen_name) is None:    # 沒冷凝器，表示Stripper
                textbox = '\n'.join([visio_name, Ndata, Ddata])   # 變成visio裡面要打印出來的格式
            else:   # 有冷凝器，就show RR
                textbox = '\n'.join([visio_name, Ndata, Rdata, Ddata])   # 變成visio裡面要打印出來的格式
        elif RR_force_show:         # 強制show RR
            textbox = '\n'.join([visio_name, Ndata, Rdata, Ddata])   # 變成visio裡面要打印出來的格式
        elif not RR_force_show:     # 強制不show RR
            textbox = '\n'.join([visio_name, Ndata, Ddata])   # 變成visio裡面要打印出來的格式


        ## 找尋指定visio_name是在visio裡的哪個visio index物件
        visio_object = None
        for visio_id in self.visio_master.num_arr:
            if self.visio_master.item_with_index(visio_id).Text.find(visio_name) != -1:
                visio_object = self.visio_master.item_with_index(visio_id)
                break
        if visio_object is None:   # 在VisioFile找不到visio_name就回報錯誤
            raise visio_UDE.Visio_ItemNotExist(f"Cannot Find '{visio_name}' in VisioFile." +
                                               "Please check the name you type!!!")

        # 將從Aspen得到的資訊貼到visio物件
        visio_object.Text = textbox

    def join_extractor_data(self, aspen_name, visio_name, solvent, feed, effdg):
        """Past the distillation data to Visio file from AspenFile.

        :param aspen_name: the distillation name in AspenFile.
        :param visio_name: the distillation name in VisioFile.
        :param solvent: the solvent inlet on extractor.
        :param feed: the feed for extracted stream.
        :param effdg: a list contains 2 integer which representing [Diameter, FS/FF]
        :return: None.
        """
        ## 先檢查資料輸入型態是否正確
        if type(aspen_name) is not str:
            raise TypeError("aspen_name must be a 'String' !!!")
        if type(visio_name) is not str:
            raise TypeError("visio_name must be a 'String' !!!")
        if type(solvent) is not str:
            raise TypeError("visio_name must be a 'String' !!!")
        if type(feed) is not str:
            raise TypeError("visio_name must be a 'String' !!!")
        if type(effdg) is not list:
            raise TypeError("effdg must be a 'List' !!!")

        ##將aspen_name變大寫
        aspen_name = aspen_name.upper()
        solvent = solvent.upper()
        feed = feed.upper()

        ##檢查輸入單元、物流名稱不存在AspenFile中
        if aspen_name not in self.aspen_master.BlocksList():
            raise aspen_UDE.AspenPlus_BlockTypeError(f"Cannot Find {aspen_name}"
                                                     + " in the AspenFile. "
                                                     + "Please Check the name you type!!")
        if solvent not in self.aspen_master.StreamsList():
            raise aspen_UDE.AspenPlus_StreamTypeError(f"Cannot Find {solvent}"
                                                      + " in the AspenFile. "
                                                      + "Please Check the name you type!!")
        if feed not in self.aspen_master.StreamsList():
            raise aspen_UDE.AspenPlus_StreamTypeError(f"Cannot Find {feed}"
                                                      + " in the AspenFile. "
                                                      + "Please Check the name you type!!")
        ## 檢查bname是否為RadFrac
        if self.aspen_master.BlockType(aspen_name) != 'Extract':
            raise aspen_UDE.AspenPlus_BlockTypeError(aspen_name + ' is not a Extract,'
                                                     + 'please check the name you type!!')
        ## 檢查有效位數參數是否無效
        if len(effdg) != 2:
            raise IndexError("effgd must have 2 parameters exactly!!!")
        for i in range(2):
            if type(effdg[i]) is not int:
                raise TypeError("The elements in effdg must be 'Integer'!!!")
            if effdg[i] < 0:
                raise ValueError("The elements should not be a negative number!!")

        ## 匯入個物性之有效位數
        Defdg = "{:." + str(effdg[0]) + "f}"
        FSefdg = "{:." + str(effdg[1]) + "f}"

        ## 從Aspen讀取物流資訊並帶入有效位數
        Ndata = ' '.join(['NTE =', str(self.aspen_master.Extractor.getNStage(aspen_name))])
        Ddata = ' '.join(['D =', Defdg.format(self.aspen_master.Extractor.getDiameter(aspen_name)),
                          self.aspen_master.Extractor.getDiameter(aspen_name, get_unit=True)])
        FSdata = ' '.join([r'FS/FF =', FSefdg.format(
            self.aspen_master.Stream.getMoleFlow(solvent) / self.aspen_master.Stream.getMoleFlow(feed))])

        textbox = '\n'.join([visio_name, Ndata, Ddata, FSdata])   # 變成visio裡面要打印出來的格式

        ## 找尋指定visio_name是在visio裡的哪個visio index物件
        visio_object = None
        for visio_id in self.visio_master.num_arr:
            if self.visio_master.item_with_index(visio_id).Text.find(visio_name) != -1:
                visio_object = self.visio_master.item_with_index(visio_id)
                break
        if visio_object is None:   # 在VisioFile找不到visio_name就回報錯誤
            raise visio_UDE.Visio_ItemNotExist(f"Cannot Find '{visio_name}' in VisioFile." +
                                               "Please check the name you type!!!")

        # 將從Aspen得到的資訊貼到visio物件
        visio_object.Text = textbox
