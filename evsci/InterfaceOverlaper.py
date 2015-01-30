import os
from GetLigandInterface import *
#from prosci.util.command import *
#import shutil
#from prosci.util.cd import *


class InterfaceOverlaper():

    def __init__(self, Docked_Result_Path,NATIVE,COMPLEXNAME):
	
	self.dockPath = Docked_Result_Path
	self.native=NATIVE
	self.complex_Name = COMPLEXNAME
	self.individualDocks_outdir=os.path.join(self.dockPath,"individualModels")
	self.outputfile= os.path.join("/work/cadd1/u049808/reyhaneh/myresults/evaluation/docked_9_12_14","overlapScores")
	#self.mode=MODE

    def Prepare_Output_File():
    	heading_str = "\t".join(("complex_Name","dock_file_name","%Residue_overlapScore","%Residue-ligAtom_Pair_overlapScore"))
    	with open(self.outputfile,"w") as f:
    		f.write(heading_str+"\n") 
	
    def Get_overlap_Score(self):
    	#First Fill in the dic for the native files
    	self.Get_native_Residue()
    	self.Get_docked_Residue()
    	
    def Get_docked_Residue(self):
    	allFiles=os.listdir(self.individualDocks_outdir)
    	receptorFile=os.path.join(self.individualDocks_outdir,"receptor.pdb")
    	for dockFile in allFiles:
    		if dockFile != "receptor.pdb":
    			
    			ligandFile=os.path.join(self.individualDocks_outdir,dockFile)
    			dockedResidueList,dockedPairlist=Get_interface_residues (receptorFile,ligandFile,"A")
    			
    			dockedmodelName=self.complex_Name.split("_")[0]
    			nativeResidueList= self.nativedic[dockedmodelName][0]["residueList"]
    			nativePairList= self.nativedic[dockedmodelName][0]["pairlist"]
     			#print a[0]["residueList"]
    			#print residueList,pairlist
    			residue_overlapScore = self.Calculate_overlap_Score( dockedResidueList, nativeResidueList)
			pair_overlapScore = self.Calculate_overlap_Score( dockedPairlist, nativePairList)
			#print dockedPairlist[0],nativePairList[0]
			overlap_str = "\t".join((self.complex_Name,rdockFile,esidue_overlapScore,pair_overlapScore))
			with open (self.outputfile,"a") as f:
				f.write(overlap_str +"\n")
    			#break

    def Get_native_Residue(self):
    	allFiles=os.listdir(self.native)
    	self.nativedic= defaultdict(list)
    	for nfile in allFiles:
    		if nfile.endswith("_receptor.pdb"):
    			#print nfile
    			receptorFile=os.path.join(self.native,nfile)
    			ligandFile=os.path.join(self.native,nfile.replace("receptor","ligand"))
    			residueList,pairlist=Get_interface_residues (receptorFile,ligandFile,"A")
     			#print residueList#,pairlist
     			name=nfile.split("_")[0]
     			#print name
     			self.nativedic[name].append({"residueList":residueList,"pairlist":pairlist})
     			#a= self.nativedic["SMO2"]#["residueList"]
     			#print a[0]["residueList"]
    			#break   			
    			
    def Calculate_overlap_Score(self, dockedList, nativeList):
    	similarities = set(nativeList) & set(dockedList)
    	#print "score", len(similarities)/float(len(nativeList))
    	#print "lensim,native",len(similarities),len(nativeList)
    	#print "len diff",len(list(set(nativeList) - set(dockedList)))
    	overlap_score= "{0:.2f}".format(len(similarities)/float(len(nativeList))*100)
    	return overlap_score

    	
    	
