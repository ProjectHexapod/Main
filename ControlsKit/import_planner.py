from sys import argv, exit, path
import string

def importPlanner(module_or_file_name = None):
    if module_or_file_name is None:
        if len(argv) != 2:
            print "Usage: %s <planner-module>" % argv[0]
            exit(2)    
        module_or_file_name = argv[1].strip()
    
    if module_or_file_name.endswith(".py"):
        module_or_file_name = module_or_file_name[:-3]
    try:
        dirname,filename = string.rsplit(module_or_file_name,'/',1)
        path.append(dirname)
    except ValueError:
        filename = module_or_file_name
    
    module = __import__(filename)
    try:
        if hasattr(module, 'controller'):
            return module.update, module.controller
        else:
            return module.update
    except AttributeError:
        raise AttributeError("The planner module must have an update() function.")
