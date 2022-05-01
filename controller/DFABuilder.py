

from itertools import product
from model.Environment import Environment
from model.Equipment import Equipment
from model.PathGenerator import PathGenerator
from model.Pipe import Pipe
from controller.IDGenerator import IDGenerator
import pathlib


path_to_dfa_folder = str(pathlib.Path().absolute().as_posix())+"/DFAs/"

class DFABuilder():


	def generate_dfa(env, equs, pipe, complete_paths):
		""" Generates the DFA file. 
		Input: Environment, List<Equipment>, Pipe, List<List<tuples/point>>. """
		DFABuilder.append_pipe_to_DFA(pipe)
		DFABuilder.append_env_to_DFA(env)
		for equ in equs:
			DFABuilder.append_equ_to_DFA(equ)
		
		for path in complete_paths:
			DFABuilder.append_path_to_DFA(path)
		DFABuilder.sweep_paths()
			
	def append_env_to_DFA(env, design_id):
		""" Append environment to the current DFA file """
		env_ID = IDGenerator.create_dfa_element_ID("environment")
		f = open(path_to_dfa_folder + "templates/Environment.dfa", "r")
		txt = f.read()
		txt = txt.replace("<ENV_ID>", env_ID)
		txt = txt.replace("<HEIGHT>", env[4])
		txt = txt.replace("<WIDTH>", env[5])
		txt = txt.replace("<LENGTH>", env[6])
		f.close()

		f = open(path_to_dfa_folder + "products/" + design_id + ".dfa", "a")
		f.write(txt)
		f.close
		return design_id

	def append_equ_to_DFA(equs, design_id):
		""" Append equ to the current DFA file """
		for equ in equs:
			equ_ID = IDGenerator.create_dfa_element_ID("equipment")
			f = open(path_to_dfa_folder + "templates/Equipments.dfa", "r")
			txt = f.read()
			txt = txt.replace("<ENV_ID>", equ_ID)
			txt = txt.replace("<X_POS>", equ[1][0])
			txt = txt.replace("<Y_POS>", equ[1][1])
			txt = txt.replace("<Z_POS>", equ[1][2])
			txt = txt.replace("<HEIGHT>", equ[4])
			txt = txt.replace("<WIDTH>", equ[5])
			txt = txt.replace("<LENGTH>", equ[6])
			f.close()

			f = open(path_to_dfa_folder + "products/" + design_id + ".dfa", "a")
			f.write(txt)
			f.close
			return design_id

	def append_pipe_to_DFA(pipe):
		""" Append pipe to the current DFA file """
		design_id = IDGenerator.create_design_ID()
		f = open(path_to_dfa_folder + "templates/PipeSystem.dfa", "r")
		txt = f.read()
		txt = txt.replace("<ID>", design_id)
		f.close()
		f = open(path_to_dfa_folder + "products/" + design_id + ".dfa", "w")
		f.write(txt)
		f.close

		f1 = open(path_to_dfa_folder + "templates/Pipe.dfa", "r")
		txt1 = f1.read()
		txt1 = txt1.replace("<CURVE_RADIUS>", pipe.elbow_curve_radius)
		txt1 = txt1.replace("<OUTER_RADIUS>", pipe.diameter_outer)
		txt1 = txt1.replace("<INNER_RADIUS>", pipe.diameter_inner)
		f1.close()

		f1 = open(path_to_dfa_folder + "products/" + design_id + ".dfa", "a")
		f1.write(txt1)
		f1.close
		return design_id




	def append_path_to_DFA(path, design_id):
		""" Append path to the current DFA file """
		paths_to_sweep = []
#-------------------------- ARCS ---------------------------------------------
		for el in path:
			if len(el) == 3:
				elbow = []
				elbow.append(el)
				for elb in straights:
					elb_ID = IDGenerator.create_dfa_element_ID("elbow")
					f = open(path_to_dfa_folder + "templates/Arc.dfa", "r")
					txt = f.read()
					txt = txt.replace("<CURVE>", elb_ID)
					txt = txt.replace("CENTER", elb[0])
					txt = txt.replace("X_ARC_VECTOR", elb[1])
					txt = txt.replace("Y_ARC_VECTOR", elb[2])
					f.close()

					f = open(path_to_dfa_folder + "products/" + design_id + ".dfa", "a") #design_ID is created in append_pipe_to_DFA and returned. need to fetch it form there.
					f.write(txt)
					f.close
					paths_to_sweep.append(elb_ID)

#-------------------------- LINES -----------------------------------------------
			if len(el) == 2:
				straights = []
				straights.append(el)
				for st in straights:
					str_ID = IDGenerator.create_dfa_element_ID("straigth")
					f = open(path_to_dfa_folder + "templates/Line.dfa", "r")
					txt = f.read()
					txt = txt.replace("START_POINT", st[0])
					txt = txt.replace("END_POINTT", st[1])
					f.close()

					f = open(path_to_dfa_folder + "products/" + design_id + ".dfa", "a") #design_ID is created in append_pipe_to_DFA and returned. need to fetch it form there.
					f.write(txt)
					f.close
					paths_to_sweep.append(str_ID)

		return paths_to_sweep

					

	def sweep_paths(paths_to_sweep, design_id):
		""" Sweeps on the paths to make the pipes """
		path = ''
		for e in paths_to_sweep:
    		
			path += e +', '
		path = path[:-2]
		f = open(path_to_dfa_folder + "templates/Sweep.dfa", "r")
		txt = f.read()
		txt = txt.replace("<PIPE_PATH>", path)
		f.close()

		f = open(path_to_dfa_folder + "products/" + design_id + ".dfa", "a")
		f.write()
		f.close()
		

