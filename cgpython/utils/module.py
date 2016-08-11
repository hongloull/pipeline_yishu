def reloadModules():
    # reload all modules
    import sys
    if globals().has_key('init_modules'):
        for m in [x for x in sys.modules.keys() if x not in init_modules]:
            del(sys.modules[m])
    else:
        init_modules = sys.modules.keys()
