#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
import os
from SCons.Script import *
import SCons.Util

def get_all_dir(path_list:list)->list:
    dir_list = []
    if isinstance(path_list,str):
        path_list = [path_list]
    for foo in path_list:   
        for r,d,f in os.walk(foo):
            for each in d:
                if ".svn" not in os.path.join(r,each):
                    dir_list.append(os.path.join(r,each))
    return dir_list
    
def get_all_specific_suffix_file(path_list:list,suffix:str)->list:
    file_list = []
    if isinstance(path_list,str):
        path_list = [path_list]
    for foo in path_list:   
        for r,d,f in os.walk(foo):
            for each in f:
                if os.path.splitext(each)[-1] == suffix:
                    file_path = os.path.join(r,each)
                    relpath = os.path.relpath(file_path,foo)
                    file_list.append(relpath)
                    
    return file_list

def compile_all_c(env,path=None,flags=''):
    if not path: path =os.getcwd()
    all_c = get_all_specific_suffix_file(path,'.c')
    libnode_list = env.Object(source=all_c,parse_flags=flags)

    return(libnode_list)

def execute_script(env,scriptfile):
    basepath = os.path.split(scriptfile)[0]
    basename = os.path.basename(basepath)
    libnode = env.SConscript(scriptfile, variant_dir='build/output/'+basename, duplicate=0 ,exports=['basepath','env'])
    return libnode

def setup():
    EnsurePythonVersion(3, 6)
    EnsureSConsVersion(3, 0)
    AddMethod(Environment, compile_all_c,'compile_all_c')
    AddMethod(Environment, execute_script,'execute_script')

import os,subprocess,logging


class Shell(object):
    
    @classmethod
    def execute(cls, cmd, **kwargs):
        '''
        to suppress the interaction with OS, such as 'puase', the stdin should be passed with the file handle of
        NULL device '/dev/null'(linux) or 'nul'(windows).
        the NULL DEV Handle can be replaced with 'subprocess.DEVNULL' in python 3.x.
        '''
        devnull_handle = open(os.devnull, "r")
        result = 0
        try:
            logging.getLogger().info("execute [%s] start !" % (cmd))
            kwargs['shell'] = True
            kwargs['stdin'] = devnull_handle
            result = subprocess.check_call(cmd, **kwargs)
            if result != 0:
                logging.getLogger().error("compile %s error !" % (cmd))
            else:
                logging.getLogger().info("execute [%s] success !" % (cmd))
        except subprocess.CalledProcessError as err:
                logging.getLogger().error("[%s] throw CalledProcessError [%s] while execute [%s]" % (err.returncode, \
                                                                                             err.output, cmd))
                result = err.returncode
        devnull_handle.close()
        return result

    @classmethod
    def execute_output(cls, cmd, **kwargs):
        devnull_handle = open(os.devnull, "r")
        result = 0
        try:
            logging.getLogger().info("execute [%s] start !" % (cmd))
            kwargs['shell'] = True
            kwargs['stdin'] = devnull_handle
            output = subprocess.check_output(cmd, **kwargs)
        except subprocess.CalledProcessError as err:
            logging.getLogger().error("[%s] throw CalledProcessError [%s] while execute [%s]" % (err.returncode, \
                                                                                         err.output, cmd))
            output = ""
        devnull_handle.close()
        return output
    @classmethod
    def fork_os_env(cls, script, **kwargs):
        def source(script):
            output = Shell.execute_output("bash -c set -a && %s >/dev/null && env -0" % script)
            output = output.decode('utf8')
            env = dict((line.split("=", 1) for line in output.split('\x00') if line))
            return env
        env = {}
        env.update(os.environ)
        env.update(source(script))
        return env



if __name__ == '__main__':
    main()
