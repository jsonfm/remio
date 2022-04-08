"""List the serial ports devices"""
from remio import Serial, Serials


print("> Available port devices:")
for port in Serial.ports():
    print(f" - {port}")
print()


# Also available with the Serials class
print("> Available port devices:")
for port in Serials.ports():
    print(f" - {port}")
