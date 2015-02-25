from evsci.util.fileConvertor import *
from evsci.InterfaceOverlaper import InterfaceOverlaper
from evsci.rmsdCalculator import rmsdCalculator

class main():
    #main(dockedModels_dir ,NativeFiles_dir,gpcrModels_dir,complexname,args.mode)
    def __init__(self, DOCKED_Models, NATIVE_files, GPCR_Models,COMPLEXNAME, MODE, OUTPUTDir,COMPETITIONPATH):
    
	self.docked_Models = DOCKED_Models
	self.native_files = NATIVE_files
	self.gpcr_Models = GPCR_Models
	self.complex_Name = COMPLEXNAME
	self.mode = MODE
	self.mainouput_dir= OUTPUTDir
	self.competitionpath=COMPETITIONPATH



	
    def Run_Dock(self):
	
	
	#self.competitionpath="/home/t701033/GPCR2013_models"
	#self.competitionpath=None
	
	
	#if mode==all means run all docking methods
	if self.mode == 'all':
		self.run_mode=1
	else:
		self.run_mode=0
		
	
	if self.run_mode ==1 or self.mode == "Glide":
		glide_docked_file=os.path.join(self.docked_Models,"Glide",self.complex_Name,"grid1","XP")
		
		print "***Running Glide ...."
		print "Processing ",self.complex_Name
		#processed=True
		glideConvertorInstance = fileConvertor(glide_docked_file,self.mode)
		processed=glideConvertorInstance.Build_Glide()
	
		ouput_dir= os.path.join(self.mainouput_dir,"Glide")
		#ouput_dir= "/work/cadd1/u049808/reyhaneh/myresults/evaluation/docked_9_12_14/Glide"
		if not os.path.isdir(ouput_dir):
   			os.mkdir(ouput_dir)
		
		
				
		if not self.DoesResultExist(glide_docked_file):
			with open(os.path.join(self.mainouput_dir,"NoGlide"),"a") as f:
				f.write(self.complex_Name+"\n")
			
			if self.competitionpath is not None:
				
				interfaceOverlaperInstance=InterfaceOverlaper(None,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
				rmsdCalculatorInstance=rmsdCalculator(None,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)	

		else:
			interfaceOverlaperInstance=InterfaceOverlaper(glide_docked_file,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
			rmsdCalculatorInstance=rmsdCalculator(glide_docked_file,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
			
		overlapDic,competition_residue_overlapScore=interfaceOverlaperInstance.Get_overlap_Score()
		rmsdDic,competitionrmsd=rmsdCalculatorInstance.Get_RMSD_Score()	
		self.Merge_results(overlapDic,rmsdDic,ouput_dir,competitionrmsd,competition_residue_overlapScore)
		
	#home/t701033/data/myresults/docked_9_12_14/Gold/SMO2_1114_0001/grid1
	if self.run_mode ==1 or self.mode == "Gold":
		print "***Running Gold ...."
		print "Processing ",self.complex_Name
		gold_docked_file=os.path.join(self.docked_Models,"Gold",self.complex_Name,"grid1")
		
		
		goldConvertorInstance = fileConvertor(gold_docked_file,self.mode)
		#processed=goldConvertorInstance.Build_Gold(self.complex_Name,os.path.join(self.gpcr_Models,self.complex_Name+"_receptor.pdb"))
		
		#interfaceOverlaperInstance=None
		
		ouput_dir= os.path.join(self.mainouput_dir,"Gold")
		#"/work/cadd1/u049808/reyhaneh/myresults/evaluation/docked_9_12_14/Gold"
		if not os.path.isdir(ouput_dir):
   			os.mkdir(ouput_dir)
		
		if not self.DoesResultExist(gold_docked_file):
			#print "***in here1"
			with open(os.path.join(self.mainouput_dir,"NoGold"),"a") as f:
				f.write(self.complex_Name+"\n")
				
			if self.competitionpath is not None:
				#print "***in here2"
				interfaceOverlaperInstance=InterfaceOverlaper(None,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
				rmsdCalculatorInstance=rmsdCalculator(None,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
			
		else:
			#print "***in here3"
			interfaceOverlaperInstance=InterfaceOverlaper(gold_docked_file,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
			
			rmsdCalculatorInstance=rmsdCalculator(gold_docked_file,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
		
		overlapDic,competition_residue_overlapScore=interfaceOverlaperInstance.Get_overlap_Score()
		rmsdDic,competitionrmsd=rmsdCalculatorInstance.Get_RMSD_Score()
		#print competition_residue_overlapScore,competitionrmsd,rmsdDic
		self.Merge_results(overlapDic,rmsdDic,ouput_dir,competitionrmsd,competition_residue_overlapScore)

	if self.run_mode ==1 or self.mode == "Vina":
		print "***Running Vina ...."
		print "Processing ",self.complex_Name
		vina_docked_file=os.path.join(self.docked_Models,"Vina",self.complex_Name,"grid1")
		
		
		vinaConvertorInstance = fileConvertor(vina_docked_file,self.mode,self.complex_Name)
		processed=vinaConvertorInstance.Build_Vina()
		ouput_dir= os.path.join(self.mainouput_dir,"Vina")
		if not os.path.isdir(ouput_dir):
   			os.mkdir(ouput_dir)
		
		if not self.DoesResultExist(vina_docked_file):
			#print "***in here1"
			with open(os.path.join(self.mainouput_dir,"NoVina"),"a") as f:
				f.write(self.complex_Name+"\n")
				
			if self.competitionpath is not None:
				interfaceOverlaperInstance=InterfaceOverlaper(None,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
				rmsdCalculatorInstance=rmsdCalculator(None,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
			
		else:
			#print "***in here3"
			interfaceOverlaperInstance=InterfaceOverlaper(vina_docked_file,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
			
			rmsdCalculatorInstance=rmsdCalculator(vina_docked_file,self.native_files,self.complex_Name,ouput_dir,self.competitionpath)
		overlapDic,competition_residue_overlapScore=interfaceOverlaperInstance.Get_overlap_Score()
		rmsdDic,competitionrmsd=rmsdCalculatorInstance.Get_RMSD_Score()
		#print competition_residue_overlapScore,competitionrmsd,rmsdDic
		#self.Merge_results(overlapDic,rmsdDic,ouput_dir,competitionrmsd,competition_residue_overlapScore)
	

    def Merge_results(self,overlapDic,rmsdDic,ouput_dir,competitionrmsd,competition_residue_overlapScore):
	
	#print overlapDic,rmsdDic
	top_rank_key,lowest_rmsd_key,toprank_rmsd,overlap_toprank_rmsd,lowest_rmsd,overlap_lowest_rmsd=("NA",)*6
	if rmsdDic is not None:
		lowest_rmsd_key=min(rmsdDic, key=rmsdDic.get)
		lowest_rmsd="{0:.2f}".format(rmsdDic[lowest_rmsd_key])
		overlap_lowest_rmsd=overlapDic[lowest_rmsd_key]
	
		top_rank_key=""
		if self.mode == "Gold":
			top_rank_key="gold_sorted_1.pdb"
		if self.mode== "Glide":
			top_rank_key="dock1_XP_sorted-2.pdb"
	
		toprank_rmsd="{0:.2f}".format(rmsdDic[top_rank_key])
		overlap_toprank_rmsd=overlapDic[top_rank_key]
	
	if competitionrmsd is not None:
		competitionrmsd="{0:.2f}".format(competitionrmsd)
	else:
		competitionrmsd="NA"
		competition_residue_overlapScore="NA"
	
	outputfile=os.path.join(ouput_dir,"GeneralScores_"+self.mode)
	if not os.path.exists(outputfile):
    		heading_str = "\t".join(("complex_Name","topRank","bestRMSD","topRankRmsd","%topRankResidue_overlapScore","bestRmsd","%bestRmsdResidue_overlapScore","competition_model_RMSD","competition_overlapScore"))
    		with open(outputfile,"w") as f:
    			f.write(heading_str+"\n")
    		 
    	
    		
	re_str = "\t".join((self.complex_Name,top_rank_key,lowest_rmsd_key,toprank_rmsd,overlap_toprank_rmsd,lowest_rmsd,overlap_lowest_rmsd,competitionrmsd,competition_residue_overlapScore))
	with open (outputfile,"a") as f:
		f.write(re_str +"\n")
	print "ouput in: ",outputfile
	
    def DoesResultExist(self,docked_Result_Path):	
	
	if self.run_mode ==1 or self.mode == "Glide":
		if not os.path.exists(os.path.join(docked_Result_Path,"dock1_XP_pv.maegz")):
    			return False
    		else:
    			return True
    	
	if self.run_mode ==1 or self.mode == "Vina":
		if not os.path.exists(os.path.join(docked_Result_Path,"FinalModels_1.pdbqt")):
    			return False
    		else:
    			return True
    	
    	if self.run_mode ==1 or self.mode == "Gold":
		targetNameOnly=self.complex_Name.split("_")[0] 
		rankingTextFile=targetNameOnly+"_ligand_Prep_m1.rnk"
		#if there is no result return False
    		if not os.path.exists(os.path.join(docked_Result_Path,rankingTextFile)):
    			return False
    		else:
    			return True
	
	return None
	
	
	
	
