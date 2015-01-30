import os
import copy
from GetLigandInterface import *
import glob
from prosci.util.pdb import Pdb
#from prosci.util.command import *
#import shutil
from prosci.util.cd import *
from prosci.util.tmalign import tmalign_objects,transform_structure
from prosci.common import write_file
from prosci.util.pdb3d import rmsd_static
import collections

class rmsdCalculator():

    def __init__(self, Docked_Result_Path,NATIVE,COMPLEXNAME):
	
	self.dockPath = Docked_Result_Path
	self.native=NATIVE
	self.complex_Name = COMPLEXNAME
	self.individualDocks_outdir=os.path.join(self.dockPath,"individualModels")
	self.outputfile= os.path.join("/work/cadd1/u049808/reyhaneh/myresults/evaluation/docked_9_12_14","overlapScores")
	#self.mode=MODE

    def Prepare_Output_File(self):
        allFiles=os.listdir(self.individualDocks_outdir)
    	docked_ReceptorFile=os.path.join(self.individualDocks_outdir,"receptor.pdb")
    	
    	dockedmodelName=self.complex_Name.split("_")[0]
    	with cd (self.native):
    		n_rec_name=glob.glob(dockedmodelName+'*_receptor.pdb')
    		
    		n_lig_name=glob.glob(dockedmodelName+'*_ligand.pdb')
    	print "*********",n_rec_name,n_lig_name
    	
    	n_lig_file=os.path.join(self.native,n_lig_name[0])
    	n_rec_file=os.path.join(self.native,n_rec_name[0])
    	
	docked_rec_pdb=Pdb(docked_ReceptorFile)
	native_rec_pdb=Pdb(n_rec_file)
	native_lig_pdb=Pdb(n_lig_file).ligands
	print n_rec_file
	print n_lig_file
	for dockFile in allFiles:
    		if dockFile != "receptor.pdb":
    			#pymol dock1_XP_sorted-2_superposed.pdb receptor_superposed.pdb receptor.pdb dock1_XP_sorted-2.pdb /work/cadd1/u049808/reyhaneh/mydata/GPCR2013/native_struc/SplittedChains/5HT1B_4IAR_0001_receptor.pdb /work/cadd1/u049808/reyhaneh/mydata/GPCR2013/native_struc/SplittedChains/5HT1B_4IAR_0001_ligand.pdb

    			dligandFile=os.path.join(self.individualDocks_outdir,dockFile)
			docked_lig_pdb=Pdb(dligandFile).ligands
			transform, alignment_info = tmalign_objects(docked_rec_pdb,native_rec_pdb, "")
			oldlig = copy.deepcopy(docked_lig_pdb)
			transform_structure(docked_lig_pdb, transform)
			#print "Ligand RMSD:", rmsd_static(docked_lig_pdb, oldlig, atom_types=None)
			print native_lig_pdb
			print "*"*80
			sorted_native_lig_pdb=self.SortLigandbyAtomName(native_lig_pdb)
			sorted_docked_lig_pdb=self.SortLigandbyAtomName(docked_lig_pdb)
			print "Ligand docked vs Native RMSD:", rmsd_static(sorted_docked_lig_pdb, sorted_native_lig_pdb, atom_types=None)
			#trans_lig_path=dligandFile.replace(".pdb","_superposed.pdb")
			#write_file(trans_lig_path, str(docked_lig_pdb))
			#trans_rec_path=docked_ReceptorFile.replace(".pdb","_superposed.pdb")
			#write_file(trans_rec_path, str(docked_rec_pdb))
			break
	
	#self.transformedStruc=copy.deepcopy(currentmodel)    

    	#for dockFile in allFiles:
    		#if dockFile != "receptor.pdb":
    			#ligandFile=os.path.join(self.individualDocks_outdir,dockFile)
    	#import pdb; pdb.set_trace()

    def SortLigandbyAtomName(self,myligand):
		#reads myligand which is in Pdb format and return a Pdb fomatted, sorted by ligand atom name and H atoms removed.
		d=dict()

		alldata=myligand.data
		for a in alldata:
			if 'H' not in a.atom:
				d[a.atom]=a
		od = collections.OrderedDict(sorted(d.items()))
		result=[]
		for k, v in od.iteritems(): 
			result.append(v)
		sorted_myligand=Pdb(result).ligands
		return sorted_myligand

    	
    	
