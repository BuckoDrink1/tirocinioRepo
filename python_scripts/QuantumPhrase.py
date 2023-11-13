from lambeq import SpacyTokeniser, AtomicType, IQPAnsatz,  BobcatParser, pregroups, Rewriter, remove_cups
from qiskit import QuantumCircuit, qpy
from qiskit.quantum_info import Statevector
from pytket.extensions.qiskit import tk_to_qiskit
#from quantum_circuit_to_matrix import Justify, qc2matrix
import numpy as np
import os
import TextProcessor
from nltk.stem import PorterStemmer
from lambeq import stairs_reader, cups_reader, spiders_reader

class QuantumPhraseProcessing:
    
    def __init__(self, phrase):
        self.rawstring = phrase
        self.tokens = []
        self.diagram = None
        self.rew_diagram = None
        self.disco_circuit = None
        self.qiskit_circuit = None
        
    def tokenise(self):
        ps = PorterStemmer()
        
        tokens = SpacyTokeniser().tokenise_sentence(self.rawstring)
        for word in tokens:
            st = ps.stem(word)
            if(st == "n’t"):
                st = 'not'
            self.tokens.append(st)
        return self
        
    def parse(self):
        if(not self.tokens):
            self.tokenise()
        parser = BobcatParser()
        #parser = spiders_reader
        self.diagram = parser.sentence2diagram(self.tokens, tokenised=True)
        return self

    def rewrite(self):
        if(self.diagram == None):
            self.parse()
        rewriter = Rewriter(['prepositional_phrase', 'determiner'])
        rewritten_diagram = rewriter(self.diagram)
        normalised_diagram = rewritten_diagram.normal_form()
        curry_functor = Rewriter(['curry'])
        #curried_diagram = self.diagram 
        curried_diagram = curry_functor(normalised_diagram)
        self.rew_diagram = remove_cups(curried_diagram.normal_form())
        return self
        
    def generate_qiskit_circuit(self):
        if(self.rew_diagram == None):
            self.rewrite()
        N = AtomicType.NOUN
        S = AtomicType.SENTENCE
        ansatz = IQPAnsatz({N: 1, S: 1}, n_layers=1, n_single_qubit_params=3)
        discopy_circuit = ansatz(self.rew_diagram)
        self.disco_circuit = discopy_circuit
        circ = discopy_circuit.to_tk()
        self.qiskit_circuit = tk_to_qiskit(circ)
        return self

class QuantumPhraseQiskit:
    
    def __init__(self, phrase):
        self.qc = QuantumPhraseProcessing(phrase).generate_qiskit_circuit().qiskit_circuit
        
    def setParameters(self, constant):
        params = self.qc.parameters
        inp = {}
        
        for t, i in enumerate(params):
            k = {i: constant}
            inp.update(k)
            
        circ = self.qc.bind_parameters(inp)
        return circ
    
    def setParametersWlist(self, list):
        params = self.qc.parameters
        inp = {}
        
        for t, i in enumerate(params):
            k = {i: list[t]}
            inp.update(k)
        
        circ = self.qc.bind_parameters(inp)
        return circ
    
#    def getExMatrix(self, fname):
#        qc2matrix(self.qc, Justify.none, fname)
#        return self

class SplitQuantumPhraseQiskit:
    
    def __init__(self, string):
        self.strings = TextProcessor.TextProcessor(string).process_text()
        self.circuits = {}
    
    def run(self):
        for s in self.strings:
            try:
                c = QuantumPhraseProcessing(s).generate_qiskit_circuit().qiskit_circuit
                self.circuits.update({s : c})
            except:
                pass
        return self

    def save(self, baseID):
        if(baseID == None):
            for key in self.circuits:
                with open(key + ".qpy", "wb") as qpy_file_write:
                    qpy.dump(self.circuits[key], qpy_file_write)
            return self
        i=baseID
        for key in self.circuits:
            with open("circuit" + str(i) + ".qpy", "wb") as qpy_file_write:
                    qpy.dump(self.circuits[key], qpy_file_write)
            with open("circuit" + str(i) + ".txt", 'w') as f:
                    f.write(key)
            i = i+1
        return i