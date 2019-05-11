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
    # # Example
    # Visio.AspenConnector.join_stream(aspen_name='f2', visio_name='F2',
    #                                  component=['BENZENE', 'WATER'],
    #                                  effdg=[1, 2, 1, 3])
    # Visio.AspenConnector.join_cooled_duty(aspen_name='c2-size',
    #                                       visio_name='QCo2',
    #                                       effdg=1)
    # Visio.AspenConnector.join_cooled_duty(aspen_name='COOLER',
    #                                       visio_name='QC1',
    #                                       effdg=1)
    # Visio.AspenConnector.join_heat_duty(aspen_name='c2-size',
    #                                     visio_name='QR2',
    #                                     effdg=1)
    # Visio.AspenConnector.join_distillation_data(aspen_name='c2-size',
    #                                             visio_name='C2-Size',
    #                                             effdg=[2, 2])
    # Visio.AspenConnector.join_distillation_data(aspen_name='c6',
    #                                             visio_name='C6',
    #                                             effdg=[2, 2])
    # Visio.AspenConnector.join_extractor_data(aspen_name='extower',
    #                                          visio_name='Extractor',
    #                                          solvent='sol',
    #                                          feed='ff1',
    #                                          effdg=[2, 2])

    def draw_HED():
        ## Block
        Visio.AspenConnector.join_extractor_data(aspen_name='EXTOWER',
                                                 visio_name='Extractor',
                                                 solvent='S',
                                                 feed='FF',
                                                 effdg=[2, 2])      # [Diameter, FS/FF]
        Visio.AspenConnector.join_distillation_data(aspen_name='C1',
                                                    visio_name='STRIP1',
                                                    effdg=[3, 2])   # [Reflux Ratio, Diameter]
        Visio.AspenConnector.join_distillation_data(aspen_name='C2',
                                                    visio_name='STRIP2',
                                                    effdg=[3, 2])   # [Reflux Ratio, Diameter]

        ## Stream
        Visio.AspenConnector.join_stream(aspen_name='FF', visio_name='Fresh Feed',
                                         component=['AAOL', 'WATER'],
                                         effdg=[0, 2, 1, 3])        # [T, P, F, X]

        Visio.AspenConnector.join_stream(aspen_name='B1', visio_name='B1',
                                         component=['AAOL'],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='B2', visio_name='B2',
                                         component=['WATER'],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]

        Visio.AspenConnector.join_stream(aspen_name='V1', visio_name='V1',
                                         component=['AAOL', 'WATER', "MBE"],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='V2', visio_name='V2',
                                         component=['AAOL', 'WATER', "MBE"],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='CO2', visio_name='Mix',
                                         component=['AAOL', 'WATER', "MBE"],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='MIX3', visio_name='Mix3',
                                         component=['AAOL', 'WATER', "MBE"],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]

        Visio.AspenConnector.join_stream(aspen_name='RAFF', visio_name='Raffinate',
                                         component=['AAOL', 'WATER', "MBE"],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='S', visio_name='Solvent',
                                         component=['AAOL', 'WATER', "MBE"],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='EX', visio_name='Extract',
                                         component=['AAOL', 'WATER', "MBE"],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='AQ', visio_name='AQ',
                                         component=['AAOL', 'WATER', "MBE"],
                                         effdg=[1, 2, 1, 3])        # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='MKUP', visio_name='Makeup',
                                         component=["MBE"],
                                         effdg=[1, 2, 6, 3])        # [T, P, F, X]

        ## Duty
        Visio.AspenConnector.join_heat_duty(aspen_name='C1',
                                            visio_name='QR1',
                                            effdg=1)
        Visio.AspenConnector.join_heat_duty(aspen_name='C2',
                                            visio_name='QR2',
                                            effdg=1)
        Visio.AspenConnector.join_cooled_duty(aspen_name='Cooler1',
                                              visio_name='QC1',
                                              effdg=1)
        Visio.AspenConnector.join_cooled_duty(aspen_name='CON1',
                                              visio_name='QCo1',
                                              effdg=1)
        Visio.AspenConnector.join_cooled_duty(aspen_name='Cooler2',
                                              visio_name='QC2',
                                              effdg=1)
        Visio.AspenConnector.join_cooled_duty(aspen_name='CON2',
                                              visio_name='QCo2',
                                              effdg=1)

    def draw_3ED():
        ## Blocks
        Visio.AspenConnector.join_distillation_data(aspen_name='C1',
                                                    visio_name='C-1',
                                                    effdg=[3, 2])  # [Reflux Ratio, Diameter]
        Visio.AspenConnector.join_distillation_data(aspen_name='C2',
                                                    visio_name='C-2',
                                                    effdg=[3, 2])  # [Reflux Ratio, Diameter]
        Visio.AspenConnector.join_distillation_data(aspen_name='C3',
                                                    visio_name='C-3',
                                                    effdg=[3, 2])  # [Reflux Ratio, Diameter]

        ## Stream
        Visio.AspenConnector.join_stream(aspen_name='FF', visio_name='FF',
                                         component=['AAOL', 'WATER'],
                                         effdg=[0, 2, 1, 3])  # [T, P, F, X]

        Visio.AspenConnector.join_stream(aspen_name='B1', visio_name='B1',
                                         component=['AAOL', 'WATER', 'EG'],
                                         effdg=[1, 2, 1, 4])  # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='B2', visio_name='B2',
                                         component=['AAOL', 'WATER', 'EG'],
                                         effdg=[1, 2, 1, 4])  # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='B3', visio_name='B3',
                                         component=['AAOL', 'WATER', 'EG'],
                                         effdg=[1, 2, 1, 4])  # [T, P, F, X]

        Visio.AspenConnector.join_stream(aspen_name='D1', visio_name='D1',
                                         component=['AAOL', 'WATER', 'EG'],
                                         effdg=[1, 2, 1, 3])  # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='D2', visio_name='D2',
                                         component=['AAOL', 'WATER', 'EG'],
                                         effdg=[1, 2, 1, 3])  # [T, P, F, X]
        Visio.AspenConnector.join_stream(aspen_name='D3', visio_name='D3',
                                         component=['AAOL', 'WATER', 'EG'],
                                         effdg=[1, 2, 1, 3])  # [T, P, F, X]

        Visio.AspenConnector.join_stream(aspen_name='MKUP', visio_name='Makeup',
                                         component=['EG'],
                                         effdg=[1, 2, 4, 3])  # [T, P, F, X]

        ## Duty
        Visio.AspenConnector.join_heat_duty(aspen_name='C1',
                                            visio_name='QR1',
                                            effdg=1)
        Visio.AspenConnector.join_heat_duty(aspen_name='C2',
                                            visio_name='QR2',
                                            effdg=1)
        Visio.AspenConnector.join_heat_duty(aspen_name='C3',
                                            visio_name='QR3',
                                            effdg=1)

        Visio.AspenConnector.join_cooled_duty(aspen_name='C1',
                                              visio_name='QCo1',
                                              effdg=1)
        Visio.AspenConnector.join_cooled_duty(aspen_name='C2',
                                              visio_name='QCo2',
                                              effdg=1)
        Visio.AspenConnector.join_cooled_duty(aspen_name='C3',
                                              visio_name='QCo3',
                                              effdg=1)
        Visio.AspenConnector.join_cooled_duty(aspen_name='Cooler',
                                              visio_name='QC1',
                                              effdg=1)

    # draw_3ED()
    # draw_HED()

    Aspen.Close()
