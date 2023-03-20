
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from ui.datamodel import DataItem, DataModel

from processor.memory import Memory
from processor.biu import BIU
from processor.EU import EU
from processor.cpu import CPU


class RegistersModel(DataModel):
    def __init__(self, registers, items, parent=None):
        super(RegistersModel, self).__init__(("Name", "Data"), parent)

        self.registers = registers
        for item in items:
            self._rootItem.appendChild(self.createItem(item))

    def createItem(self, name):
        if (hasattr(self.registers, 'gpr')):
            item = (name, self.registers.gpr[name])         # if eu
        else:
            item = (name, self.registers.registers[name])   # if biu
        return DataItem(item)

class FlagModel(DataModel):
    def __init__(self, registers: EU, items, parent=None):
        super(FlagModel, self).__init__(("Name", "Data"), parent)

        self.registers = registers
        for item in items:
            self._rootItem.appendChild(self.createItem(item))

    def format(self, data, bits):
        if isinstance(data, int):
            return str.format("0x{0:0%dx}" % 1, data)
        else:
            return data

    def createItem(self, name):
        item = (name, self.registers.flag.get_from_sym(name))
        return DataItem(item)

class CodeSegModel(DataModel):
    def __init__(self, BIU: BIU, ip, parent=None):
        super(CodeSegModel, self).__init__(("Addr.", "Data"), parent)
        self.ip = ip
        for addr in range(int('30000', 16), int('300ff', 16)):
            info = BIU.read_byte(addr)
            item = (hex(addr), ' '.join(info))
            self._rootItem.appendChild(DataItem(item))

    def data(self, index, role):
        if role == Qt.BackgroundRole and self.ip >= 0 and index.row() == self.ip:
            return QBrush(QColor("#6a4791"))

        return super(CodeSegModel, self).data(index, role)

class StackSegModel(DataModel):
    def __init__(self, BIU: BIU, sp, parent=None):
        super(StackSegModel, self).__init__(["Adr", 'Data'], parent)
        self.sp = sp
        for addr in range(int('60000', 16), int('5ff00', 16), -1):
            info = BIU.read_byte(addr)
            item = [hex(addr), ' '.join(info)]
            self._rootItem.appendChild(DataItem(item))

    def data(self, index, role):
        if role == Qt.BackgroundRole and self.sp >= 0 \
            and index.row() == (0x10000 - self.sp) % 0x10000:
            return QBrush(QColor("#53917f"))

        return super(StackSegModel, self).data(index, role)

class DataSegModel(DataModel):
    def __init__(self, BIU: BIU, parent=None):
        super(DataSegModel, self).__init__(['Adr', '+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8'], parent)

        for adr in range(BIU.registers['DS'] * 16, BIU.registers['DS'] * 16 + 256):
            item = [hex(adr)]
            for i in range(8):
                info = BIU.read_byte(adr + i)
                if isinstance(info, int):
                    item.append(hex(info))
                else:
                    item.append(info[0])

            self._rootItem.appendChild(DataItem(item))