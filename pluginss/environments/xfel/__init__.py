import time
import numpy as np
from badger import environment
from badger.interface import Interface


class Environment(environment.Environment):

    name = 'xfel'

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)

        self.pv_limits = {}
        self.update_pvs_limits()

    @staticmethod
    def list_vars():
        return [
            'XFEL.MAGNETS/MAGNET.ML/CFX.2162.T2/CURRENT.SP',
            'XFEL.MAGNETS/MAGNET.ML/CFX.2219.T2/CURRENT.SP',
            'XFEL.MAGNETS/MAGNET.ML/CFY.2177.T2/CURRENT.SP',
            'XFEL.MAGNETS/MAGNET.ML/CFY.2207.T2/CURRENT.SP',
            'XFEL.MAGNETS/MAGNET.ML/CFX.2162.T2/CURRENT.SP',
            'XFEL.MAGNETS/MAGNET.ML/CFX.2219.T2/CURRENT.SP',
            'XFEL.MAGNETS/MAGNET.ML/CFY.2177.T2/CURRENT.SP',
            'XFEL.MAGNETS/MAGNET.ML/CFY.2207.T2/CURRENT.SP',
            'XFEL.MAGNETS/MAGNET.ML/CBB.62.I1D/KICK_MRAD.SP',
            'XFEL.MAGNETS/MAGNET.ML/CIX.90.I1/KICK_MRAD.SP',
            'XFEL.MAGNETS/MAGNET.ML/CIX.95.I1/KICK_MRAD.SP',
            'XFEL.MAGNETS/MAGNET.ML/CIX.65.I1/KICK_MRAD.SP',
            'XFEL.MAGNETS/MAGNET.ML/CIX.51.I1/KICK_MRAD.SP',
            'XFEL.MAGNETS/MAGNET.ML/CIX.102.I1/KICK_MRAD.SP',
            'XFEL.MAGNETS/MAGNET.ML/CX.39.I1/KICK_MRAD.SP',
            'XFEL.MAGNETS/MAGNET.ML/BL.50I.I1/KICK_DEG.SP',
            'XFEL.MAGNETS/MAGNET.ML/BL.50II.I1/KICK_DEG.SP',
            'XFEL.MAGNETS/MAGNET.ML/CIY.92.I1/KICK_MRAD.SP',
            'XFEL.MAGNETS/MAGNET.ML/CIY.72.I1/KICK_MRAD.SP',
            'XFEL.MAGNETS/MAGNET.ML/CY.39.I1/KICK_MRAD.SP',
        ]

    # TODO: add losses
    @staticmethod
    def list_obses():
        return ['charge', 'sases', 'beam_energy', 'wavelength', 'ref_sase_signal', 'target_sase', 'target_disp']

    @staticmethod
    def get_default_params():
        return None

    def _get_vrange(self, var):
        return self.pv_limits[var]

    def _get_var(self, var):
        # TODO: update pv limits every time?
        return self.interface.get_value(var)

    def _set_var(self, var, x):
        self.interface.set_value(var, x)

    def _get_obs(self, obs):
        if obs == 'charge':
            return self.interface.get_value('XFEL.DIAG/CHARGE.ML/TORA.25.I1/CHARGE.SA1')
        elif obs == 'seses':
            try:
                sa1 = self.interface.get_value(
                    "XFEL.FEL/XGM/XGM.2643.T9/INTENSITY.SA1.SLOW.TRAIN")
            except:
                sa1 = None
            try:
                sa2 = self.interface.get_value(
                    "XFEL.FEL/XGM/XGM.2595.T6/INTENSITY.SLOW.TRAIN")
            except:
                sa2 = None
            try:
                sa3 = self.interface.get_value(
                    "XFEL.FEL/XGM/XGM.3130.T10/INTENSITY.SA3.SLOW.TRAIN")
            except:
                sa3 = None
            return [sa1, sa2, sa3]
        elif obs == 'beam_energy':
            try:
                tld = self.interface.get_value(
                    "XFEL.DIAG/BEAM_ENERGY_MEASUREMENT/TLD/ENERGY.DUD")
            except:
                tld = None
            #t3 = self.interface.get_value("XFEL.DIAG/BEAM_ENERGY_MEASUREMENT/T3/ENERGY.SA2")
            #t4 = self.interface.get_value("XFEL.DIAG/BEAM_ENERGY_MEASUREMENT/T4/ENERGY.SA1")
            #t5 = self.interface.get_value("XFEL.DIAG/BEAM_ENERGY_MEASUREMENT/T5/ENERGY.SA2")
            try:
                t4d = self.interface.get_value(
                    "XFEL.DIAG/BEAM_ENERGY_MEASUREMENT/T4D/ENERGY.SA1")
            except:
                t4d = None
            try:
                t5d = self.interface.get_value(
                    "XFEL.DIAG/BEAM_ENERGY_MEASUREMENT/T5D/ENERGY.SA2")
            except:
                t5d = None
            return [tld, t4d, t5d]
        elif obs == 'wavelength':
            try:
                sa1 = self.interface.get_value(
                    "XFEL.FEL/XGM.PHOTONFLUX/XGM.2643.T9/WAVELENGTH")
            except:
                sa1 = None
            try:
                sa2 = self.interface.get_value(
                    "XFEL.FEL/XGM.PHOTONFLUX/XGM.2595.T6/WAVELENGTH")
            except:
                sa2 = None
            try:
                sa3 = self.interface.get_value(
                    "XFEL.FEL/XGM.PHOTONFLUX/XGM.3130.T10/WAVELENGTH")
            except:
                sa3 = None
            return [sa1, sa2, sa3]
        elif obs == 'ref_sase_signal':
            try:
                sa1 = self.interface.get_value(
                    "XFEL.FEL/XGM/XGM.2643.T9/INTENSITY.SA1.SLOW.TRAIN")
            except:
                sa1 = None
            try:
                sa2 = self.interface.get_value(
                    "XFEL.FEL/XGM/XGM.2595.T6/INTENSITY.SLOW.TRAIN")
            except:
                sa2 = None
            # try:
            #    sa3 = self.interface.get_value("XFEL.FEL/XGM.PHOTONFLUX/XGM.3130.T10/WAVELENGTH")
            # except:
            #    sa3 = None
            return [sa1, sa2]
        elif obs == 'target_sase':
            bpms = [
                "XFEL.DIAG/BPM/BPME.2252.SA2/X.ALL",
                "XFEL.DIAG/BPM/BPME.2258.SA2/X.ALL",
                "XFEL.DIAG/BPM/BPME.2264.SA2/X.ALL",
            ]

            orbit1 = self.read_bpms(bpms=bpms, nreadings=7)
            orbit2 = np.zeros(len(bpms))  # just [0, 0, 0, ... ]
            target = np.sqrt(np.sum((orbit2 - orbit1) ** 2))

            return target
        elif obs == "target_disp":
            bpms = ["XFEL.DIAG/BPM/BPMA.59.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.72.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.75.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.77.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.80.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.82.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.85.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.87.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.90.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.92.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMF.95.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMC.134.L1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.117.I1/X.ALL",
                    "XFEL.DIAG/BPM/BPMC.158.L1/X.ALL",
                    "XFEL.DIAG/BPM/BPMA.179.B1/X.ALL"]
            Vinit = self.interface.get_value("XFEL.RF/LLRF.CONTROLLER/CTRL.A1.I1/SP.AMPL")
            orbit1 = self.read_bpms(bpms=bpms, nreadings=7)

            time.sleep(0.1)
            self.interface.set_value("XFEL.RF/LLRF.CONTROLLER/CTRL.A1.I1/SP.AMPL", Vinit - 2)
            time.sleep(0.9)

            orbit2 = self.read_bpms(bpms=bpms, nreadings=7)

            self.interface.set_value("XFEL.RF/LLRF.CONTROLLER/CTRL.A1.I1/SP.AMPL", Vinit)
            time.sleep(0.9)

            target = -np.sqrt(np.sum((orbit2 - orbit1)**2))
            return target

    def read_bpms(self, bpms, nreadings):
        orbits = np.zeros((nreadings, len(bpms)))
        for i in range(nreadings):
            for j, bpm in enumerate(bpms):
                orbits[i, j] = self.interface.get_value(bpm)
            time.sleep(0.1)
        return np.mean(orbits, axis=0)

    def update_pv_limits(self, eid):
        self.pv_limits[eid] = (0, 1)

    def update_pvs_limits(self):
        for eid in self.list_vars():
            self.update_pv_limits(eid)
