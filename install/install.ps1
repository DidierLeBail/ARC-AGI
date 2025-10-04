# first we need admin privileges, but remembering the initial working directory
param(
	[switch]$Elevated,
    [Parameter(Mandatory=$false)][string]$working_dir=""
)

function Test-Admin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
    $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

if ((Test-Admin) -eq $false)  {
    if ($elevated) {
        # tried to elevate, did not work, aborting
    } else {
		$working_dir = Get-Location
        $processOptions = @{
            FilePath = "powershell"
            Verb = "RunAs"
            ArgumentList = ('-noprofile -noexit -file "{0}" -elevated -working_dir "{1}"' -f ($myinvocation.MyCommand.Definition, $working_dir))
        }
        Start-Process @processOptions
    }
    exit
}
'running with full privileges'

# name of the custom module
$custom_module = "GitTools"

# create the folder containing the custom scripts
$script_path = "$env:ProgramFiles\WindowsPowerShell\Modules\$custom_module"
New-Item -ItemType "Directory" -Path $script_path

# move there the file implementing the custom functions
Move-Item -Path "$working_dir\$custom_module.psm1" -Destination "$script_path\$custom_module.psm1"

# add in the same folder the manifest for the created module,
$moduleManifestParams = @{
    Path = "$script_path\$custom_module.psd1"
    RootModule = $custom_module
    Author = 'Didier Le Bail'
    Description = 'a handful of commands to ease pushing, creating, renaming and switching branches when working on a Git repository'
    CompanyName = 'None'
	FunctionsToExport = 'Switch-git', 'Start-git', 'Push-git', 'Rename-git'
}

New-ModuleManifest @moduleManifestParams
