$ErrorActionPreference = "Stop"

$root = Split-Path $PSScriptRoot -Parent

$expected = @{
    "src\govq\protocol.py" =
        "43FE0AE672F07F8CC91D022B713F6DCC01F0C01021D8CD194EE4CC6C7B4EB692"
    "src\govq\providers\model_input.py" =
        "27660946D30FB6EE320697BF1AB60F09D51F7205DC15A590303686D6C397B7B1"
}

foreach ($relative in $expected.Keys) {
    $path = Join-Path $root $relative
    if (-not (Test-Path $path)) { throw "Missing required public source: $relative" }
    $actual = (Get-FileHash $path -Algorithm SHA256).Hash.ToUpperInvariant()
    if ($actual -ne $expected[$relative]) {
        throw "Public source identity changed: $relative`nExpected: $($expected[$relative])`nActual: $actual"
    }
    Write-Host "HASH PASS  $relative"
}

$forbiddenPattern = 'benchama|bma_|ysc|police|host\.docker|D:\\benchama-ai-project'
$textExtensions = @(".py",".md",".toml",".txt",".yml",".yaml",".json")

$hits = Get-ChildItem $root -Recurse -File |
    Where-Object { $textExtensions -contains $_.Extension.ToLowerInvariant() } |
    Where-Object { $_.FullName -notmatch '\\.git\\' -and $_.FullName -notmatch '\\.venv\\' } |
    Select-String -Pattern $forbiddenPattern -CaseSensitive:$false

if ($hits) {
    $hits | Format-Table Path, LineNumber, Line -AutoSize
    throw "Private/project-specific naming scan failed."
}

Write-Host "PRIVATE NAMING SCAN PASS"
Write-Host "PUBLIC_BATCH_1A_VERIFY = PASS"