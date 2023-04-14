# pymu86

Pymu is a Python-based program that provides a reliable and efficient way to run software written for the Intel 8086 microprocessor.

The emulator includes an assembler that loads assembled programs into a memory object and a CPU class that executes instructions. It uses regex to streamline the translation of Assembly language instructions, and executes it using an emulated CPU written in Python. PyQt5 was used for the GUI, so it must be installed before running.

Pymu was built as a project to learn CPU architectures and not as a faithful replica of the 8086. As such, results may not be entirely accurate, but I've done my best to have instructions executed the way they're meant to!
