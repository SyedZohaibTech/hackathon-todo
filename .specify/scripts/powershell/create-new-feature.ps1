param(
    [Parameter(Mandatory=$true)]
    [string]$Json,
    [Parameter(Mandatory=$false)]
    [int]$Number,
    [Parameter(Mandatory=$false)]
    [string]$ShortName,
    [Parameter(Mandatory=$false)]
    [string]$Description
)

# Create the feature branch and spec directory
$branchName = "${Number}-${ShortName}"
$specDir = "specs/${Number}-${ShortName}"

# Create the spec directory if it doesn't exist
if (!(Test-Path $specDir)) {
    New-Item -ItemType Directory -Path $specDir -Force | Out-Null
}

# Create the spec file
$specFile = "${specDir}/spec.md"
if (!(Test-Path $specFile)) {
    # We'll write the content later from the calling process
    New-Item -ItemType File -Path $specFile -Force | Out-Null
}

# Output JSON result
$result = @{
    BRANCH_NAME = $branchName
    SPEC_FILE = $specFile
    SPEC_DIR = $specDir
} | ConvertTo-Json

Write-Output $result