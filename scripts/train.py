import os
import argparse
import configparser
from shutil import copyfile
from importlib import import_module

parser = argparse.ArgumentParser()
parser.add_argument("ModelName", help= "Model class name")
parser.add_argument("PreprocessorName", help = "Preprocessor class name")
args = parser.parse_args()

config = configparser.ConfigParser()
config.optionxform = str
config.read("./config.cfg")

'''
for sect in config.sections():
    section_items = dict(config.items(sect))
    print("Section %s" % sect)
    for key in section_items.keys():
        print("Key: %s" % section_items[key])
''' and None

model_parameters = dict(config.items(args.ModelName))
preprocessor_parameters = dict(config.items(args.PreprocessorName))
data_parameters = dict(config.items('Data'))

#load preprocessor
module_name = preprocessor_parameters['PreprocessorModule']
input_path = data_parameters['Inputs']

module = import_module("preprocessors.%s" % (module_name))
preprocessor_class = getattr(module, args.PreprocessorName)
preprocessor = preprocessor_class(input_path, preprocessor_parameters) #needs to be changed for processor params or something

#load network model
module_name = model_parameters['ModelModule']
checkpoint_dir = data_parameters['CheckpointDirectory']
result_path = data_parameters['Outputs']

module = import_module("models.%s" % (module_name))
ml_class= getattr(module, args.ModelName)
my_model = ml_class(result_path, checkpoint_dir, model_parameters, preprocessor)
my_model.init_network()

# my_model.model.load_weights('/home/user/Mozgalo/checkpoints/MicroblinkBaseNet/MicroblinkBasePreprocessorWithFakes/2018-04-03__09_27_51/0.4697-0001.hdf5', by_name = True, skip_mismatch = True)

copyfile("./config.cfg", os.path.join(my_model.full_checkpoint_dir_path,'config.cfg'))
my_model.fit_with_generator()
