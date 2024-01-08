import sys
import ESC
import time

HateGuardVersion = "0.1.0a"
HateGuardDate = "10.01.2023"

ESC.CLS()

ESC.TxtBold(True)
ESC.SetForeGround(ESC.Solarized16.Base3)
print( "  H a t e G u a r d - CLI", end="")
ESC.TxtBold(False)
ESC.SetForeGround(ESC.Solarized16.Base2)
print( " v" + HateGuardVersion, end="")
print( " (" + HateGuardDate + ") ", end="")
ESC.SetForeGround(ESC.Solarized16.Base02)
print( "by https://github.com/PitWD/HateGuard")
ESC.ResetForeGround()


