# download the ARC data from the website

# clone the official repo
& git clone "https://github.com/arcprize/ARC-AGI-2.git"

# copy the data inside the repo and move them to the desired location
Move-Item -Path ".\ARC-AGI-2\data" -Destination "..\data"

# destroy the clone
& Remove-Item -Path ".\ARC-AGI-2" -Recurse -Force
