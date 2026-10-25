param([Parameter(Mandatory=$true)][string]$RequestJson)
$ErrorActionPreference='Stop'
$request=Get-Content -LiteralPath $RequestJson -Raw -Encoding UTF8 | ConvertFrom-Json
$speaker=New-Object -ComObject SAPI.SpVoice
$matching=@($speaker.GetVoices() | Where-Object { $_.GetDescription() -eq $request.voice })
if($matching.Count -ne 1){throw 'The requested David voice is not installed.'}
$speaker.Voice=$matching[0];$speaker.Rate=0;$speaker.Volume=100
$stream=New-Object -ComObject SAPI.SpFileStream
try{$stream.Format.Type=18;$stream.Open([string]$request.output,3);$speaker.AudioOutputStream=$stream;$speaker.Speak([string]$request.text) | Out-Null}finally{$stream.Close()}
