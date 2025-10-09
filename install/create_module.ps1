param(
    [Parameter(Mandatory=$true)][string]$custom_module,
    [Parameter(Mandatory=$true)][string]$script_path,
    [Parameter(Mandatory=$true)][string]$working_dir
)

# create the folder containing the custom scripts
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
