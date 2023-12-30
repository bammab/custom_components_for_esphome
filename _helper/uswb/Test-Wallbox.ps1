﻿#Writing to a Serial Port

#PS> [System.IO.Ports.SerialPort]::getportnames()
#COM3
#PS> $port= new-Object System.IO.Ports.SerialPort COM3,9600,None,8,one
#PS> $port.open()
#PS> $port.WriteLine(“Hello world”)
#PS> $port.Close()

#Reading from a Serial Port

#PS> $port= new-Object System.IO.Ports.SerialPort COM3,9600,None,8,one
#PS> $port.Open()
#PS> $port.ReadLine()

#  ([a-f0-9]{2})
# , 0x\1
$data1 = @(
,[byte[]]@(0x00, 0x78, 0xe0, 0x78, 0x3e, 0x0f, 0x78, 0xe0, 0x00, 0xf8, 0xf8, 0xf8, 0xf8, 0xf8, 0x78, 0xfe, 0xf8, 0xf8, 0x80, 0x80, 0x80, 0xf8 )
,[byte[]]@(0x00, 0x78, 0xe0, 0x78, 0x3e, 0x0f, 0x78, 0xe0, 0x00, 0xf8, 0x78, 0xfe, 0xf8, 0xf8, 0xf8, 0x78, 0xfe, 0xf8, 0x78, 0x00, 0xff, 0x80, 0x80, 0x00 )
,[byte[]]@(0x00, 0x78, 0xe0, 0x78, 0x3e, 0x0f, 0x78, 0xe0, 0x00, 0xf8, 0xf8, 0xf8, 0xf8, 0xf8, 0x78, 0xfe, 0xf8, 0x78, 0x3e, 0xff, 0x80, 0x78, 0x00 )
,[byte[]]@(0x00, 0x78, 0xe0, 0x78, 0x3e, 0x0f, 0x78, 0xe0, 0x00, 0xf8, 0x78, 0xe0, 0xf8, 0xf8, 0x78, 0xfe, 0xf8, 0xf8, 0xf8, 0x80, 0x78, 0xfe, 0xf8 )
,[byte[]]@(0x00, 0x78, 0xe0, 0x78, 0x3e, 0x0f, 0x78, 0xe0, 0x00, 0xf8, 0xf8, 0xf8, 0xf8, 0xf8, 0x78, 0xfe, 0xf8, 0x78, 0x3e, 0xff, 0x80, 0x80, 0xf8 )
,[byte[]]@(0x00, 0x78, 0xe0, 0x78, 0x3e, 0x0f, 0x78, 0xe0, 0x00, 0xf8, 0x78, 0x3e, 0xff, 0xf8, 0xf8, 0x78, 0xfe, 0xf8, 0xf8, 0xf8, 0x80, 0x00, 0x80 )
,[byte[]]@(0x00, 0x78, 0xe0, 0x78, 0x3e, 0x0f, 0x78, 0xe0, 0x00, 0xf8, 0xf8, 0x80, 0xf8, 0xf8, 0x78, 0xfe, 0xf8, 0xf8, 0xf8, 0x80, 0x80, 0x00 )
,[byte[]]@(0x00, 0x78, 0xe0, 0x78, 0x3e, 0x0f, 0x78, 0xe0, 0x00, 0xf8, 0x78, 0x00, 0xff, 0xf8, 0xf8, 0x78, 0xfe, 0xf8, 0x78, 0x3e, 0xff, 0x80, 0xf8, 0xf8, 0xf8 )
)

#19200 8N1
$data2 = @(
,[byte[]]@(0x80, 0xf8, 0x78, 0x3c, 0x0f, 0x80, 0xf8, 0xf8, 0x00, 0x00, 0x78, 0x3c, 0x00, 0x80, 0x00, 0x78, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0xff )
,[byte[]]@(0x80, 0xf8, 0x78, 0x3c, 0x0f, 0x80, 0xf8, 0xf8, 0x00, 0x00, 0x80, 0x00, 0x80, 0x00, 0x78, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8, 0xff )
,[byte[]]@(0x80, 0xf8, 0x78, 0x3c, 0x0f, 0x80, 0xf8, 0xf8, 0x00, 0x00, 0xf8, 0x00, 0x80, 0x00, 0x78, 0x00, 0x00, 0x78, 0x3c, 0x00, 0x00, 0x80, 0x80, 0xff )
,[byte[]]@(0x80, 0xf8, 0x78, 0x3c, 0x0f, 0x80, 0xf8, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x78, 0x00, 0x00, 0x80, 0x00, 0x00, 0x80, 0xff )
,[byte[]]@(0x80, 0xf8, 0x78, 0x3c, 0x0f, 0x80, 0xf8, 0xf8, 0x00, 0x00, 0x78, 0xc0, 0x00, 0x80, 0x00, 0x78, 0x00, 0x00, 0xf8, 0x00, 0x00, 0x80, 0xff )
,[byte[]]@(0x80, 0xf8, 0x78, 0x3c, 0x0f, 0x80, 0xf8, 0xf8, 0x00, 0x00, 0x80, 0x00, 0x80, 0x00, 0x78, 0x00, 0x00, 0x78, 0x3c, 0x00, 0x00, 0xf8, 0xff )
,[byte[]]@(0x80, 0xf8, 0x78, 0x3c, 0x0f, 0x80, 0xf8, 0xf8, 0x00, 0x00, 0xf8, 0x00, 0x80, 0x00, 0x78, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78, 0x00, 0xff )
,[byte[]]@(0x80, 0xf8, 0x78, 0x3c, 0x0f, 0x80, 0xf8, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x78, 0x00, 0x00, 0x78, 0x3c, 0x00, 0x00, 0x78 )
)

