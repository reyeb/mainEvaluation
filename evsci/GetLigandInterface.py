#import os
from Bio.PDB import *
from Bio.PDB import PDBParser
from Bio.PDB import PDBIO
import Bio.PDB
from optparse import OptionParser
import random,os
from collections import defaultdict

#python GetLigandInterface.py --f1 5HT2B_1106_0001_receptor.pdb --f2 5HT2B_1106_0001_ligand.pdb --c1 A --c2 c --c 4.5 --i 10.0 --jobid example_output


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_atom_list(structure, chains):
	
	output = dict()
	for chain in structure:
		if chain.id in chains:
			for residue in chain.get_residues():
				hetflag, resseq, icode=residue.get_id()
				#print hetflag, resseq, icode# 
				the_id = (chain.id+"_"+str(resseq)+"_"+residue.get_resname()).strip()
				for atom in residue.get_unpacked_list():
					if hetflag==' ':
						if the_id in output:
							output[the_id].append(atom)
						else:
							output[the_id] = [atom]
	return output
	

def is_contact(res_1,other_atoms,cutoff):
	
	for atom in res_1:
		ns = NeighborSearch(other_atoms)
		center = atom.get_coord()
		neighbors = ns.search(center, cutoff) # 5.0 for distance in angstrom
		residue_list = Selection.unfold_entities(neighbors, 'R') # R for residues
		if len(residue_list)>0:
			ligandlist=[]
			for rr in residue_list:
				for atom in rr.get_unpacked_list():
					ligandlist.append(atom)
			return True,ligandlist
	return False,[] 	

def get_contacts(struc,all_atoms,verbose,cutoff):
	progress = 0 
	contacts = []
	contactLigandDic= defaultdict(list)
	for residue in struc:
		#print residue
		progress+=1
		#if len(verbose)>0:
			#print verbose,progress,"out of",len(struc)
		atom_list = struc[residue]
		outcome,ligandlist = is_contact(atom_list,all_atoms,cutoff)
		if outcome:
			contacts.append(residue)
			contactLigandDic[residue].append(ligandlist)
	return contacts,contactLigandDic			

#Filter out all the atoms from the chain,residue map given by residue_map
def get_all_atoms(residue_map):
	all_atoms_out = []
	for residue in residue_map:
		print residue
		for atom in residue_map[residue]:
			all_atoms_out.append(atom)
			
			#Set the b-factor to zero for coloring by contacts
			#atom.set_bfactor(0.0)
	return all_atoms_out

def get_all_ligand_atoms(model_lig):
	all_atoms_out = []
	for chain in model_lig:
		for residue in chain:
		    id = residue.id
		    if id[0] != ' ':
		    	for atom in residue:
		    		#print atom
		    		all_atoms_out.append(atom)
	return all_atoms_out
	
#Save the structures with B-factor field replaced with contact (100) and interface neighborhood (50)
def save_contacts(structure, chains,out_file):
	
	#Save only those chains that we are supposed to
	Select = Bio.PDB.Select
        class ConstrSelect(Select):
            def accept_chain(self, chain):
                #print dir(residue)
                
                if chain.id in chains:
                    return 1
                else:
                    return 0
	
	w = PDBIO()
        w.set_structure(structure)
	randint = random.randint(0,9999999)
        w.save("TMP"+str(randint)+".pdb",ConstrSelect())
        #Remove the HETATM and TER lines
	f_tmp = open("TMP"+str(randint)+".pdb", 'r')
	f_out = open(out_file, 'w')
	for line in f_tmp.readlines():
		if line[0:3]!="TER" and line[0:6]!="HETATM":
			f_out.write(line)
	f_tmp.close()
	f_out.close()	
	os.remove("TMP"+str(randint)+".pdb")

#Save the residues which are contacts or neighborhood interface in a space-delimited file
def save_residues(filename,interface,contacts):
	f = open(filename,'w')	
	for elem in interface:
		splitted = elem.split("_")
		resname = str((splitted[1]+splitted[2]).strip())
		chain = splitted[0]
		#contact or neighbor of interface?
		coninf = "I" #Interface neighbor
		if elem in contacts:
			coninf = "C" #Contact
		f.write(chain+" "+resname+" "+coninf+"\n")
	f.close()

#Save the residues which are contacts or neighborhood interface in a space-delimited file
def save_residues(filename,interface,contacts,):
	residueList=[]
	#f = open(filename,'w')
	for elem in interface:
		splitted = elem.split("_")
		resname = str((splitted[2]+"_"+splitted[1]).strip())
		
		residueList.append(resname)
		chain = splitted[0]
		#contact or neighbor of interface?
		coninf = "I" #Interface neighbor
		if elem in contacts:
			coninf = "C" #Contact
		#f.write(chain+" "+resname+" "+coninf+"\n")
	#f.close()
	return residueList
	
#only save the residues of the file that are in thelist
def save_constrained(filename_in,filename_out,thelist):
	f = open(filename_in,'r')
	f_out = open(filename_out,'w')
	for line in f.readlines():
		if "ATOM" in line:
			line = line.strip()
			resname=line[23:28].strip()
			icode = "" 
			if (not is_number(resname[len(resname)-1])):
				icode = resname[len(resname)-1]
				resname = resname[0:(len(resname)-1)]
				
			resname = line[21]+"_"+resname+"_"+icode
			if resname in thelist:
				f_out.write(line+"\n")
			
#Save the residues which are contacts or neighborhood interface in a space-delimited file
def save_residues_Ligand_pair(filename,interface,contacts,contactLigandDic):
	pairlist=[]
	for res in contactLigandDic:
		splitted = res.split("_")
		resname = str((splitted[2]+"_"+splitted[1]).strip())
		#print contactLigandDic[res]
		for atoml in contactLigandDic[res]:
			for aa in atoml:
				#print resname,aa.get_name()
				pairlist.append(resname+"_"+aa.get_name())
				#break
				
	return pairlist
	
def Get_interface_residues(f1,f2,c1,cutoff = 5.0):			

	cutoff = float(cutoff)
	
	str_1 = PDBParser().get_structure('first_one', f1) # load your molecule
	str_2 = PDBParser().get_structure('second_one', f2) # load your molecule

	chains_1 = c1


	#Load the structures - they can be the same!
	atoms_1 = Selection.unfold_entities(str_1, 'C') # C for chains
	atoms_2 =  str_2[0]
	#print atoms_1
	#get the mapping from chain,residue id to the atom lists
	input_1 = get_atom_list(atoms_1,chains_1)

	#get the full atom lists for neighbor search
	all_atoms_2 = get_all_ligand_atoms(atoms_2)
	
	#run neighbor search on both instances - not optimal but good enough for most imaginable applications.
	contacts_1, contactLigandDic = get_contacts(input_1,all_atoms_2,"First molecule, residue ",cutoff)
	

	contact_map_1 = []
	for residue in contacts_1:
		for atom in input_1[residue]:
			contact_map_1.append(atom)
	#Get interfacial residues
	#run neighbor search on both instances - not optimal but good enough for most imaginable applications.
	interface_1 = contacts_1
	
	residueList = save_residues("",interface_1,contacts_1)
	
	pairlist=save_residues_Ligand_pair("",interface_1,contacts_1,contactLigandDic)
	
	#print len(residueList),len(pairlist)
	return residueList,pairlist
		
#Get_interface_residues("5HT1B_4IAR_receptor.pdb","5HT1B_4IAR_ligand.pdb",c1="A")
