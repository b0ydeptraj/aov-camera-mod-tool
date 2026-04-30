Set shell = CreateObject("WScript.Shell")
toolDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
scriptPath = toolDir & "\patch_camera_gui.py"
shell.Run "pythonw.exe " & Chr(34) & scriptPath & Chr(34), 0, False
