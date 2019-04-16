import pyAspenPlus
import pyAspenPlus.Visio as Visio
import os
import time

if __name__=="__main__":
    # 先開啟AspenFile
    aspen_path = os.path.join(os.path.abspath('.'), "TestFile", "DistillationColumn.apw")
    path_visio = os.path.join(os.path.abspath('.'), "TestFile/TextFile/Visio_test.vsdx")
    Aspen = pyAspenPlus.AP(aspen_path)
    Visio = Visio.Visio(Aspen, path_visio)

    Visio.Show(True)

    Visio.AspenConnector.join_stream(aspen_name='f2', visio_name='F2',
                                     component=['BENZENE', 'WATER'],
                                     effdg=[1, 2, 1, 3])
    Visio.AspenConnector.join_cooled_duty(aspen_name='c2-size',
                                          visio_name='QCo2',
                                          effdg=1)
    Visio.AspenConnector.join_cooled_duty(aspen_name='COOLER',
                                          visio_name='QC1',
                                          effdg=1)
    Visio.AspenConnector.join_heat_duty(aspen_name='c2-size',
                                        visio_name='QR2',
                                        effdg=1)
    Visio.AspenConnector.join_distillation_data(aspen_name='c2-size',
                                                visio_name='C2-Size',
                                                effdg=[2, 2])
    Visio.AspenConnector.join_distillation_data(aspen_name='c6',
                                                visio_name='C6',
                                                effdg=[2, 2])
    Visio.AspenConnector.join_extractor_data(aspen_name='extower',
                                             visio_name='Extractor',
                                             solvent='sol',
                                             feed='ff1',
                                             effdg=[2, 2])

    Aspen.Close()
