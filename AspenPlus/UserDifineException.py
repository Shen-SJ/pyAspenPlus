class FileNotExist(Exception):
    """在電腦找不到檔案用"""
    pass

class AspenPlus_BlockTypeError(Exception):
    """Aspen單元辨認失敗用"""
    pass

class AspenPlus_StreamTypeError(Exception):
    """Aspen物流辨認失敗用"""
    pass

class AspenPlus_ComponentTypeError(Exception):
    """Aspen化合物辨認失敗用"""
    pass

class AspenPlus_SizingError(Exception):
    """Aspen的sizing未開啟"""
    pass
if __name__ == "__main__":
    raise FileNotExist