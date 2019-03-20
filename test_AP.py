import unittest
import AspenPlus

path = "D:\\Google Cloud\\Python\\Great program for AspenPlus\\TestFile\\DistillationColumn.apw"
Aspen = AspenPlus.AP(path)
obj = Aspen.aspen.Tree.FindNode("\Data\Streams\B1\Output\TOT_FLOW")


class Basic_test(unittest.TestCase):
    # def test_Error(self):
    #     self.assertEqual(Aspen.Error(), )
    def test_Show(self):
        # 測試 Aspen.Show 的 log 參數輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "table must be 'Boolen' value.",
            Aspen.Show,
            123)

    def test_Unit(self):
        # 測試 Aspen.Unit 的 item 參數輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "item has to be a 'None' or .*",
            Aspen.Unit,
            123)
        # 測試 Aspen.Unit 的 table 參數輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "table must be 'Boolen' value.",
            Aspen.Unit,
            [], 123)


class Stream_test(unittest.TestCase):
    def sname_test(self, fun, correct_value):
        # 測試 sname 輸入正常時功能正常
        self.assertEqual(
            fun('b1'),
            correct_value)

        # 測試輸入之 sname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_StreamTypeError,
            "Cannot Find B11 in the AspenFile. Please Check the name you type!!",
            fun,
            'b11')
        # 測試輸入 sname 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "sname must be a 'String'!!!",
            fun,
            123)

    def component_test(self, fun, correct_value):
        # 測試 component 輸入正常時功能正常
        self.assertEqual(
            fun('b1', component='water'),
            correct_value)

        # 測試輸入之 component 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_ComponentTypeError,
            "Cannot Find WATERR in the AspenFile. Please Check the name you type!!",
            fun,
            'b1', component='waterr')
        # 測試輸入 component 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "component must be a 'String'!!!",
            fun,
            'b1', component=123)

    def getunit_test(self, fun, correct_value):
        # 測試 getunit 輸入正常時功能正常
        self.assertEqual(
            fun('b1', get_unit=True),
            correct_value)

        # 測試輸入 getunit 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit must be a 'Boolean'!!!",
            fun,
            'b1', get_unit=123)

    def unitchangeto_test(self, fun, correct_value, pre):
        # 測試 unitchangeto 輸入正常時功能正常
        self.assertAlmostEqual(
            fun('b1', unit_change_to=1),
            correct_value, pre)

        # 測試輸入 unitchangeto 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit_change_to must be a 'Integer' or 'None'!!!",
            fun,
            'b1', unit_change_to='123')

        # 測試輸入 unitchangeto 超出內建合法值
        self.assertRaisesRegex(
            IndexError,
            'The um index is out of range !!!',
            fun,
            'b1', unit_change_to=1234)

    def test_getMoleFlow(self):
        """進行 getMoleFlow 函式的各種測試，測試內容如下：
        # 測試　Aspen.StreamgetMoleFlow 中 sname 的功能
        # 測試　Aspen.StreamgetMoleFlow 中 component 的功能
        # 測試　Aspen.StreamgetMoleFlow 中 getunit 的功能
        # 測試　Aspen.StreamgetMoleFlow 中 unitchangeto 的功能

        # 測試 Aspen.Stream.getMoleFlow 的取得轉換單位後物流流量單位功能
        # 測試 Aspen.Stream.getMoleFlow 的取得組分物流流量單位功能
        # 測試 Aspen.Stream.getMoleFlow 的取得轉換單位後組分物流流量功能
        # 測試 Aspen.Stream.getMoleFlow 的取得轉換單位後組分物流流量單位功能
        """
        # 測試　Aspen.StreamgetMoleFlow 中 sname 的功能
        self.sname_test(Aspen.Stream.getMoleFlow, 50.0)

        # 測試　Aspen.StreamgetMoleFlow 中 component 的功能
        self.component_test(Aspen.Stream.getMoleFlow, 39.309023)

        # 測試　Aspen.StreamgetMoleFlow 中 getunit 的功能
        self.getunit_test(Aspen.Stream.getMoleFlow, 'kmol/hr')

        # 測試　Aspen.StreamgetMoleFlow 中 unitchangeto 的功能
        self.unitchangeto_test(Aspen.Stream.getMoleFlow, 0.0138888888, 9)


        # 測試 Aspen.Stream.getMoleFlow 的取得轉換單位後物流流量單位功能
        self.assertEqual(
            Aspen.Stream.getMoleFlow('b1', get_unit=True, unit_change_to=1),
            'kmol/sec')
        # 測試 Aspen.Stream.getMoleFlow 的取得組分物流流量單位功能
        self.assertEqual(
            Aspen.Stream.getMoleFlow('b1', component='water', get_unit=True),
            'kmol/hr')
        # 測試 Aspen.Stream.getMoleFlow 的取得轉換單位後組分物流流量功能
        self.assertAlmostEqual(
            Aspen.Stream.getMoleFlow('b1', component='water', get_unit=False, unit_change_to=1),
            0.010919173055555564,
            17)
        # 測試 Aspen.Stream.getMoleFlow 的取得轉換單位後組分物流流量單位功能
        self.assertEqual(
            Aspen.Stream.getMoleFlow('b1', component='water', get_unit=True, unit_change_to=1),
            'kmol/sec')

    def test_getMoleFrac(self):
        """進行 getMoleFrac 函式的各種測試，測試內容如下：
       # 測試　Aspen.StreamgetMoleFrac 中 snme 與 component 的功能

        # 測試 Aspen.Stream.getMoleFrac 的 sname 找不到物流之Aspen物流錯誤
        # 測試 Aspen.Stream.getMoleFrac 的 sname 輸入型態錯誤
        """
        # 測試　Aspen.StreamgetMoleFrac 中 snme 與 component 的功能
        self.component_test(Aspen.Stream.getMoleFrac, 0.7861804600000001)

        # 測試 Aspen.Stream.getMoleFrac 的 sname 找不到物流之Aspen物流錯誤
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_StreamTypeError,
            "Cannot Find B11 in the AspenFile. Please Check the name you type!!",
            Aspen.Stream.getMoleFrac,
            'b11', 'water')
        # 測試 Aspen.Stream.getMoleFrac 的 sname 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "sname must be a 'String'!!!",
            Aspen.Stream.getMoleFrac,
            123, 'water')

    def test_getMassFlow(self):
        """進行 getMassFlow 函式的各種測試，測試內容如下：
        # 測試　Aspen.StreamgetMassFlow 中 sname 的功能
        # 測試　Aspen.StreamgetMassFlow 中 component 的功能
        # 測試　Aspen.StreamgetMassFlow 中 getunit 的功能
        # 測試　Aspen.StreamgetMassFlow 中 unitchangeto 的功能

        # 測試 Aspen.Stream.getMassFlow 的取得轉換單位後物流流量單位功能
        # 測試 Aspen.Stream.getMassFlow 的取得組分物流流量單位功能
        # 測試 Aspen.Stream.getMassFlow 的取得轉換單位後組分物流流量功能
        # 測試 Aspen.Stream.getMassFlow 的取得轉換單位後組分物流流量單位功能
        """
        # 測試　Aspen.StreamgetMassFlow 中 sname 的功能
        self.sname_test(Aspen.Stream.getMassFlow, 1200.6861)

        # 測試　Aspen.StreamgetMassFlow 中 component 的功能
        self.component_test(Aspen.Stream.getMassFlow, 708.163055)

        # 測試　Aspen.StreamgetMassFlow 中 getunit 的功能
        self.getunit_test(Aspen.Stream.getMassFlow, 'kg/hr')

        # 測試　Aspen.StreamgetMassFlow 中 unitchangeto 的功能
        self.unitchangeto_test(Aspen.Stream.getMassFlow, 0.3335239166666669, 15)

        # 測試 Aspen.Stream.getMassFlow 的取得轉換單位後物流流量單位功能
        self.assertEqual(
            Aspen.Stream.getMassFlow('b1', get_unit=True, unit_change_to=1),
            'kg/sec')
        # 測試 Aspen.Stream.getMassFlow 的取得組分物流流量單位功能
        self.assertEqual(
            Aspen.Stream.getMassFlow('b1', component='water', get_unit=True),
            'kg/hr')
        # 測試 Aspen.Stream.getMassFlow 的取得轉換單位後組分物流流量功能
        self.assertAlmostEqual(
            Aspen.Stream.getMassFlow('b1', component='water', get_unit=False, unit_change_to=1),
            0.19671195972222238,
            16)
        # 測試 Aspen.Stream.getMassFlow 的取得轉換單位後組分物流流量單位功能
        self.assertEqual(
            Aspen.Stream.getMassFlow('b1', component='water', get_unit=True, unit_change_to=1),
            'kg/sec')

    def test_getMassFrac(self):
        """進行 getMassFrac 函式的各種測試，測試內容如下：
        # 測試　Aspen.StreamgetMassFrac 中 snme 與 component 的功能

        # 測試 Aspen.Stream.getMassFrac 的 sname 找不到物流之Aspen物流錯誤
        # 測試 Aspen.Stream.getMassFrac 的 sname 輸入型態錯誤
        """
        # 測試　Aspen.StreamgetMassFrac 中 snme 與 component 的功能
        self.component_test(Aspen.Stream.getMassFrac, 0.589798661781793)

        # 測試 Aspen.Stream.getMassFrac 的 sname 找不到物流之Aspen物流錯誤
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_StreamTypeError,
            "Cannot Find B11 in the AspenFile. Please Check the name you type!!",
            Aspen.Stream.getMassFrac,
            'b11', 'water')
        # 測試 Aspen.Stream.getMassFrac 的 sname 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "sname must be a 'String'!!!",
            Aspen.Stream.getMassFrac,
            123, 'water')

    def test_getTemperature(self):
        """進行 getTemperature 函式的各種測試，測試內容如下：
        # 測試　Aspen.Stream.getTemperature 中 sname 的功能
        # 測試　Aspen.Stream.getTemperature 中 getunit 的功能
        # 測試　Aspen.Stream.getTemperature 中 unitchangeto 的功能

        # 測試 Aspen.Stream.getTemperature 的取得轉換單位後物流流量單位功能
        """
        # 測試　Aspen.Stream.getTemperature 中 sname 的功能
        self.sname_test(Aspen.Stream.getTemperature, 361.224387)

        # 測試　Aspen.Stream.getTemperature 中 getunit 的功能
        self.getunit_test(Aspen.Stream.getTemperature, 'K')

        # 測試　Aspen.Stream.getTemperature 中 unitchangeto 的功能
        self.unitchangeto_test(Aspen.Stream.getTemperature, 361.224387, 5)

        # 測試 Aspen.Stream.getTemperature 的取得轉換單位後物流流量單位功能
        self.assertEqual(
            Aspen.Stream.getTemperature('b1', get_unit=True, unit_change_to=1),
            'K')

    def test_getPressure(self):
        """進行 getPressure 函式的各種測試，測試內容如下：
        # 測試　Aspen.Stream.getPressure 中 sname 的功能
        # 測試　Aspen.Stream.getPressure 中 getunit 的功能
        # 測試　Aspen.Stream.getPressure 中 unitchangeto 的功能

        # 測試 Aspen.Stream.getPressure 的取得轉換單位後物流流量單位功能
        """
        # 測試　Aspen.Stream.getPressure 中 sname 的功能
        self.sname_test(Aspen.Stream.getPressure, 1.2312)

        # 測試　Aspen.Stream.getPressure 中 getunit 的功能
        self.getunit_test(Aspen.Stream.getPressure, 'atm')

        # 測試　Aspen.Stream.getPressure 中 unitchangeto 的功能
        self.unitchangeto_test(Aspen.Stream.getPressure, 124751.34000000001, 10)

        # 測試 Aspen.Stream.getPressure 的取得轉換單位後物流流量單位功能
        self.assertEqual(
            Aspen.Stream.getPressure('b1', get_unit=True, unit_change_to=1),
            'N/sqm')

    def test_getVaporFrac(self):
        """進行 getPressure 函式的各種測試，測試內容如下：
        # 測試　Aspen.Stream.getVaporFrac 中 sname 的功能
        """
        # 測試　Aspen.Stream.getVaporFrac 中 sname 的功能
        self.sname_test(Aspen.Stream.getVaporFrac, 0.0)

    def test_getVolumeFlow(self):
        """進行 getVolumeFlow 函式的各種測試，測試內容如下：
        # 測試　Aspen.Stream.getVolumeFlow 中 sname 的功能
        # 測試　Aspen.Stream.getVolumeFlow 中 getunit 的功能
        # 測試　Aspen.Stream.getVolumeFlow 中 unitchangeto 的功能

        # 測試 Aspen.Stream.getVolumeFlow 的取得轉換單位後物流流量單位功能
        """
        # 測試　Aspen.Stream.getVolumeFlow 中 sname 的功能
        self.sname_test(Aspen.Stream.getVolumeFlow, 1.43922982)

        # 測試　Aspen.Stream.getVolumeFlow 中 getunit 的功能
        self.getunit_test(Aspen.Stream.getVolumeFlow, 'cum/hr')

        # 測試　Aspen.Stream.getVolumeFlow 中 unitchangeto 的功能
        self.unitchangeto_test(Aspen.Stream.getVolumeFlow, 0.0003997860611111114, 18)

        # 測試 Aspen.Stream.getVolumeFlow 的取得轉換單位後物流流量單位功能
        self.assertEqual(
            Aspen.Stream.getVolumeFlow('b1', get_unit=True, unit_change_to=1),
            'cum/sec')


