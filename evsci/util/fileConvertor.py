import os
from prosci.util.command import *
import shutil
from prosci.util.cd import *
import shutil, errno, os
#This class is used to create the individual pdb files of the docked ligands.

class fileConvertor():

    def __init__(self, Docked_Result_Path,MODE,COMPLEXNAME=None):
	
	self.dockPath = Docked_Result_Path
	self.individualDocks_outdir=os.path.join(self.dockPath,"individualModels")
	if MODE=="Glide" or MODE=="Gold":
		self.Program_path = Command().Get_program_path("maestro").replace("maestro","")
	if MODE=="Vina":
		self.Program_path_Vina = Command().Get_program_path("vina_split")
		self.Program_babel = Command().Get_program_path("babel")
	self.complex_name= COMPLEXNAME

    def Build_Glide(self):
    	
    	if not os.path.exists(os.path.join(self.dockPath,"dock1_XP_pv.maegz")):
    		return False
	#if not os.path.exists(os.path.join(self.individualDocks_outdir,"dock1_XP_sorted.mae")):
    		#shutil.copyfile(os.path.join(self.dockPath,"dock1_XP_sorted.mae"), os.path.join(self.individualDocks_outdir,"dock1_XP_sorted.mae"))
        if not os.path.exists(self.individualDocks_outdir):
   		print "*****making directory", self.individualDocks_outdir
		os.mkdir(self.individualDocks_outdir) 
    	self.Run_conversion("mae","pdb",os.path.join(self.dockPath,"dock1_XP_sorted.mae"),"dock1_XP_sorted.pdb")
    	receptorFile=os.path.join(self.individualDocks_outdir,"dock1_XP_sorted-1.pdb")
    	if os.path.exists(receptorFile):
    		with cd (self.individualDocks_outdir):
    			os.rename("dock1_XP_sorted-1.pdb","receptor.pdb")

    def Build_Gold(self,complexname, receptorFilefromGPCRmodels):
	
	targetNameOnly=complexname.split("_")[0] 
	rankingTextFile=targetNameOnly+"_ligand_Prep_m1.rnk"
	#if there is no result return False
    	if not os.path.exists(os.path.join(self.dockPath,rankingTextFile)):
    		return False
    	if not os.path.exists(self.individualDocks_outdir):
   		print "*****making directory", self.individualDocks_outdir
		os.mkdir(self.individualDocks_outdir) 
    	rankedlist=self.Read_Gold_RankingFile(os.path.join(self.dockPath,rankingTextFile))
    	self.convert_Gold_files(rankedlist)
    	if not os.path.exists(os.path.join(self.individualDocks_outdir,"receptor.pdb")):
    		shutil.copyfile(receptorFilefromGPCRmodels,os.path.join(self.individualDocks_outdir,"receptor.pdb"))

    def Build_Vina(self):
    	
	alldocked_Path=os.path.join(self.dockPath,"FinalModels_1.pdbqt")
    	if not os.path.isfile(alldocked_Path):
    		return False
	#if not os.path.exists(os.path.join(self.individualDocks_outdir,"dock1_XP_sorted.mae")):
    		#shutil.copyfile(os.path.join(self.dockPath,"dock1_XP_sorted.mae"), os.path.join(self.individualDocks_outdir,"dock1_XP_sorted.mae"))
        if not os.path.isdir(self.individualDocks_outdir):
   		print "*****making directory", self.individualDocks_outdir
		os.mkdir(self.individualDocks_outdir) 
	self.Split_Vina_files(alldocked_Path)
	self.Vina_Select_receptor()
    	self.convert_Vina_files()
	
    

    def Read_Gold_RankingFile(self,address):
    	ranklist=[]
    	with open (address) as f:
    		content=f.readlines()
    	for l in content:
    		line = l.rstrip()
    		if line:
	    		parts=line.split()
	    		if self.RepresentsInt(parts[0]):
	    			ranklist.append(parts[0])
    	return ranklist

    def Vina_Select_receptor(self):
	receptorPath=self.dockPath.replace("grid1","")
	receptor_file=os.path.join(receptorPath,self.complex_name+"_receptor_Prep.pdbqt")
	dst=os.path.join(self.individualDocks_outdir,self.complex_name+"_receptor_Prep.pdbqt")
	#print "**",dst,receptor_file
	self.copyanything(receptor_file, dst)

    def Split_Vina_files(self,inputFile):
	dst=os.path.join(self.individualDocks_outdir,"FinalModels_1.pdbqt")
	self.copyanything(inputFile, dst)
	with cd (self.individualDocks_outdir):
		arguments=[self.Program_path_Vina ,"--input", dst]
		Command().Process_Command(arguments," ", "Splitting files")
		os.remove(dst)

    def convert_Vina_files(self):
	# babel -ipdbqt 5HT1B_2128_0002_receptor_Prep.pdbqt -opdb 5HT1B_2128_0002_receptor_Prep.pdb
	allFiles=os.listdir(self.individualDocks_outdir)   		
    	for fileName in allFiles:
		outfile=fileName.replace(".pdbqt",".pdb")
		with cd (self.individualDocks_outdir):
			arguments=[self.Program_babel ,"-ipdbqt", fileName,"-opdb",outfile]
			Command().Process_Command(arguments," ", "Converting files")
			os.remove(fileName)
    			
    def convert_Gold_files(self,ranklist): 
    	allFiles=os.listdir(self.dockPath)   		
    	
    	for fileName in allFiles:
    		if fileName.endswith(".sdf") and not fileName.startswith("ranked"):
    			parts= fileName.split("_")
    			soln_number = parts[-1].replace(".sdf","")
    			index=ranklist.index(soln_number)
    			#print soln_number,index
    			newname="gold_sorted_"+str(index+1)+".pdb"
    			self.Run_conversion("sd","pdb",os.path.join(self.dockPath,fileName),newname)
    			#break

    def Run_conversion(self,in_ex,out_ex,in_filename,out_filename):
    	
        with cd (self.individualDocks_outdir):
    		mainExecutablePath = os.path.join(self.Program_path,"utilities/structconvert")
		print "*****cd to",self.individualDocks_outdir
		arguments=[mainExecutablePath,"--i"+in_ex, in_filename , "-o"+out_ex, out_filename]
		Command().Process_Command(arguments," ", "Converting Formats")
		
    def RepresentsInt(self,s):
    	try: 
       		int(s)
        	return True
    	except ValueError:
        	return False


 
    def copyanything(self,src, dst):
    	try:
		shutil.copytree(src, dst)
    	except OSError as exc:
		if exc.errno == errno.ENOTDIR:
		    shutil.copy(src, dst)
		else: raise

