

def Visio(master, visio_path):
    ## 將重要模組匯入為Visio類別的屬性
    from .Basic import Visio
    from . import AspenConnector

    V = Visio(master, visio_path)
    V.AspenConnector = AspenConnector.AspenConnector(V)

    return V