class Distillation_test(unittest.TestCase):
    def bname_test(self, fun, correct_value):
        # 測試 bname 輸入正常時功能正常
        self.assertEqual(
            fun('c2-size'),
            correct_value)

        # 測試輸入之 bname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "Cannot Find C11 in the AspenFile. Please Check the name you type!!",
            fun,
            'c11')
        # 測試輸入 bname 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "bname must be a 'String'!!!",
            fun,
            123)

        # 測試輸入 bname 非RadFrac
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "C3-RE is not a RadFrac,please check the name you type!!",
            fun,
            'c3-re')

    def getunit_test(self, fun, correct_value):
        # 測試 getunit 輸入正常時功能正常
        self.assertEqual(
            fun('c2-size', get_unit=True),
            correct_value)

        # 測試輸入 getunit 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit must be a 'Boolean'!!!",
            fun,
            'c2-size', get_unit=123)

    def unitchangeto_test(self, fun, correct_value, pre):
        # 測試 unitchangeto 輸入正常時功能正常
        self.assertAlmostEqual(
            fun('c2-size', unit_change_to=2),
            correct_value, pre)

        # 測試輸入 unitchangeto 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit_change_to must be a 'Integer' or 'None'!!!",
            fun,
            'c2-size', unit_change_to='123')

        # 測試輸入 unitchangeto 超出內建合法值
        self.assertRaisesRegex(
            IndexError,
            'The um index is out of range !!!',
            fun,
            'c2-size', unit_change_to=1234)

    def test_getNStage(self):
        """進行 getNStage 函式的各種測試，測試內容如下：
        # 測試　Aspen.Distillation.setNStage 中 bname 的功能
        """
        # 測試　Aspen.Distillation.getNStage 中 bname 的功能
        self.bname_test(Aspen.Distillation.getNStage, 35)

    def test_setNStage(self):
        """進行 setNStage 函式的各種測試，測試內容如下：
       # 測試 Aspen.Distillation.setNStage 功能正常

        # 測試 Aspen.Distillation.setNStage 中 bname 不存在檔案中時
        # 測試 Aspen.Distillation.setNStage 中 bname 輸入型態錯誤
        # 測試 Aspen.Distillation.setNStage 中 set_value 輸入型態錯誤
        # 測試 Aspen.Distillation.setNStage 中 set_value 為負整數
        """
        # 測試 Aspen.Distillation.setNStage 功能正常
        origin = Aspen.Distillation.getNStage('c1')
        Aspen.Distillation.setNStage('c1', set_value=origin+1)
        self.assertEqual(Aspen.Distillation.getNStage('c1'), origin+1)
        Aspen.Distillation.setNStage('c1', set_value=origin)

        # 測試 Aspen.Distillation.setNStage 中 bname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "Cannot Find C11 in the AspenFile. Please Check the name you type!!",
            Aspen.Distillation.setNStage,
            'c11', set_value=35)

        # 測試 Aspen.Distillation.setNStage 中 bname 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "bname must be a 'String'!!!",
            Aspen.Distillation.setNStage,
            123, set_value=35)

        # 測試 Aspen.Distillation.setNStage 中 set_value 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "set_value must be a 'Integer'!!!",
            Aspen.Distillation.setNStage,
            'c1', set_value='')

        # 測試 Aspen.Distillation.setNStage 中 set_value 為負整數
        self.assertRaisesRegex(
            ValueError,
            "set_value must be a 'Positive' number!!!",
            Aspen.Distillation.setNStage,
            'c1', set_value=-30)

    def test_getNF(self):
        """進行 getNF 函式的各種測試，測試內容如下：
        # 測試　Aspen.Distillation.getNF 中 bname 的功能

        # 測試輸入 sname 不存在AspenFile當中
        # 測試輸入 sname 不是指定蒸餾塔之進料物流
        # 測試輸入 sname 輸入型態錯誤
        """
        # 測試　Aspen.Distillation.getNF 中 bname 的功能
        self.bname_test(Aspen.Distillation.getNF, ['F2'])

        # 測試　Aspen.Distillation.getNF 中 sname 的功能正常
        self.assertEqual(
            Aspen.Distillation.getNF('c1', sname='f1'),
            15)

        # 測試輸入 sname 不存在AspenFile當中
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_StreamTypeError,
            'Cannot Find F11 in the AspenFile. Please Check the name you type!!',
            Aspen.Distillation.getNF,
            'c1', sname='f11')

        # 測試輸入 sname 不是指定蒸餾塔之進料物流
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_StreamTypeError,
            'F2 is not a feed stream for C1. Please Check the name you type!!',
            Aspen.Distillation.getNF,
            'c1', sname='f2')

        # 測試輸入 sname 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "sname must be a 'String'!!!",
            Aspen.Distillation.getNF,
            'c1', sname=123)

    def test_setNF(self):
        """進行 setNF 函式的各種測試，測試內容如下：
       # 測試 Aspen.Distillation.setNF 功能正常

        # 測試 Aspen.Distillation.setNF 中 bname 不存在檔案中時
        # 測試 Aspen.Distillation.setNF 中 bname 輸入型態錯誤
        # 測試 Aspen.Distillation.setNF 中 sname 不存在檔案中時
        # 測試 Aspen.Distillation.setNF 中 sname 非指定蒸餾塔之進料物流
        # 測試 Aspen.Distillation.setNF 中 sname 輸入型態錯誤
        # 測試 Aspen.Distillation.setNF 中 set_value 輸入型態錯誤
        # 測試 Aspen.Distillation.setNF 中 set_value 為負整數
        """
        # 測試 Aspen.Distillation.setNF 功能正常
        origin = Aspen.Distillation.getNF('c1', sname='f1')
        Aspen.Distillation.setNF('c1', sname='f1', set_value=origin+1)
        self.assertEqual(Aspen.Distillation.getNF('c1', sname='f1'), origin+1)
        Aspen.Distillation.setNF('c1', sname='f1', set_value=origin)

        # 測試 Aspen.Distillation.setNF 中 bname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "Cannot Find C11 in the AspenFile. Please Check the name you type!!",
            Aspen.Distillation.setNF,
            'c11', sname='f1', set_value=15)

        # 測試 Aspen.Distillation.setNF 中 bname 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "bname must be a 'String'!!!",
            Aspen.Distillation.setNF,
            123, sname='f1', set_value=15)

        # 測試 Aspen.Distillation.setNF 中 sname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_StreamTypeError,
            "Cannot Find F11 in the AspenFile. Please Check the name you type!!",
            Aspen.Distillation.setNF,
            'c1', sname='f11', set_value=15)

        # 測試 Aspen.Distillation.setNF 中 sname 非指定蒸餾塔之進料物流
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_StreamTypeError,
            "F2 is not a feed stream for C1. Please Check the name you type!!",
            Aspen.Distillation.setNF,
            'c1', sname='f2', set_value=15)

        # 測試 Aspen.Distillation.setNF 中 sname 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "sname must be a 'String'!!!",
            Aspen.Distillation.setNF,
            'c1', sname=123, set_value=15)

        # 測試 Aspen.Distillation.setNF 中 set_value 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "set_value must be a 'Integer'!!!",
            Aspen.Distillation.setNF,
            'c1', sname='f1', set_value='')

        # 測試 Aspen.Distillation.setNF 中 set_value 為負整數
        self.assertRaisesRegex(
            ValueError,
            "set_value must be a 'Positive' number!!!",
            Aspen.Distillation.setNF,
            'c1', sname='f1', set_value=-15)

    def test_getDiameter(self):
        """進行 getDiameter 函式的各種測試，測試內容如下：
        # 測試　Aspen.Distillation.getDiameter 中 bname 的功能
        # 測試　Aspen.Distillation.getDiameter 中 getunit 的功能
        # 測試　Aspen.Distillation.getDiameter 中 unitchangeto 的功能

        # 測試 Aspen.Distillation.getDiameter 的取得轉換單位後物流流量單位功能
        # 測試 Aspen.Distillation.getDiameter 中 bname 如無開啟size功能
        """
        # 測試　Aspen.Distillation.getDiameter 中 bname 的功能
        self.bname_test(Aspen.Distillation.getDiameter, 0.7259635661)

        # 測試　Aspen.Distillation.getDiameter 中 getunit 的功能
        self.getunit_test(Aspen.Distillation.getDiameter, 'meter')

        # 測試　Aspen.Distillation.getDiameter 中 unitchangeto 的功能
        self.unitchangeto_test(Aspen.Distillation.getDiameter, 2.3817702299868766, 15)

        # 測試 Aspen.Distillation.getDiameter 的取得轉換單位後物流流量單位功能
        self.assertEqual(
            Aspen.Distillation.getDiameter('c2-size', get_unit=True, unit_change_to=2),
            'ft')

        # 測試　Aspen.Distillation.getDiameter 中 bname 如無開啟size功能
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_SizingError,
            "'Sizing' function dosen't open!!!",
            Aspen.Distillation.getDiameter,
            'c1')

    def test_getHeight(self):
        """進行 getHeight 函式的各種測試，測試內容如下：
        # 測試　Aspen.Distillation.getHeight 中 bname 的功能
        # 測試　Aspen.Distillation.getHeight 中 getunit 的功能
        """
        # 測試　Aspen.Distillation.getHeight 中 bname 的功能
        self.bname_test(Aspen.Distillation.getHeight, 24.871679999999998)

        # 測試　Aspen.Distillation.getHeight 中 getunit 的功能
        self.getunit_test(Aspen.Distillation.getHeight, 'meter')

    def test_getQR(self):
        """進行 getQR 函式的各種測試，測試內容如下：
        # 測試　Aspen.Distillation.getQR 中 bname 的功能
        # 測試　Aspen.Distillation.getQR 中 getunit 的功能
        # 測試　Aspen.Distillation.getQR 中 unitchangeto 的功能

        # 測試 Aspen.Distillation.getQR 中 bname 沒有reboiler狀況
        # 測試 Aspen.Distillation.getQR 的取得轉換單位後物流流量單位功能
        """
        # 測試　Aspen.Distillation.getQR 中 bname 的功能
        self.bname_test(Aspen.Distillation.getQR, 1272.88127)

        # 測試　Aspen.Distillation.getQR 中 getunit 的功能
        self.getunit_test(Aspen.Distillation.getQR, 'kW')

        # 測試　Aspen.Distillation.getQR 中 unitchangeto 的功能
        self.unitchangeto_test(Aspen.Distillation.getQR, 4343251.175395772, 8)

        # 測試 Aspen.Distillation.getQR 中 bname 沒有reboiler狀況
        self.assertEqual(
            Aspen.Distillation.getQR('c3'),
            None)

        # 測試 Aspen.Distillation.getQR 的取得轉換單位後物流流量單位功能
        self.assertEqual(
            Aspen.Distillation.getQR('c2-size', get_unit=True, unit_change_to=2),
            'Btu/hr')

    def test_getReboilerArea(self):
        """進行 getReboilerArea 函式的各種測試，測試內容如下：
        # 測試　Aspen.Distillation.getReboilerArea 中 bname 的功能
        # 測試　Aspen.Distillation.getReboilerArea 中 getunit 的功能

        # 測試 Aspen.Distillation.getReboilerArea 中 bname 沒有reboiler狀況
        # 測試輸入 U 型態錯誤
        # 測試輸入 U 數值錯誤
        """
        # 測試　Aspen.Distillation.getReboilerArea 中 bname 的功能
        self.bname_test(Aspen.Distillation.getReboilerArea, 31.157025403571478)

        # 測試　Aspen.Distillation.getReboilerArea 中 getunit 的功能
        self.getunit_test(Aspen.Distillation.getReboilerArea, 'sqrm')

        # 測試 Aspen.Distillation.getReboilerArea 中 bname 沒有reboiler狀況
        self.assertEqual(
            Aspen.Distillation.getReboilerArea('c3'),
            None)

        # 測試輸入 U 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit must be a 'Number'!!!",
            Aspen.Distillation.getReboilerArea,
            'c2-size', Ur='')

        # 測試輸入 U 數值錯誤
        self.assertRaisesRegex(
            ValueError,
            "Ur shouldn't be equal to  or smaller than 0. Please Check the Value you Type!!!",
            Aspen.Distillation.getReboilerArea,
            'c2-size', Ur=-123)

    def test_getQC(self):
        """進行 getQC 函式的各種測試，測試內容如下：
        # 測試　Aspen.Distillation.getQC 中 bname 的功能
        # 測試　Aspen.Distillation.getQC 中 getunit 的功能
        # 測試　Aspen.Distillation.getQC 中 unitchangeto 的功能

        # 測試 Aspen.Distillation.getQC 中 bname 沒有condenser狀況
        # 測試 Aspen.Distillation.getQC 的取得轉換單位後物流流量單位功能
        """
        # 測試　Aspen.Distillation.getQC 中 bname 的功能
        self.bname_test(Aspen.Distillation.getQC, -1102.11129)

        # 測試　Aspen.Distillation.getQC 中 getunit 的功能
        self.getunit_test(Aspen.Distillation.getQC, 'kW')

        # 測試　Aspen.Distillation.getQC 中 unitchangeto 的功能
        self.unitchangeto_test(Aspen.Distillation.getQC, -3760559.8169493456, 9)

        # 測試 Aspen.Distillation.getQC 中 bname 沒有condenser狀況
        self.assertEqual(
            Aspen.Distillation.getQC('c4'),
            None)

        # 測試 Aspen.Distillation.getQC 的取得轉換單位後物流流量單位功能
        self.assertEqual(
            Aspen.Distillation.getQC('c2-size', get_unit=True, unit_change_to=2),
            'Btu/hr')

    def test_getCondenserArea(self):
        """進行 getCondenserArea 函式的各種測試，測試內容如下：
        # 測試　Aspen.Distillation.getCondenserArea 中 bname 的功能
        # 測試　Aspen.Distillation.getCondenserArea 中 getunit 的功能

        # 測試 Aspen.Distillation.getCondenserArea 中 bname 沒有Condenser狀況
        # 測試輸入 U 型態錯誤
        # 測試輸入 U 數值錯誤
        """
        # 測試　Aspen.Distillation.getCondenserArea 中 bname 的功能
        self.bname_test(Aspen.Distillation.getCondenserArea, 35.488867175587714)

        # 測試　Aspen.Distillation.getCondenserArea 中 getunit 的功能
        self.getunit_test(Aspen.Distillation.getCondenserArea, 'sqrm')

        # 測試 Aspen.Distillation.getCondenserArea 中 bname 沒有Condenser狀況
        self.assertEqual(
            Aspen.Distillation.getCondenserArea('c4'),
            None)

        # 測試輸入 U 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit must be a 'Number'!!!",
            Aspen.Distillation.getCondenserArea,
            'c2-size', Uc='')

        # 測試輸入 U 數值錯誤
        self.assertRaisesRegex(
            ValueError,
            "Uc shouldn't be equal to  or smaller than 0. Please Check the Value you Type!!!",
            Aspen.Distillation.getCondenserArea,
            'c2-size', Uc=-123)

    def test_getRefluxRatio(self):
        """進行 getRefluxRatio 函式的各種測試，測試內容如下：
        # 測試　Aspen.Distillation.setRefluxRatio 中 bname 的功能
        """
        # 測試　Aspen.Distillation.getRefluxRatio 中 bname 的功能
        self.bname_test(Aspen.Distillation.getRefluxRatio, 1.0)


