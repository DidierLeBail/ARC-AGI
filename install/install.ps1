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

<#
create the custom module implementing the powershell commands for Git management
first check whether the module already exists
#>
# name of the custom module
$custom_module = "GitTools"

# path to the folder containing the custom scripts
$script_path = "$env:ProgramFiles\WindowsPowerShell\Modules\$custom_module"

if (!(Test-Path -Path $script_path)) {
    & "$working_dir\create_module.ps1" $custom_module $script_path $working_dir
}
