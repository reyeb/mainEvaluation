from argparse import ArgumentParser
import ntpath
import os
from main import *


#python evaluator.py -ligand /home/t701033/data/docking/test/input/5HT2B_1106_0001_ligand.pdb -receptor /home/t701033/data/docking/test/input/5HT2B_1106_0001_receptor.pdb -outDirectory /home/t701033/data/docking/test -mode Glide 

#python evaluator.py -receptor 5HT1B_2128_0002_receptor.pdb -dockedResultpath /work/cadd1/u049808/reyhaneh/myresults/temp/dockedmodels -nativeFiles /work/cadd1/u049808/reyhaneh/mydata/GPCR2013/native_struc/SplittedChains -gpcrModelsPath /home/t701033/GPCR2013_models -mode Glide 

#-receptor give this so we can read the complex name and something to do bash run
#result path /work/cadd1/u049808/reyhaneh/myresults/docked_9_12_14
#native file path /work/cadd1/u049808/reyhaneh/mydata/GPCR2013/native_struc/SplittedChains
#model path /home/t701033/GPCR2013_models
argparser = ArgumentParser()

argparser.add_argument("-dockedResultpath", dest = "d", nargs = "*", help = "docked model path", type = str)
argparser.add_argument("-nativeFiles", dest = "n", nargs = "*", help = "native path", type = str)
argparser.add_argument("-gpcrModelsPath", dest = "m", nargs = "*", help = "gpcr models", type = str)
argparser.add_argument("-receptor", dest = "r", nargs = "*", help = "receptor_address", type = str)
argparser.add_argument("-outDirectory", dest = "o", nargs = "*", help = "outputdir", type = str)
argparser.add_argument('-mode', dest = "mode", choices=['Gold', 'Glide','Vina','all'])


args = argparser.parse_args()

if args.d:
	dockedModels_dir =args.d[0]
else:
	raise IOError("Enter dockedResultpath address")

if args.n:
	NativeFiles_dir=args.n[0]
else:
	raise IOError("Enter nativeFiles address")



if args.m:
	gpcrModels_dir=args.m[0]
else:
	raise IOError("Enter gpcrModelsPath location")

if args.o:
	ouput_dir =args.o[0]

if not os.path.exists(dockedModels_dir):
   raise IOError("Couldn't locate the dockedModels dir")

if not os.path.exists(NativeFiles_dir):
   raise IOError("Couldn't locate the NativeFiles die")

if not os.path.exists(ouput_dir):
   print "making directory", ouput_dir
   os.mkdir(ouput_dir)

if args.r:
    complexname=args.r[0].replace('_receptor.pdb',"")

	
main(dockedModels_dir,NativeFiles_dir,gpcrModels_dir,complexname,args.mode,ouput_dir).Run_Dock()
#print("--- %s seconds ---" % str(time.time() - start_time))