class Heater_test(unittest.TestCase):
    def bname_test(self, fun, correct_value):
        # 測試 bname 輸入正常時功能正常
        self.assertEqual(
            fun('c4-con'),
            correct_value)

        # 測試輸入之 bname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "Cannot Find C11 in the AspenFile. Please Check the name you type!!",
            fun,
            'c11')
        # 測試輸入 bname 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "bname must be a 'String'!!!",
            fun,
            123)

        # 測試輸入 bname 非 Heater
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "C3-RE is not a Heater,please check the name you type!!",
            fun,
            'c3-re')

    def getunit_test(self, fun, correct_value):
        # 測試 getunit 輸入正常時功能正常
        self.assertEqual(
            fun('c4-con', get_unit=True),
            correct_value)

        # 測試輸入 getunit 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit must be a 'Boolean'!!!",
            fun,
            'c4-con', get_unit=123)

    def unitchangeto_test(self, fun, correct_value, pre):
        # 測試 unitchangeto 輸入正常時功能正常
        self.assertAlmostEqual(
            fun('c4-con', unit_change_to=2),
            correct_value, pre)

        # 測試輸入 unitchangeto 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit_change_to must be a 'Integer' or 'None'!!!",
            fun,
            'c4-con', unit_change_to='123')

        # 測試輸入 unitchangeto 超出內建合法值
        self.assertRaisesRegex(
            IndexError,
            'The um index is out of range !!!',
            fun,
            'c4-con', unit_change_to=1234)

    def test_getQ(self):
        """進行 getQ 函式的各種測試，測試內容如下：
        # 測試　Aspen.Heater.getQ 中 bname 的功能
        # 測試　Aspen.Heater.getQ 中 getunit 的功能
        # 測試　Aspen.Heater.getQ 中 unitchangeto 的功能

        # 測試 Aspen.Heater.getQ 的取得轉換單位後物流流量單位功能
        """
        # 測試　Aspen.Heater.getQ 中 bname 的功能
        self.bname_test(Aspen.Heater.getQ, -1102.0933)

        # 測試　Aspen.Heater.getQ 中 getunit 的功能
        self.getunit_test(Aspen.Heater.getQ, 'kW')

        # 測試　Aspen.Heater.getQ 中 unitchangeto 的功能
        self.unitchangeto_test(Aspen.Heater.getQ, -3760498.4325213656, 9)

        # 測試 Aspen.Heater.getQ 的取得轉換單位後物流流量單位功能
        self.assertEqual(
            Aspen.Heater.getQ('c4-con', get_unit=True, unit_change_to=2),
            'Btu/hr')

    def test_getArea(self):
        """進行 getArea 函式的各種測試，測試內容如下：
        # 測試 Aspen.Heater.getArea 功能正常
        # 測試 Aspen.Heater.getArea 中 get_unit 功能正常

        # 測試 Aspen.Heater.getArea 中 bname 不存在檔案中時
        # 測試 Aspen.Heater.getArea 中 bname 輸入型態錯誤
        # 測試 Aspen.Heater.getArea 中 exchanger_type 輸入錯誤
        # 測試 Aspen.Heater.getArea 中 getunit 輸入型態錯誤
        # 測試輸入 U 型態錯誤
        # 測試輸入 U 數值錯誤
        """
        # 測試 Aspen.Heater.getArea 功能正常
        self.assertEqual(
            Aspen.Heater.getArea('c4-con', exchanger_type='CONDENSER'),
            35.49062862994761)

        # 測試 Aspen.Heater.getArea 中 get_unit 功能正常
        self.assertEqual(
            Aspen.Heater.getArea('c4-con', exchanger_type='CONDENSER', get_unit=True),
            'sqrm')

        # 測試 Aspen.Heater.getArea 中 bname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "Cannot Find C11 in the AspenFile. Please Check the name you type!!",
            Aspen.Heater.getArea,
            'c11', exchanger_type='CONDENSER')

        # 測試 Aspen.Heater.getArea 中 bname 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "bname must be a 'String'!!!",
            Aspen.Heater.getArea,
            123, exchanger_type='CONDENSER')

        # 測試 Aspen.Heater.getArea 中 exchanger_type 輸入錯誤
        self.assertRaisesRegex(
            TypeError,
            "exchanger_type must be a String and one of them that 'CONDENSER', 'HEATER', 'REBOILER', and 'COOLER' !!!",
            Aspen.Heater.getArea,
            'c4-con', exchanger_type='CONDENSERR')

        # 測試 Aspen.Heater.getArea 中 getunit 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit must be a 'Boolean'!!!",
            Aspen.Heater.getArea,
            'c4-con', exchanger_type='CONDENSER', get_unit=123)

        # 測試輸入 U 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "U must be a 'Number'!!!",
            Aspen.Heater.getArea,
            'c4-con', exchanger_type='CONDENSER', U='')

        # 測試輸入 U 數值錯誤
        self.assertRaisesRegex(
            ValueError,
            "U shouldn't be equal to  or smaller than 0. Please Check the Value you Type!!!",
            Aspen.Heater.getArea,
            'c4-con', exchanger_type='CONDENSER', U=-123)


