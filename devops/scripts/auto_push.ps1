# auto_push.ps1
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
cd "$PSScriptRoot\..\.."

git add .
git commit -m "Automated push $timestamp"
git push origin main
