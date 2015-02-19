import os
from GetLigandInterface import *
#from prosci.util.command import *
#import shutil
#from prosci.util.cd import *


class InterfaceOverlaper():

    def __init__(self, Docked_Result_Path,NATIVE,COMPLEXNAME,OUTPUTFolder,COMPETITIOMODEL=None):
	
	self.dockPath = Docked_Result_Path
	self.native=NATIVE
	self.complex_Name = COMPLEXNAME
	#if self.dockPath is not None:
		#print "i am not None"
	if self.dockPath is not None:
		self.individualDocks_outdir=os.path.join(self.dockPath,"individualModels")
	self.outputfile= os.path.join(OUTPUTFolder,"overlapScores")
	self.competitionModelFile=COMPETITIOMODEL
	self.Prepare_Output_File()
	
	#self.mode=MODE

    def Prepare_Output_File(self):
	if not os.path.exists(self.outputfile):
    		heading_str = "\t".join(("complex_Name","dock_file_name","%Residue_overlapScore","%Residue-ligAtom_Pair_overlapScore"))
    		with open(self.outputfile,"w") as f:
    			f.write(heading_str+"\n") 
	
    def Get_overlap_Score(self):
    	try:
    		#First Fill in the dic for the native files
    		print "start calculating overlap score: "
    		self.Get_native_Residue()
    		
    		competition_residue_overlapScore=None
    		if self.competitionModelFile is not None:
    			competition_residue_overlapScore=self.Get_competition_Model()
		docked_overlap_scores=None
		if self.dockPath is not None:
    			docked_overlap_scores= self.Get_docked_Residue()
    		return docked_overlap_scores,competition_residue_overlapScore
    			
    			
    	except Exception,err:
    		print str(err)
    		#raise Exception('failed to process overlap',str(err))
    	
    def Get_competition_Model(self):
    	receptorFile=os.path.join(self.competitionModelFile,self.complex_Name+"_receptor.pdb")
    	ligandFile=os.path.join(self.competitionModelFile,self.complex_Name+"_ligand.pdb")
    	residue_overlapScore,pair_overlapScore = self.Get_the_Score(receptorFile,ligandFile)
    	return residue_overlapScore
    
    def Get_docked_Residue(self):
    	allFiles=os.listdir(self.individualDocks_outdir)
    	receptorFile=os.path.join(self.individualDocks_outdir,"receptor.pdb")
    	allFiles.sort()
    	resultDic=dict()
    	for dockFile in allFiles:
    		if "receptor" not in dockFile:
    			print dockFile
    			ligandFile=os.path.join(self.individualDocks_outdir,dockFile)
			residue_overlapScore,pair_overlapScore = self.Get_the_Score(receptorFile,ligandFile)
			overlap_str = "\t".join((self.complex_Name,dockFile,residue_overlapScore,pair_overlapScore))
			with open (self.outputfile,"a") as f:
				f.write(overlap_str +"\n")
    			
    			resultDic[dockFile]= residue_overlapScore
    			#print resultDic
    			#break
    	return resultDic

    def Get_the_Score(self,receptorFile,ligandFile):
        dockedResidueList,dockedPairlist=Get_interface_residues (receptorFile,ligandFile,"A")
	dockedmodelName=self.complex_Name.split("_")[0]
	nativeResidueList= self.nativedic[dockedmodelName][0]["residueList"]
	nativePairList= self.nativedic[dockedmodelName][0]["pairlist"]
	#print a[0]["residueList"]
	#print residueList,pairlist
	residue_overlapScore = self.Calculate_overlap_Score( dockedResidueList, nativeResidueList)
	pair_overlapScore = self.Calculate_overlap_Score( dockedPairlist, nativePairList)
	return residue_overlapScore,pair_overlapScore
        	

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
    			  			
    			
    def Calculate_overlap_Score(self, dockedList, nativeList):
    	similarities = set(nativeList) & set(dockedList)
    	#print "score", len(similarities)/float(len(nativeList))
    	#print "lensim,native",len(similarities),len(nativeList)
    	#print "len diff",len(list(set(nativeList) - set(dockedList)))
    	overlap_score= "{0:.2f}".format(len(similarities)/float(len(nativeList))*100)
    	return overlap_score

    	
    	