class Extractor_test(unittest.TestCase):
    def bname_test(self, fun, correct_value):
        # 測試 bname 輸入正常時功能正常
        self.assertEqual(
            fun('extower'),
            correct_value)

        # 測試輸入之 bname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "Cannot Find C11 in the AspenFile. Please Check the name you type!!",
            fun,
            'c11')
        # 測試輸入 bname 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "bname must be a 'String'!!!",
            fun,
            123)

        # 測試輸入 bname 非 Extractor
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "C3-RE is not a Extract,please check the name you type!!",
            fun,
            'c3-re')

    def getunit_test(self, fun, correct_value):
        # 測試 getunit 輸入正常時功能正常
        self.assertEqual(
            fun('extower', get_unit=True),
            correct_value)

        # 測試輸入 getunit 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit must be a 'Boolean'!!!",
            fun,
            'extower', get_unit=123)

    def test_getNStage(self):
        """進行 getNStage 函式的各種測試，測試內容如下：
        # 測試　Aspen.Extractor.setNStage 中 bname 的功能
        """
        # 測試　Aspen.Extractor.getNStage 中 bname 的功能
        self.bname_test(Aspen.Extractor.getNStage, 3)

    def test_setNStage(self):
        """進行 setNStage 函式的各種測試，測試內容如下：
       # 測試 Aspen.Extractor.setNStage 功能正常

        # 測試 Aspen.Extractor.setNStage 中 bname 不存在檔案中時
        # 測試 Aspen.Extractor.setNStage 中 bname 輸入型態錯誤
        # 測試 Aspen.Extractor.setNStage 中 set_value 輸入型態錯誤
        # 測試 Aspen.Extractor.setNStage 中 set_value 為負整數
        """
        # 測試 Aspen.Extractor.setNStage 功能正常
        origin = Aspen.Extractor.getNStage('extower')
        Aspen.Extractor.setNStage('extower', set_value=origin+1)
        self.assertEqual(Aspen.Extractor.getNStage('extower'), origin+1)
        Aspen.Extractor.setNStage('extower', set_value=origin)

        # 測試 Aspen.Extractor.setNStage 中 bname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "Cannot Find C11 in the AspenFile. Please Check the name you type!!",
            Aspen.Extractor.setNStage,
            'c11', set_value=35)

        # 測試 Aspen.Extractor.setNStage 中 bname 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "bname must be a 'String'!!!",
            Aspen.Extractor.setNStage,
            123, set_value=35)

        # 測試 Aspen.Extractor.setNStage 中 set_value 輸入型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "set_value must be a 'Integer'!!!",
            Aspen.Extractor.setNStage,
            'extower', set_value='')

        # 測試 Aspen.Extractor.setNStage 中 set_value 為負整數
        self.assertRaisesRegex(
            ValueError,
            "set_value must be a 'Positive' number!!!",
            Aspen.Extractor.setNStage,
            'extower', set_value=-3)

    def test_getDiameter(self):
        """進行 getDiameter 函式的各種測試，測試內容如下：
        # 測試　Aspen.Extractor.getDiameter 中 bname 的功能
        # 測試　Aspen.Extractor.getDiameter 中 getunit 的功能
        """
        # 測試　Aspen.Extractor.getDiameter 中 bname 的功能
        self.bname_test(Aspen.Extractor.getDiameter, 0.22195053024005312)

        # 測試　Aspen.Extractor.getDiameter 中 getunit 的功能
        self.getunit_test(Aspen.Extractor.getDiameter, 'meter')

    def test_getHeight(self):
        """進行 getHeight 函式的各種測試，測試內容如下：
        # 測試　Aspen.Extractor.getHeight 中 bname 的功能
        # 測試　Aspen.Extractor.getHeight 中 getunit 的功能
        """
        # 測試　Aspen.Extractor.getHeight 中 bname 的功能
        self.bname_test(Aspen.Extractor.getHeight, 5.486400000000001)

        # 測試　Aspen.Extractor.getHeight 中 getunit 的功能
        self.getunit_test(Aspen.Extractor.getHeight, 'meter')


