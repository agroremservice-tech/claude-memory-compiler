# PowerShell — UTF-8 файли з українським текстом

## Проблема

`Get-Content` без явного кодування читає файл як Windows-1252 (CP1252). Якщо потім записати через `Out-File -Encoding utf8` — отримуємо кракозябри замість кирилиці.

## Правило

Для читання і запису UTF-8 файлів (щоденники, нотатки Obsidian) — **тільки** через .NET:

```powershell
# Читати
$text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# Записати
[System.IO.File]::WriteAllText($path, $text, [System.Text.Encoding]::UTF8)
```

## Альтернатива

Використовувати Write tool (Claude Code) замість PowerShell для запису utf-8 файлів — він завжди пише в UTF-8.

## Небезпечні патерни (не використовувати для кирилиці)

```powershell
Get-Content $file                     # читає як CP1252
$lines | Out-File $file               # пише як UTF-16 LE
$lines | Out-File $file -Encoding utf8  # BOM + неправильне читання якщо Get-Content був без кодування
```
