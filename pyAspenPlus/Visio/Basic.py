import win32com.client as win32


class Visio:
    def __init__(self, aspen_master, visio_path):
        self.aspen_master = aspen_master
        self.aspen = aspen_master.aspen

        self.visio = win32.Dispatch('Visio.Application')

        self.visio.Visible = False
        self.visio.Documents.Open(visio_path)

        ##找看看此檔案有幾個物件與個別的名稱
        k = 0
        self.num_arr = []
        for num in range(0, 2001):
            try:
                self.visio.ActiveWindow.Page.Shapes.ItemFromID(num).Characters
            except:
                pass
            else:
                self.num_arr.append(num)
                k = k + 1

    def __del__(self):
        """Close Visio COM Object after Visio class destroyed."""
        self.visio.Quit()

    def Show(self, log):
        """To Show or Hide the Visio Window.

        :param log: boolean variable. True for show the window. vice versa.
        :return: None.
        """
        ## 檢查輸入變數型態
        if type(log) != bool:
            raise TypeError("log must be 'Boolean' value.")

        self.visio.Visible = log

    def item_with_index(self, index):
        """Get the object of visio item of specified visio index.

        :param index: Integer. the visio index of visio item.
        :return: visio object.
        """
        ## 檢查輸入的資料型態正確與否
        if type(index) != int:
            raise TypeError("index must be a 'Integer'!!!")

        return self.visio.ActiveWindow.Page.Shapes.ItemFromID(index).Characters