class Decanter_test(unittest.TestCase):
    def bname_test(self, fun, correct_value):
        # 測試 bname 輸入正常時功能正常
        self.assertEqual(
            fun('dec'),
            correct_value)

        # 測試輸入之 bname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "Cannot Find C11 in the AspenFile. Please Check the name you type!!",
            fun,
            'c11')
        # 測試輸入 bname 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "bname must be a 'String'!!!",
            fun,
            123)

        # 測試輸入 bname 非 Decanter
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "C3-RE is not a Decanter,please check the name you type!!",
            fun,
            'c3-re')

    def getunit_test(self, fun, correct_value):
        # 測試 getunit 輸入正常時功能正常
        self.assertEqual(
            fun('dec', get_unit=True),
            correct_value)

        # 測試輸入 getunit 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "unit must be a 'Boolean'!!!",
            fun,
            'dec', get_unit=123)

    def test_getVolume(self):
        """進行 getVolume 函式的各種測試，測試內容如下：
        # 測試　Aspen.Decanter.getVolume 中 bname 的功能
        # 測試　Aspen.Decanter.getVolume 中 getunit 的功能

        # 測試輸入 Aspen.Decanter.getVolume 中 rtime 的型態錯誤
        # 測試輸入 Aspen.Decanter.getVolume 中 rtime 的數值錯誤
        # 測試輸入 Aspen.Decanter.getVolume 中 LF 的型態錯誤
        # 測試輸入 Aspen.Decanter.getVolume 中 LF 的數值錯誤
        """
        # 測試　Aspen.Decanter.getVolume 中 bname 的功能
        self.bname_test(Aspen.Decanter.getVolume, 0.9698495799999987)

        # 測試　Aspen.Extractor.getVolume 中 getunit 的功能
        self.getunit_test(Aspen.Decanter.getVolume, 'cum')

        # 測試輸入 Aspen.Decanter.getVolume 中 rtime 的型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "rtime must be a Number!!!",
            Aspen.Decanter.getVolume,
            'dec', rtime='')

        # 測試輸入 Aspen.Decanter.getVolume 中 rtime 的數值錯誤
        self.assertRaisesRegex(
            ValueError,
            "rtime should not be a negative number!!",
            Aspen.Decanter.getVolume,
            'dec', rtime=-123)

        # 測試輸入 Aspen.Decanter.getVolume 中 LF 的型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "LF must be a Number!!!",
            Aspen.Decanter.getVolume,
            'dec', LF='')

        # 測試輸入 Aspen.Decanter.getVolume 中 LF 的數值錯誤
        self.assertRaisesRegex(
            ValueError,
            "LF should not be a negative number!!",
            Aspen.Decanter.getVolume,
            'dec', LF=-123)

    def test_getDiameter(self):
        """進行 getDiameter 函式的各種測試，測試內容如下：
        # 測試　Aspen.Decanter.getDiameter 中 bname 的功能
        # 測試　Aspen.Decanter.getDiameter 中 getunit 的功能
        """
        # 測試　Aspen.Decanter.getDiameter 中 bname 的功能
        self.bname_test(Aspen.Decanter.getDiameter, 0.8515199698200184)

        # 測試　Aspen.Extractor.getDiameter 中 getunit 的功能
        self.getunit_test(Aspen.Decanter.getDiameter, 'meter')

    def test_getHeight(self):
        """進行 getHeight 函式的各種測試，測試內容如下：
        # 測試　Aspen.Decanter.getHeight 中 bname 的功能
        # 測試　Aspen.Decanter.getHeight 中 getunit 的功能

        # 測試輸入 Aspen.Decanter.getHeight 中 AR 的型態錯誤
        # 測試輸入 Aspen.Decanter.getHeight 中 AR 的數值錯誤
        """
        # 測試　Aspen.Decanter.getHeight 中 bname 的功能
        self.bname_test(Aspen.Decanter.getHeight, 1.7030399396400369)

        # 測試　Aspen.Decanter.getHeight 中 getunit 的功能
        self.getunit_test(Aspen.Decanter.getHeight, 'meter')

        # 測試輸入 Aspen.Decanter.getHeight 中 AR 的型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "AR must be a Number!!!",
            Aspen.Decanter.getHeight,
            'dec', AR='')

        # 測試輸入 Aspen.Decanter.getHeight 中 AR 的數值錯誤
        self.assertRaisesRegex(
            ValueError,
            "AR should not be a negative number!!",
            Aspen.Decanter.getHeight,
            'dec', AR=-123)


