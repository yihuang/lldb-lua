import lldb
import shlex

def extract_str(s):
    return s[s.find('"'):]

def set_luastate(debugger, name):
    res = lldb.SBCommandReturnObject()
    interp = debugger.GetCommandInterpreter()

    set_L = 'expr lua_State* $L=(lua_State*)%s' % name
    interp.HandleCommand(set_L, res)
    if not res.Succeeded():
        interp.HandleCommand('up', res)
        while res.Succeeded():
            interp.HandleCommand(set_L, res)
            if res.Succeeded():
                break
            interp.HandleCommand('up', res)
        else:
            return False
        return True
    return True

def luatrace(debugger, command, result, internal_dict):
    parts = shlex.split(command)
    assert set_luastate(debugger, parts[0] if parts else 'L')

    res = lldb.SBCommandReturnObject()
    interp = debugger.GetCommandInterpreter()
    interp.HandleCommand('p luaL_loadstring ($L, "return debug.traceback()")', res)
    assert res.Succeeded(), res.GetError()
    interp.HandleCommand('p lua_pcall($L, 0, 1, 0)', res)
    assert res.Succeeded(), res.GetError()
    interp.HandleCommand('p lua_tolstring ($L, -1, 0)', res)
    assert res.Succeeded(), res.GetError()
    print >>result, eval(extract_str(res.GetOutput()))
    interp.HandleCommand('p lua_settop ($L, -2)', res)

    assert res.Succeeded(), res.GetError()

def __lldb_init_module(debugger, internal_dict):
    res = lldb.SBCommandReturnObject()
    interp = lldb.debugger.GetCommandInterpreter()
    interp.HandleCommand('command script add -f lldb_lua.luatrace luatrace', res)
    assert res.Succeeded()

#if __name__ == '__main__':
#    lldb.debugger = lldb.SBDebugger.Create()
#    init(lldb.debugger)
#elif lldb.debugger:
#    init(lldb.debugger)
