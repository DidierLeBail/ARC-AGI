# rename the branch $old_name to $new_name
function Rename-git {
    param (
        [Parameter(Mandatory=$true)][string]$old_name,
        [Parameter(Mandatory=$true)][string]$new_name,
        [Parameter(Mandatory=$false)][string]$remote="origin"
    )
    # Rename the local branch to the new name
    & git branch -m $old_name $new_name

    # Delete the old branch on remote
    & git push $remote --delete $old_name

    # Prevent git from using the old name when pushing in the next step.
    # Otherwise, git will use the old upstream name instead of $new_name.
    & git branch --unset-upstream $new_name

    # Push the new branch to remote
    & git push $remote $new_name

    # Reset the upstream branch for the new_name local branch
    & git push $remote -u $new_name
}

# return the path to $project_root
function Get-root {
    param (
        [Parameter(Mandatory=$false)][string]$project_root="ARC-AGI"
    )
    $list_paths=(& Get-Location).Path.Split('\')

    # find the index in list_paths at which we get the project root
    # and determine its absolute path
    $index = 0
    $root_path = ""
    while (!($list_paths[$index] -eq $project_root)) {
        $root_path = $root_path, $list_paths[$index] -join "\"
        $index = $index + 1
    }

    $root_path = $root_path, $project_root -join "\"
    return $root_path.TrimStart("\")
}

# push local changes to remote
function Push-git {
    param (
        [Parameter(Mandatory=$false)][string]$commit_msg="minor",
        [Parameter(Mandatory=$false)][string]$remote="origin"
    )
    $current_branch = & git rev-parse --abbrev-ref HEAD

    # push local changes upstream
    & git add ../*
    & git commit -m $commit_msg
    & git push $remote $current_branch
}

# create a new branch of name $new_branch both locally and upstream, and end in the current branch
function Start-git {
    param (
        [Parameter(Mandatory=$true)][string]$new_branch,
        [Parameter(Mandatory=$false)][string]$remote="origin"
    )
    $current_branch = & git rev-parse --abbrev-ref HEAD

    & git checkout -b $new_branch
    Push-git -commit_msg "initialized a new branch" -remote $remote
    & git checkout $current_branch
}

# switch from the current branch to $new_branch
function Switch-git {
    param (
        [Parameter(Mandatory=$true)][string]$new_branch,
        [Parameter(Mandatory=$false)][string]$commit_msg="minor",
        [Parameter(Mandatory=$false)][string]$remote="origin"
    )

    # first push eventual changes
    Push-git -commit_msg $commit_msg -remote $remote

    # get the path to the root of the project
    $root_path = Get-root

    # remove undesired untracked files:
    #__pycache__
    & Get-ChildItem -Path $root_path -Include __pycache__ -Recurse | Remove-Item -Recurse -Force

    # switch branch
    & git checkout $new_branch
}