class Cost_test(unittest.TestCase):
    def bname_test(self, fun, correct_value):
        # 測試 bname 輸入正常時功能正常
        self.assertEqual(
            fun('c1'),
            correct_value)

        # 測試輸入之 bname 不存在檔案中時
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "Cannot Find C11 in the AspenFile. Please Check the name you type!!",
            fun,
            'c11')
        # 測試輸入 bname 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "bname must be a 'String'!!!",
            fun,
            123)

    def test_SteamType(self):
        """進行 SteamType 函式的各種測試，測試內容如下：
        # 測試　Aspen.Cost.SteamType 中 bname 的功能

        # 測試　Aspen.Cost.SteamType 中 bname 非指定三種block錯誤
        # 測試　Aspen.Cost.SteamType 中 bname 為RadFrac但沒有reboiler
        # 測試　Aspen.Cost.SteamType 中 bname 指定三種block但不是加熱作用錯誤
        # 測試 Aspen.Cost.SteamType 中 minDeltaT 型態錯誤
        # 測試 Aspen.Cost.SteamType 中 minDeltaT 數值錯誤
        # 測試 Aspen.Cost.SteamType 無適用蒸氣
        """
        # 測試　Aspen.Cost.SteamType 中 bname 的功能
        self.bname_test(Aspen.Cost.SteamType, 'LP')

        # 測試　Aspen.Cost.SteamType 中 bname 非指定三種block錯誤
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "C4-SPLIT is not a RadFrac or a Heater or a Flash2,please check the name you type!!",
            Aspen.Cost.SteamType,
            'c4-split')

        # 測試　Aspen.Cost.SteamType 中 bname 為RadFrac但沒有reboiler
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "The specified column doesn't have reboiler. Please check the name you type!!!",
            Aspen.Cost.SteamType,
            'c3')

        # 測試　Aspen.Cost.SteamType 中 bname 指定三種block但不是加熱作用錯誤
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "The duty of specified Heater is equal or smaller than Zero. It is no need to use steam !!!",
            Aspen.Cost.SteamType,
            'c4-con')

        # 測試 Aspen.Cost.SteamType 中 minDeltaT 型態錯誤
        self.assertRaisesRegex(
            TypeError,
            "minDeltaT must be a Number!!!",
            Aspen.Cost.SteamType,
            'c1', '')

        # 測試 Aspen.Cost.SteamType 中 minDeltaT 數值錯誤
        self.assertRaisesRegex(
            ValueError,
            "minDeltaT should not be a negative number!!",
            Aspen.Cost.SteamType,
            'c1', -20)

        # 測試 Aspen.Cost.SteamType 無適用蒸氣
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_SteamError,
            "The temperature difference between outlet stream and utility cannot match the required minimum value. Please Check your design detail !!!",
            Aspen.Cost.SteamType,
            'c1', 1000)

    def test_WaterType(self):
        """進行 WaterType 函式的各種測試，測試內容如下：
        # 測試　Aspen.Cost.WaterType 中 bname 的功能

        # 測試　Aspen.Cost.WaterType 中 bname 非指定兩種block錯誤
        # 測試　Aspen.Cost.WaterType 中 bname 為RadFrac但沒有condenser
        # 測試　Aspen.Cost.WaterType 中 bname 指定兩種block但不是冷卻作用錯誤
        # 測試 Aspen.Cost.WaterType 無適用冷卻物質
        """
        # 測試　Aspen.Cost.WaterType 中 bname 的功能
        self.bname_test(Aspen.Cost.WaterType, 'Cooling')

        # 測試　Aspen.Cost.WaterType 中 bname 非指定兩種block錯誤
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "C4-SPLIT is not a RadFrac or a Heater,please check the name you type!!",
            Aspen.Cost.WaterType,
            'c4-split')

        # 測試　Aspen.Cost.WaterType 中 bname 為RadFrac但沒有condenser
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "The specified column doesn't have condenser. Please check the name you type!!!",
            Aspen.Cost.WaterType,
            'c4')

        # 測試　Aspen.Cost.WaterType 中 bname 指定兩種block但不是冷卻作用錯誤
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_BlockTypeError,
            "The duty of specified Heater is equal or greater than Zero. It is no need to use water !!!",
            Aspen.Cost.WaterType,
            'c5-re')

        # 測試 Aspen.Cost.SteamType 無適用冷卻物質
        self.assertRaisesRegex(
            AspenPlus.UserDifineException.AspenPlus_WaterError,
            "The temperature of outlet stream may be too low. Please Check your design detail !!!",
            Aspen.Cost.WaterType,
            'cooler')
