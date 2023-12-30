# Master Anfragen

Start of Frame      Len                 SlaveId   Func?     Q/A                 CRC16 Modbus (LE uint16)
5Ah       A5h       07h       00h       02h       02h       01h       00h       85h       E8h      
5Ah       A5h       07h       00h       03h       02h       01h       00h       84h       14h      
5Ah       A5h       07h       00h       04h       02h       01h       00h       85h       60h      
5Ah       A5h       07h       00h       05h       02h       01h       00h       84h       9Ch      
5Ah       A5h       07h       00h       06h       02h       01h       00h       84h       D8h      
5Ah       A5h       07h       00h       07h       02h       01h       00h       85h       24h      
5Ah       A5h       07h       00h       08h       02h       01h       00h       86h       30h      
5Ah       A5h       07h       00h       09h       02h       01h       00h       87h       CCh      
                              
090d      165d      007d      000d      002d      002d      001d      000d      133d      232d     
090d      165d      007d      000d      003d      002d      001d      000d      132d      020d     
090d      165d      007d      000d      004d      002d      001d      000d      133d      096d     
090d      165d      007d      000d      005d      002d      001d      000d      132d      156d     
090d      165d      007d      000d      006d      002d      001d      000d      132d      216d     
090d      165d      007d      000d      007d      002d      001d      000d      133d      036d     
090d      165d      007d      000d      008d      002d      001d      000d      134d      048d     
090d      165d      007d      000d      009d      002d      001d      000d      135d      204d     
                              
01011010d 10100101d 00000111d 00000000d 00000010d 00000010d 00000001d 00000000d 10000101d 11101000d
01011010d 10100101d 00000111d 00000000d 00000011d 00000010d 00000001d 00000000d 10000100d 00010100d
01011010d 10100101d 00000111d 00000000d 00000100d 00000010d 00000001d 00000000d 10000101d 01100000d
01011010d 10100101d 00000111d 00000000d 00000101d 00000010d 00000001d 00000000d 10000100d 10011100d
01011010d 10100101d 00000111d 00000000d 00000110d 00000010d 00000001d 00000000d 10000100d 11011000d
01011010d 10100101d 00000111d 00000000d 00000111d 00000010d 00000001d 00000000d 10000101d 00100100d
01011010d 10100101d 00000111d 00000000d 00001000d 00000010d 00000001d 00000000d 10000110d 00110000d
01011010d 10100101d 00000111d 00000000d 00001001d 00000010d 00000001d 00000000d 10000111d 11001100d


# Kommunikation

## SlaveID 2

-> 5Ah       A5h       07h       00h       02h       02h       01h       00h       85h       E8h  
   090d      165d      007d      000d      002d      002d      001d      000d      133d      232d
   01011010d 10100101d 00000111d 00000000d 00000010d 00000010d 00000001d 00000000d 10000101d 11101000d
<- 5Ah       A5h       07h       00h       02h       02h       02h       00h       85h       18h 
   090d      165d      007d      000d      002d      002d      002d      000d      133d      024d
   01011010d 10100101d 00000111d 00000000d 00000010d 00000010d 00000010d 00000000d 10000101d 00011000d

## SlaveID 3

-> 5Ah       A5h       07h       00h       03h       02h       01h       00h       84h       14h  
   090d      165d      007d      000d      003d      002d      001d      000d      132d      020d
   01011010d 10100101d 00000111d 00000000d 00000011d 00000010d 00000001d 00000000d 10000100d 00010100d
<- 5Ah       A5h       07h       00h       03h       02h       02h       00h       84h       E4h  
   090d      165d      007d      000d      003d      002d      002d      000d      132d      228d
   01011010d 10100101d 00000111d 00000000d 00000011d 00000010d 00000010d 00000000d 10000100d 11100100d










# Mitschnitt
10 Byte Umbruch

00h       02h       02h       01h       00h       85h       E8h       5Ah       A5h       07h
00h       03h       02h       01h       00h       84h       14h       5Ah       A5h       07h
00h       04h       02h       01h       00h       85h       60h       5Ah       A5h       07h
00h       05h       02h       01h       00h       84h       9Ch       5Ah       A5h       07h
00h       06h       02h       01h       00h       84h       D8h       5Ah       A5h       07h
00h       07h       02h       01h       00h       85h       24h       5Ah       A5h       07h
00h       08h       02h       01h       00h       86h       30h       5Ah       A5h       07h
00h       09h       02h       01h       00h       87h       CCh       5Ah       A5h       07h

000d      002d      002d      001d      000d      133d      232d      090d      165d      007d
000d      003d      002d      001d      000d      132d      020d      090d      165d      007d
000d      004d      002d      001d      000d      133d      096d      090d      165d      007d
000d      005d      002d      001d      000d      132d      156d      090d      165d      007d
000d      006d      002d      001d      000d      132d      216d      090d      165d      007d
000d      007d      002d      001d      000d      133d      036d      090d      165d      007d
000d      008d      002d      001d      000d      134d      048d      090d      165d      007d
000d      009d      002d      001d      000d      135d      204d      090d      165d      007d

00000000d 00000010d 00000010d 00000001d 00000000d 10000101d 11101000d 01011010d 10100101d 00000111d
00000000d 00000011d 00000010d 00000001d 00000000d 10000100d 00010100d 01011010d 10100101d 00000111d
00000000d 00000100d 00000010d 00000001d 00000000d 10000101d 01100000d 01011010d 10100101d 00000111d
00000000d 00000101d 00000010d 00000001d 00000000d 10000100d 10011100d 01011010d 10100101d 00000111d
00000000d 00000110d 00000010d 00000001d 00000000d 10000100d 11011000d 01011010d 10100101d 00000111d
00000000d 00000111d 00000010d 00000001d 00000000d 10000101d 00100100d 01011010d 10100101d 00000111d
00000000d 00001000d 00000010d 00000001d 00000000d 10000110d 00110000d 01011010d 10100101d 00000111d
00000000d 00001001d 00000010d 00000001d 00000000d 10000111d 11001100d 01011010d 10100101d 00000111d


This is not entirely correct. Modbus is a/the protocoll. And if using modbus with the default functions (like reading register) it's easy to read all registers to find out simple values without a documented register table (I don't seen custom function codes yet).
But the uswb11a1 (and a2) don't use modbus. The version A2 should use modbus, but the documentation of the "register" is a propritary protocoll and not modbus.
So the protocoll was really not known for version A1. Not even the baudrate on the communication layer rs485 was known.