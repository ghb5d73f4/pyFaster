import sys,os

import argparse



if __name__=="__main__":
    parser = argparse.ArgumentParser(description='perform routine calibration of a channel')
    parser.add_argument('channelname', type=str,
                        nargs='?', help="Name of the channel")
    args = parser.parse_args()

    path = "./data/{0}".format(args.channelname)
    scriptpath = "./pyfaster/scripts"

    
    def oscall(command, echo=False):
        thecommand = command.format(sp=scriptpath,
                                    p=path,
                                    chan=args.channelname,
                                    py="python3") 
        if echo:
            print(thecommand)
        os.system(thecommand)

    print("#Computing the Clean rate")
    oscall("{py} {sp}/get_pileup_factor.py {p}/{chan}.counters.1d.txt > {p}/{chan}.cleanrate.txt")
    #oscall("cat {p}/{chan}.cleanrate.txt")
    print("#Guessing the slope")
    oscall("echo 122./`{py} {sp}/get_peak_positions.py --npeaks=1 --min=5000 --width=150 --min=5000 {p}/{chan}.Eclean.1d.txt | cut -d \" \" -f 1` | bc -l > {p}/{chan}.slopeguess.txt")
    oscall("cat {p}/{chan}.slopeguess.txt")
    print("# Fine calibration")
    oscall("{py} {sp}//auto-calib.py --energies=ref_egamma_152Eu.txt --offsetguess=0.0 --slopeguess=`cat {p}/{chan}.slopeguess.txt` --method=fit {p}/{chan}.Eclean.1d.txt > {p}/{chan}.autocal.txt")
    oscall("cat {p}/{chan}.autocal.txt | tail -n 2")
    print("#Calibrating")
    oscall("{py} {sp}/calibrate1D.py --slope=`cat {p}/{chan}.autocal.txt |grep slope | cut -d \"=\" -f2` --offset=`cat {p}/{chan}.autocal.txt |grep offset | cut -d \"=\" -f2` {p}/{chan}.Eclean.1d.txt > {p}/{chan}.Eclean.calibrated.1d.txt")
    oscall("{py} {sp}/Draw1Dh.py --yscale=log {p}/{chan}.Eclean.calibrated.1d.txt")
    oscall("mv -v {p}/{chan}.Eclean.calibrated.1d.txt.png {p}/{chan}.Eclean.calibrated.logy.1d.txt.png")
    for lims in [ (115, 128),
                  (240, 255),
                  (340, 352),
                  (700, 1000),
                  (1050, 1150),
                  (1390, 1425), ]:
        oscall("".join( ("{py} {sp}/Draw1Dh.py --grid ",
                         "--min={0} --max={1} ".format(*lims),
                         "{p}/{chan}.Eclean.calibrated.1d.txt")))
        oscall("".join( ("mv -v {p}/{chan}.Eclean.calibrated.1d.txt.png ",
                         "{p}/check",
                         "{0}to{1}.png".format(*lims))))
    oscall("{py} {sp}/Draw1Dh.py {p}/{chan}.Eclean.calibrated.1d.txt")
    oscall("{py} {sp}/check-152Eu.py {p}/{chan}.Eclean.calibrated.1d.txt > {p}/{chan}.152Eu-calibcheck.txt ")
    
    print("#done")
