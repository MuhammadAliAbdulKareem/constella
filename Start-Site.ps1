$ErrorActionPreference = "SilentlyContinue"
$root = $PSScriptRoot
$port = 8000
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
try {
    $listener.Start()
} catch {
    $port = 8080
    $listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add("http://localhost:$port/")
    $listener.Start()
}

$mime = @{
    ".html"="text/html; charset=utf-8"; ".js"="application/javascript"; ".css"="text/css";
    ".json"="application/json"; ".png"="image/png"; ".jpg"="image/jpeg"; ".jpeg"="image/jpeg";
    ".svg"="image/svg+xml"; ".ico"="image/x-icon"; ".woff"="font/woff"; ".woff2"="font/woff2"
}

Write-Host ""
Write-Host "  ================================================"
Write-Host "   Constella is running at  http://localhost:$port"
Write-Host "  ================================================"
Write-Host "  If the browser didn't open on its own, copy the link above into it."
Write-Host "  Keep THIS window open while you browse the site."
Write-Host ""

Start-Process "http://localhost:$port/"

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
    } catch {
        Write-Host "  (connection hiccup, still listening: $($_.Exception.Message))"
        continue
    }
    $request = $context.Request
    $response = $context.Response
    try {
        $localPath = $request.Url.LocalPath
        if ($localPath -eq "/") { $localPath = "/index.html" }
        $filePath = Join-Path $root ($localPath.TrimStart('/') -replace '/', [IO.Path]::DirectorySeparatorChar)

        if (Test-Path $filePath -PathType Leaf) {
            $ext = [IO.Path]::GetExtension($filePath)
            $contentType = $mime[$ext]
            if (-not $contentType) { $contentType = "application/octet-stream" }
            $bytes = [IO.File]::ReadAllBytes($filePath)
            $response.ContentType = $contentType
            $response.ContentLength64 = $bytes.Length
            $response.OutputStream.Write($bytes, 0, $bytes.Length)
        } else {
            $response.StatusCode = 404
            $msg = [Text.Encoding]::UTF8.GetBytes("404 Not Found: $localPath")
            $response.OutputStream.Write($msg, 0, $msg.Length)
        }
    } catch {
        $response.StatusCode = 500
    } finally {
        $response.OutputStream.Close()
    }
}

Write-Host ""
Write-Host "  The server stopped."
Read-Host "  Press Enter to close this window"
