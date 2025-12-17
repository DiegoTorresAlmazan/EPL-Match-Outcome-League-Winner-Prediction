Get-ChildItem "E0*.csv" |
ForEach-Object {
    if ($_.Name -eq "E0.csv") {
        $startYear = 2024
    }
    elseif ($_.Name -match '\((\d+)\)') {
        $startYear = 2024 - [int]$matches[1]
    }
    else {
        return
    }

    $endYear = $startYear + 1
    $newName = "EPL_${startYear}_${endYear}.csv"

    Write-Host "Renaming $($_.Name) -> $newName"
    Rename-Item $_ $newName
}
