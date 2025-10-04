#download the ARC data from the website
function DownloadFilesFromRepo {
	Param(
		[string]$SourcePath,
		[string]$DestinationPath
		)
		$prefix="https://raw.githubusercontent.com/fchollet/ARC-AGI/refs/heads/master/data/training/"
		$ProgressPreference='SilentlyContinue'
	
		$wr = (Invoke-WebRequest -Uri $SourcePath).Content -split "\n"
		$substring="`"path`":`"data`""
		$start=0
		while (-not ($wr[$start].Contains($substring))) {
			$start=$($start+1)
		}

		$line=$wr[$start]
		$firstIndex = $line.IndexOf('[')
		$lastIndex = $line.IndexOf(']')
		$length=$($lastIndex-$firstIndex+1)
		$names=(ConvertFrom-Json -InputObject $line.Substring($firstIndex,$length)).name
		
		$WebClient = New-Object System.Net.WebClient
		foreach ($name in $names) {
			$fileSource=$($prefix+$name)
			$fileDestination = Join-Path $DestinationPath $name
			$WebClient.DownloadFile($fileSource,$fileDestination)
		}
}
# $env:path
# $SourcePath = "https://github.com/fchollet/ARC-AGI/tree/master/data/training/"
# $DestinationPath = "../data"
# $completeDestination=Join-Path $PSScriptRoot $DestinationPath
# DownloadFilesFromRepo -SourcePath $SourcePath -DestinationPath $completeDestination

# define a directory of custom Modules in:
# C:\Program Files\WindowsPowerShell\Modules

Push-git "test for custom modules!"
