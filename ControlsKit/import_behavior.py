from sys import argv, exit

def importBehavior(module_or_file_name = None):
    if module_or_file_name is None:
        if len(argv) != 2:
            print "Usage: %s <behavior-module>" % argv[0]
            exit(2)    
        module_or_file_name = argv[1].strip()
    
    if module_or_file_name.endswith(".py"):
        module_or_file_name = module_or_file_name[:-3]
    
    module = __import__(module_or_file_name)
    try:
        return module.update
    except AttributeError:
        raise AttributeError("The behavior module must have an update() function.")
