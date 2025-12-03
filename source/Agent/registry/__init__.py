import pkgutil
import importlib
import  Agent.Agents 

lib = Agent.Agents.__path__
dir_name = Agent.Agents.__name__
for _, module_name, _ in pkgutil.iter_modules(lib):
    print(module_name)  
    importlib.import_module(f"{dir_name}.{module_name}")