# 9600 8N1
$data3 = @(
,[byte[]]@(0x98, 0x66, 0x33, 0xf3, 0x7e, 0x80, 0x00, 0x18, 0x00, 0x18, 0x00, 0x06, 0x00, 0x00, 0x66, 0xc0, 0x80, 0xfe )
,[byte[]]@(0x98, 0x66, 0x33, 0xf3, 0x7e, 0x80, 0x00, 0x1e, 0x00, 0x18, 0x00, 0x06, 0x00, 0x00, 0x60, 0xc0, 0x60, 0x03 )
,[byte[]]@(0x98, 0x66, 0x33, 0xf3, 0x7e, 0x80, 0x00, 0x60, 0x00, 0x18, 0x00, 0x06, 0x00, 0x00, 0x66, 0xc0, 0x00, 0xfe )
,[byte[]]@(0x98, 0x66, 0x33, 0xf3, 0x7e, 0x80, 0x00, 0x66, 0x00, 0x18, 0x00, 0x06, 0x00, 0x00, 0x60, 0xc0, 0xe0, 0xf8 )
,[byte[]]@(0x98, 0x66, 0x33, 0xf3, 0x7e, 0x80, 0x00, 0x78, 0x00, 0x18, 0x00, 0x06, 0x00, 0x00, 0x60, 0xc0, 0x80, 0xfe )
,[byte[]]@(0x98, 0x66, 0x33, 0xf3, 0x7e, 0x80, 0x00, 0x7e, 0x00, 0x18, 0x00, 0x06, 0x00, 0x00, 0x66, 0xc0, 0x60, 0x0c )
,[byte[]]@(0x98, 0x66, 0x33, 0xf3, 0x7e, 0x80, 0x00, 0x80, 0x80, 0x18, 0x00, 0x06, 0x00, 0x00, 0x78, 0xc0, 0x00, 0x87 )
,[byte[]]@(0x98, 0x66, 0x33, 0xf3, 0x7e, 0x80, 0x00, 0x86, 0x80, 0x18, 0x00, 0x06, 0x00, 0x00, 0x7e, 0xc0, 0xe0, 0xf8)
)

# 4800 8N1
$data4 = @(
#,[byte[]]@(0x5A,0xA5,0x07,0x00,0x02,0x02,0x01,0x00,0x85,0xE8)
#,[byte[]]@(0x5A,0xA5,0x07,0x00,0x02,0x02,0x01,0x00,0x85,0xE8)
,[byte[]]@(0x5A,0xA5,0x07,0x00,0x03,0x02,0x01,0x00,0x84,0x14)
)

$data = $data4

function create-buffer() {
# Direct array initialization:
#[byte[]] $b = 1,2,3,4,5
#$b = [byte]1,2,3,4,5
#$b = @([byte]1,2,3,4,5)
#$b = [byte]1..5

# Create a zero-initialized array
#$b = [System.Array]::CreateInstance([byte],5)
#$b = [byte[]]::new(5)        # Powershell v5+
#$b = New-Object byte[] 5
#$b = New-Object -TypeName byte[] -Args 5
}

$data | % {
#$port= new-Object System.IO.Ports.SerialPort COM5,9600,None,8,one
$port= new-Object System.IO.Ports.SerialPort COM5,4800,None,8,one
$port.ReadTimeout = 500
Write-Host "Open COM port"
$port.open()
Write-Host "Write Data $_"
$port.Write($_, 0, $_.Length)
Write-Host "Read byte"
$b = @()
for ($i = 1; $i -lt 11; $i++)
{ $b += $port.ReadByte()
    
}
#$port.ReadByte()
#$b = [byte[]]::new(10)
#$port.Read($b,0,10)
Write-Host "Read buffer $b"
#$port.read
Write-Host "Close connection"
$port.Close()
}