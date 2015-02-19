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
from prosci.util.command import *
import re

class rmsdCalculator():

    def __init__(self, Docked_Result_Path,NATIVE,COMPLEXNAME,OUTPUTFolder,COMPETITIOMODEL=None):
	
	self.dockPath = Docked_Result_Path
	self.native=NATIVE
	self.complex_Name = COMPLEXNAME
	if self.dockPath is not None:
		self.individualDocks_outdir=os.path.join(self.dockPath,"individualModels")
	self.outputfile= os.path.join(OUTPUTFolder,"rmsdScores")
	self.competitionModelFile=COMPETITIOMODEL
	self.Prepare_Output_File()
	#self.mode=MODE
	self.Program_path = Command().Get_program_path("maestro").replace("maestro","")
	self.mainExecutablePath = os.path.join(self.Program_path,"run")
	
    def Prepare_Output_File(self):
	if not os.path.exists(self.outputfile):
    		heading_str = "\t".join(("complex_Name","dock_file_name","rmsd_native_dock_ligand"))
    		with open(self.outputfile,"w") as f:
    			f.write(heading_str+"\n")

    def Get_RMSD_Score(self):
    	try:
    		self.Get_native_data()
    		rmsddic=None
    		if self.dockPath is not None:
    			rmsddic= self.Get_all_RMSD_Score()
    		competitionrmsd=None
    		if self.competitionModelFile is not None:
    			competitionrmsd=self.Get_competition_Rmsd()
    		return rmsddic,competitionrmsd
    	
    	except Exception,err:
    		print str(err)
    		#raise Exception('failed to process rmsd',str(err))

    def Get_competition_Rmsd(self):
    	receptorFile=os.path.join(self.competitionModelFile,self.complex_Name+"_receptor.pdb")
    	ligandFile=os.path.join(self.competitionModelFile,self.complex_Name+"_ligand.pdb")
    	docked_rec_pdb=Pdb(receptorFile)
    	rmsd=self.Calcualte_rmsd(ligandFile,docked_rec_pdb)
    	return rmsd
    	
    def Get_native_data(self):
    	dockedmodelName=self.complex_Name.split("_")[0]
    	with cd (self.native):
    		n_rec_name=glob.glob(dockedmodelName+'*_receptor.pdb')
    		
    		n_lig_name=glob.glob(dockedmodelName+'*_ligand.pdb')
    	#print "*********",n_rec_name,n_lig_name
    	
    	self.n_lig_file=os.path.join(self.native,n_lig_name[0])
    	n_rec_file=os.path.join(self.native,n_rec_name[0])
	self.native_rec_pdb=Pdb(n_rec_file)
	self.native_lig_pdb=Pdb(self.n_lig_file).ligands
	    	
    		
    def Get_all_RMSD_Score(self):
   	print "Calculating ligand score: "
   	resultDic=dict()
	allFiles=os.listdir(self.individualDocks_outdir)
	docked_ReceptorFile=os.path.join(self.individualDocks_outdir,"receptor.pdb")
	docked_rec_pdb=Pdb(docked_ReceptorFile)

	allFiles.sort()
	
	for dockFile in allFiles:
    		if "receptor" not in dockFile and "superposed" not in dockFile:
			print dockFile
			dligandFile=os.path.join(self.individualDocks_outdir,dockFile)
			rmsd=self.Calcualte_rmsd(dligandFile,docked_rec_pdb)
			#print "Ligand docked vs Native RMSD:", rmsd
			final_rmsd="{0:.2f}".format(rmsd)
			overlap_str = "\t".join((self.complex_Name,dockFile,final_rmsd))
			with open (self.outputfile,"a") as f:
				f.write(overlap_str +"\n")
			resultDic[dockFile]= rmsd

			

			#with cd (self.ouPutDir): 


			#trans_lig_path=dligandFile.replace(".pdb","native_superposed.pdb")
			#write_file(trans_lig_path, str(sorted_native_lig_pdb))
			#print "files in: ",trans_lig_path
			#trans_rec_path=docked_ReceptorFile.replace(".pdb","_superposed.pdb")
			#write_file(trans_rec_path, str(docked_rec_pdb))
			#break
    	return resultDic
	
	#self.transformedStruc=copy.deepcopy(currentmodel)    

    	#for dockFile in allFiles:
    		#if dockFile != "receptor.pdb":
    			#ligandFile=os.path.join(self.individualDocks_outdir,dockFile)
    	#import pdb; pdb.set_trace()
    
    def Calcualte_rmsd(self,dligandFile,docked_rec_pdb):
	
	docked_lig_pdb=Pdb(dligandFile).ligands
	transform, alignment_info = tmalign_objects(docked_rec_pdb,self.native_rec_pdb, "")
	oldlig = copy.deepcopy(docked_lig_pdb)
	transform_structure(docked_lig_pdb, transform)
	#print "Ligand RMSD:", rmsd_static(self.SortLigandbyAtomName(docked_lig_pdb), self.SortLigandbyAtomName(oldlig), atom_types=None)
	#print native_lig_pdb
	#print "*"*80
	sorted_native_lig_pdb=self.SortLigandbyAtomName(self.native_lig_pdb)
	sorted_docked_lig_pdb=self.SortLigandbyAtomName(docked_lig_pdb)
	#myrmsd = rmsd_static(sorted_docked_lig_pdb, sorted_native_lig_pdb, atom_types=None)
	
	trans_lig_path=dligandFile.replace(".pdb","_superposed.pdb")
	#if not os.path.isfile(trans_lig_path): 
	#print "write supeposition"
	write_file(trans_lig_path, str(sorted_docked_lig_pdb))
	
	arguments=[self.mainExecutablePath,"rmsd.py","-use_neutral_scaffold", self.n_lig_file, trans_lig_path]
	rmnsdLine=Command().Process_Command(arguments," ","Get RMSD btw docked and native ligand.")
	rmsd=self.GetrmsdFromLine(rmnsdLine)
	
	#print "python /home/model/schrodinger.2014-4/mmshare-v28013/python/common/rmsd.py -use_neutral_scaffold "+self.n_lig_file+" "+ trans_lig_path
	
	#os.system("python /home/model/schrodinger.2014-4/mmshare-v28013/python/common/rmsd.py -use_neutral_scaffold "+self.n_lig_file+" "+ trans_lig_path)
	
	return rmsd

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

    	
    def GetrmsdFromLine(self,rmsdLine):    	
    	#parts=rmsdLine.split()
    	print rmsdLine
    	m = re.search('In-place RMSD = (.+?);', rmsdLine)
    	if m:
    		rmsd = m.group(1)
    	else:
    		rmsd=1000
    	return float(rmsd)
    	
