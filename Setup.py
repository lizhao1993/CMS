from cx_Freeze import setup, Executable


includefiles = [] # include any files here that you wish
includes = []
excludes = []
packages = []
 
exe = Executable(
 # what to build
   script = "example.py", # the name of your main python script goes here 
   initScript = None,
   base = "Win32GUI", # if creating a GUI instead of a console app, type "Win32GUI"
   targetName = "Student CMS.exe", # this is the name of the executable file
   copyDependentFiles = True,
   compress = True,
   appendScriptToExe = True,
   appendScriptToLibrary = True,
   icon = None # if you want to use an icon file, specify the file name here
)
 
setup(
 # the actual setup & the definition of other misc. info
    name = "Student CMS", # program name
    version = "0.1",
    description = 'Test',
    author = "LZ",
    author_email = "LZ",
    options = {"build_exe": {"excludes":excludes,"packages":packages,
      "include_files":includefiles}},
    executables = [exe]
)
