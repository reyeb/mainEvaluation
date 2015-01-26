from evsci.util.fileConvertor import *

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

		glideConvertorInstance = fileConvertor(glide_docked_file)
		processed=glideConvertorInstance.Build_Glide()
		if processed == False:
			with open("No_glide.txt",a) as f:
				f.write(self.complex_Name+"\n")
			print "this hasn't been processed"
		else:
			print "continue proicessing"
		
	#home/t701033/data/myresults/docked_9_12_14/Gold/SMO2_1114_0001/grid1
	if run_mode ==1 or self.mode == "Gold":
		gold_docked_file=os.path.join(self.docked_Models,"Gold",self.complex_Name,"grid1")
		
		print "***Running Gold ...."

		goldConvertorInstance = fileConvertor(gold_docked_file)
		processed=goldConvertorInstance.Build_Gold(self.complex_Name,os.path.join(self.gpcr_Models,self.complex_Name+"_receptor.pdb"))
		if processed == False:
			with open("No_gold.txt",a) as f:
				f.write(self.complex_Name+"\n")
			print "this hasn't been processed"
		else:
			print "continue proicessing"



