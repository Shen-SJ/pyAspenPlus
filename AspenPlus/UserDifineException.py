class FileNotExist(Exception):
    """在電腦找不到檔案用"""
    pass

class AspenPlus_FileStatusError(Exception):
    """AspenFile狀態辨認錯誤"""
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

class AspenPlus_SteamError(Exception):
    """Steam使用上有問題，像是: 連HP可能都不太能使用的情況"""
    pass

class AspenPlus_WaterError(Exception):
    """Water使用上有問題，像是: 連Chill water可能都不太能使用的情況"""
    pass
if __name__ == "__main__":
    raise FileNotExist