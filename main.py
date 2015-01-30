from evsci.util.fileConvertor import *
from evsci.InterfaceOverlaper import InterfaceOverlaper
from evsci.rmsdCalculator import rmsdCalculator

class main():
    #main(dockedModels_dir ,NativeFiles_dir,gpcrModels_dir,complexname,args.mode)
    def __init__(self, DOCKED_Models, NATIVE_files, GPCR_Models,COMPLEXNAME, MODE):
    
	self.docked_Models = DOCKED_Models
	self.native_files = NATIVE_files
	self.gpcr_Models = GPCR_Models
	self.complex_Name = COMPLEXNAME
	self.mode = MODE



	
    def Run_Dock(self):
		
	#if mode==all means run all docking methods
	if self.mode == 'all':
		run_mode=1
	else:
		run_mode=0
		
	
	if run_mode ==1 or self.mode == "Glide":
		glide_docked_file=os.path.join(self.docked_Models,"Glide",self.complex_Name,"grid1","XP")
		
		print "***Running Glide ...."
		processed=True
		glideConvertorInstance = fileConvertor(glide_docked_file)
		#processed=glideConvertorInstance.Build_Glide()
		if processed == False:
			with open("/home/t701033/data/mycodes/bashCodes/No_glide.txt","a") as f:
				f.write(self.complex_Name+"\n")
			print "this hasn't been processed"
		else:
			print "continue proicessing"
			#interfaceOverlaperInstance=InterfaceOverlaper(glide_docked_file,self.native_files,self.complex_Name)
			#interfaceOverlaperInstance.Get_overlap_Score()
			rmsdCalculatorInstance=rmsdCalculator(glide_docked_file,self.native_files,self.complex_Name)
			rmsdCalculatorInstance.Prepare_Output_File()
		
	#home/t701033/data/myresults/docked_9_12_14/Gold/SMO2_1114_0001/grid1
	if run_mode ==1 or self.mode == "Gold":
		gold_docked_file=os.path.join(self.docked_Models,"Gold",self.complex_Name,"grid1")
		
		print "***Running Gold ...."

		goldConvertorInstance = fileConvertor(gold_docked_file)
		processed=goldConvertorInstance.Build_Gold(self.complex_Name,os.path.join(self.gpcr_Models,self.complex_Name+"_receptor.pdb"))
		if processed == False:
			with open("/home/t701033/data/mycodes/bashCodes/No_gold.txt","a") as f:
				f.write(self.complex_Name+"\n")
			print "this hasn't been processed"
		else:
			print "continue proicessing"



