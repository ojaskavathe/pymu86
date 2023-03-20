from datetime import datetime
import os
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic

from ui.codeeditor import CodeEditor, AssemblyHighlighter
from ui.models import (RegistersModel, FlagModel, CodeSegModel, StackSegModel, DataSegModel)

import re
import sys
import queue
from src.assembler import assemble
from processor.memory import Memory
from processor.biu import BIU
from processor.EU import EU
from processor.cpu import CPU


INSTRUCTION_QUEUE_SIZE = 6
MEMORY_SIZE = int('FFFFF', 16)  # 1MB
CACHE_SIZE = int('10000', 16)  # 64KB
SEGMENT_SIZE = int('10000', 16) # 64kB（10000H）
DEBUG = False

# Initial Values of the segment registers
SEG_INIT = {
    'DS': int('2000', 16),
    'CS': int('3000', 16),
    'SS': int('5000', 16),
    'ES': int('7000', 16) 
}


def _resource(*rsc):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, *rsc)

class MainWindow(object):
    def __init__(self, qApp=None):

        qApp.setStyle('Fusion')
        self.gui = uic.loadUi(_resource('main.ui'))
        # Assembly editor get focus on start
        self.asmEdit = self.gui.findChild(CodeEditor, "asmEdit")
        # Get console area
        self.console = self.gui.findChild(QPlainTextEdit, "txtConsole")

        self.memory = Memory(SEGMENT_SIZE, MEMORY_SIZE)
        
        self.asmEdit.setPlainText(open(_resource('default.asm')).read())
        assembly = self.asmEdit.toPlainText()
        self.exe_file = assemble(assembly, SEG_INIT)
        self.memory.load(self.exe_file, DEBUG)  # load code segment
        
        self.cpu = CPU(self.memory, DEBUG)
        self.runStep = False

        self.emitter = Emitter(self.emitStart)
        self.emitter.refresh.connect(self.refreshModels)
        self.setupEditorAndDiagram()
        self.setupSplitters()
        self.setupModels()
        self.setupTrees()
        self.setupActions()
        self.gui.showMaximized()

    def setupEditorAndDiagram(self):
        self.asmEdit.setFocus()
        self.asmEdit.setStyleSheet("""QPlainTextEdit{
            font-size: 11pt;
            color: #ccc; }""")
        self.highlight = AssemblyHighlighter(self.asmEdit.document())


    def setupSplitters(self):
        mainsplitter = self.gui.findChild(QSplitter, "mainsplitter")
        mainsplitter.setStretchFactor(0, 3)
        mainsplitter.setStretchFactor(1, 4)

        editor_cmd_split = self.gui.findChild(QSplitter, "editor_cmd_split")
        editor_cmd_split.setStretchFactor(0, 2)
        editor_cmd_split.setStretchFactor(1, 1)

        reg_cs_split = self.gui.findChild(QSplitter, "reg_flag_cs_split")
        reg_cs_split.setStretchFactor(0, 1)
        reg_cs_split.setStretchFactor(1, 1)
        reg_cs_split.setStretchFactor(2, 2)

        data_stack_spilt = self.gui.findChild(QSplitter, "data_stack_split")
        data_stack_spilt.setStretchFactor(0, 3)
        data_stack_spilt.setStretchFactor(1, 1)

    def setupModels(self):
        self.genRegsModel = RegistersModel(self.cpu.eu, (
                'AX', 'BX', 'CX', 'DX', 'SP', 'BP', 'SI', 'DI',
            ))
        self.specRegsModel = RegistersModel(self.cpu.biu, (
                'DS', 'CS', 'SS', 'ES', 'IP',
            ))
        self.stateRegsModel = FlagModel(self.cpu.eu, (
                'CF', 'PF', 'AF', 'Z', 'S', 'O', 'TF', 'IF', 'DF',
            ))
        self.CodeSegModel = CodeSegModel(self.cpu.biu, self.cpu.biu.registers['IP'])
        self.StackSegModel = StackSegModel(self.cpu.biu, self.cpu.eu.gpr['SP'])
        self.DataSegModel = DataSegModel(self.cpu.biu)

    def setupTrees(self):
        treeGenericRegs = self.gui.findChild(QTreeView, "treeGenericRegs")
        treeGenericRegs.setModel(self.genRegsModel)
        treeGenericRegs.resizeColumnToContents(0)
        treeGenericRegs.resizeColumnToContents(1)

        treeSpecificRegs = self.gui.findChild(QTreeView, "treeSpecificRegs")
        treeSpecificRegs.setModel(self.specRegsModel)
        treeSpecificRegs.resizeColumnToContents(0)
        treeSpecificRegs.resizeColumnToContents(1)

        treeStateRegs = self.gui.findChild(QTreeView, "treeStateRegs")
        treeStateRegs.setModel(self.stateRegsModel)
        treeStateRegs.resizeColumnToContents(0)
        treeStateRegs.resizeColumnToContents(1)

        # memory
        self.treeMemory = self.gui.findChild(QTreeView, "treeMemory")
        treeMemory = self.treeMemory
        treeMemory.setModel(self.CodeSegModel)
        treeMemory.resizeColumnToContents(0)
        treeMemory.resizeColumnToContents(1)

        self.treeViewStack = self.gui.findChild(QTreeView, "treeViewStack")
        treeViewStack = self.treeViewStack
        treeViewStack.setModel(self.StackSegModel)
        for i in range(8):
            treeViewStack.resizeColumnToContents(i)

        self.treeViewData = self.gui.findChild(QTreeView, "treeViewData")
        treeViewData = self.treeViewData
        treeViewData.setModel(self.DataSegModel)
        treeViewData.resizeColumnToContents(0)
        for i in range(1,9):
            width = treeViewData.width() - treeViewData.columnWidth(0)
            treeViewData.setColumnWidth(i, width // 8)
            # treeViewData.resizeColumnToContents(i)

    def setupActions(self):
        self.actionNew = self.gui.findChild(QAction, "actionNew")
        self.actionNew.triggered.connect(self.newAction)

        self.actionOpen = self.gui.findChild(QAction, "actionOpen")
        self.actionOpen.triggered.connect(self.openAction)

        self.actionSave = self.gui.findChild(QAction, "actionSave")
        self.actionSave.triggered.connect(self.saveAction)

        self.actionLoad = self.gui.findChild(QPushButton, "ButtonLoad")
        self.actionLoad.clicked.connect(self.loadAssembly)

        self.actionRun = self.gui.findChild(QPushButton, "ButtonRun")
        self.actionRun.clicked.connect(self.runAction)

        self.actionRun = self.gui.findChild(QPushButton, "ButtonRunStep")
        self.actionRun.clicked.connect(self.runStepAction)

        self.actionPause = self.gui.findChild(QPushButton, "ButtonPause")
        self.actionPause.clicked.connect(self.pauseAction)
        
        self.actionStep = self.gui.findChild(QPushButton, "ButtonStep")
        self.actionStep.clicked.connect(self.nextInstruction)

        self.actionStop = self.gui.findChild(QPushButton, "ButtonStop")
        self.actionStop.clicked.connect(self.stopAction)

    def loadAssembly(self):
        # Enable/Disable actions
        # self.treeMemory.resizeColumnToContents(0)
        # self.treeMemory.resizeColumnToContents(1)
        self.actionLoad.setEnabled(False)
        self.actionRun.setEnabled(True)
        self.actionStop.setEnabled(True)
        self.actionPause.setEnabled(True)
        self.actionStep.setEnabled(True)

        editor = self.asmEdit
        editor.setReadOnly()
        
        assembly = editor.toPlainText()
        if not assembly:
            self.console.appendPlainText("Input Error.")
            self.restoreEditor()
            return
        editor.verticalScrollBar().setValue(0)

        self.exe_file = assemble(assembly, SEG_INIT)
        self.memory = Memory(SEGMENT_SIZE, MEMORY_SIZE)
        self.memory.load(self.exe_file, DEBUG)  # load code segment
        self.cpu = CPU(self.memory, DEBUG)
        self.refreshModels()

        self.console.appendPlainText("Initial DS: " + hex(self.cpu.biu.registers['DS']))
        self.console.appendPlainText("Initial CS: " + hex(self.cpu.biu.registers['CS']))
        self.console.appendPlainText("Initial SS: " + hex(self.cpu.biu.registers['SS']))
        self.console.appendPlainText("Initial ES: " + hex(self.cpu.biu.registers['ES']))
        self.console.appendPlainText("Initial IP: " + hex(self.cpu.biu.registers['IP']))
        self.console.appendPlainText("\nCPU initialized successfully.")
        self.console.appendPlainText("=" * 60 + '\n')
    
    def newAction(self):
        self.stopAction()
        self.asmEdit.setPlainText('\n'*30)
        self.restoreEditor()

    def saveAction(self):
        self.stopAction()
        filename = QFileDialog().getSaveFileName(self.gui, 'Save file', filter='*.asm', initialFilter='*.asm')[0]
        if os.path.exists(filename):
            with open(filename,'w') as f:
                text=self.asmEdit.toPlainText()
                f.write(text)

    def openAction(self):
        self.stopAction()
        filename = QFileDialog().getOpenFileName(self.gui, "Open File")[0]
        if os.path.exists(filename) and self.asmEdit.document().isModified():
            answer = QMessageBox.question(None, "Modified Code",
                """<b>The current code is modified</b>
                   <p>What do you want to do?</p>
                """,
                QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
        if os.path.exists(filename):
            text = open(filename, encoding='utf-8').read()
            if len(text.split('\n')) < 30:
                text += '\n' * (30-len(text.split('\n')))
            self.asmEdit.setPlainText(text)
            self.restoreEditor()

    def emitStart(self, refresh):
        self.cpu.eu.interrupt = False
        while not self.cpu.terminated():
            self.cpu.run()
            if (self.runStep):
                refresh.emit()
                time.sleep(0.1)
        self.actionRun.setEnabled(True)
        self.actionStep.setEnabled(True)
        self.cpu.print_end_state()
        refresh.emit()
        if self.cpu.eu.shutdown:
            self.cpu.eu.print("CPU Shutdown.")
            self.actionLoad.setEnabled(True)
            self.actionRun.setEnabled(False)
            self.actionPause.setEnabled(False)
            self.actionStep.setEnabled(False)
            self.actionStop.setEnabled(True)

    def runAction(self):
        print("run...")
        self.runStep = False
        self.actionRun.setEnabled(False)
        self.actionStep.setEnabled(False)        
        self.emitter.start()
        self.restoreEditor()

    def runStepAction(self):
        self.runStep = True
        self.actionRun.setEnabled(False)
        self.actionStep.setEnabled(False)        
        self.emitter.start()

    def nextInstruction(self):
        self.cpu.eu.interrupt = False
        if not self.cpu.terminated():
            self.cpu.run()
            self.refreshModels()

        if self.cpu.eu.shutdown:
            self.cpu.print_end_state()
            self.restoreEditor()
        print("step end")

    def pauseAction(self):
        self.cpu.eu.interrupt = True
        self.actionRun.setEnabled(True)
        self.actionStep.setEnabled(True)

    def stopAction(self):
        self.pauseAction()
        self.restoreEditor()

    def restoreEditor(self):
        # Enable/Disable actions
        self.actionLoad.setEnabled(True)
        self.actionRun.setEnabled(False)
        self.actionPause.setEnabled(False)
        self.actionStep.setEnabled(False)
        self.actionStop.setEnabled(False)
        # Re-enable editor
        self.asmEdit.setReadOnly(False)
        self.asmEdit.setFocus()

    def refreshModels(self):
        self.console.moveCursor(self.console.textCursor().End)
        self.console.insertPlainText(self.cpu.eu.output)
        self.cpu.eu.output = ''
        self.setupModels()
        self.setupTrees()

    def show(self):
        self.gui.show()

class Emitter(QThread):
    refresh = pyqtSignal()

    def __init__(self, fn):
        super(Emitter, self).__init__()
        self.fn = fn

    def run(self):
        self.fn(self.refresh)
