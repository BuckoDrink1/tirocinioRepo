import QuantumPhrase
import os
import warnings
from pytket.extensions.qiskit import AerBackend
from lambeq import TketModel
from lambeq import SpacyTokeniser
from pytket import Circuit
import importlib
from sympy import symbols
from discopy.quantum import tk

QuantumPhrase = importlib.reload(QuantumPhrase)

warnings.filterwarnings('ignore')
os.environ['TOKENIZERS_PARALLELISM'] = 'true'

import numpy as np
import random

BATCH_SIZE = 230
EPOCHS = 100
SEED = 2

def evaluation(a, b):
    if(b%a == 0):
        return 1
    return 0

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line

def getvalues(tokens):
    count = 0
    out = []
    for char in tokens:
        if(count >= 2):
            return out[0], out[1]
        if(char.isnumeric()):
            out.append(int(char))
            count = count + 1
    return

def read_data(fname, diction, qta):
    data = []
    values = []
    with open(fname) as f:
        i=0
        while(i<=qta):
            line = random_line(f)
            var0, var1 = getvalues(SpacyTokeniser().tokenise_sentence(line))
            
            if(var1 != 0):
                data.append(line.strip())
                values.append(evaluation(var1, var0))
                diction.append([var0, var1])
                i = i+1
            f.seek(0)
    return data, values, diction

def parametrize(circ, variables):
    for v in variables:
        circ.symbol_substitution({symbols(str(v)+"__s_0"):v})
    return circ

def parametrize_list(circuits, variables_list):
    j = 0
    out = []
    while(j < len(circuits)):
        out.append(parametrize(circuits[j], variables_list[j]))
        j=j+1
    return out

diction1 = []
diction2 = []
text, labels, diciton1 = read_data("phrases.txt", diction1, 230)
text_test, labels_test, diction2 = read_data("phrases_test.txt", diction2, 230)
print("Done loading files...\n")

train_circuits = [QuantumPhrase.QuantumPhraseProcessing(t).generate_qiskit_circuit().disco_circuit for t in text]
train_labels = [[i, 1-i] for i in labels]
#display(QuantumPhrase.QuantumPhraseProcessing(text[0]).generate_qiskit_circuit().disco_circuit.draw(figsize=(15,10)))
#print(len(train_circuits))
#print(type(train_circuits[0]))
#print(train_circuits[0])
#train_circuits = parametrize_list(train_circuits, diction1)
print("Done generating training circuits...\n")

test_circuits = [QuantumPhrase.QuantumPhraseProcessing(t).generate_qiskit_circuit().disco_circuit for t in text_test]
test_labels = [[i, 1-i] for i in labels_test]
#test_circuits = parametrize_list(test_circuits, diction2)
print("Done generating test circuits...\n")

#print(len(train_circuits))
#print(len(train_labels))
#print(len(test_circuits))
#print(len(test_labels))

#temp1 = [tk.from_tk(t) for t in train_circuits]
#temp2 = [tk.from_tk(t) for t in test_circuits]
#train_circuits = temp1
#test_circuits = temp2

#display(train_circuits[0].draw(figsize=(15,10)))
#print(type(temp1[0]))

all_circuits = train_circuits + test_circuits

backend = AerBackend()
backend_config = {
    'backend': backend,
    'compilation': backend.default_compilation_pass(2),
    'shots': 8192
}

print("Backend initialized...\n")

model = TketModel.from_diagrams(all_circuits, backend_config=backend_config)

from lambeq import NumpyModel

#model = NumpyModel.from_diagrams(all_circuits, use_jit=False)

from lambeq import BinaryCrossEntropyLoss

# Using the builtin binary cross-entropy error from lambeq
bce = BinaryCrossEntropyLoss()

acc = lambda y_hat, y: np.sum(np.round(y_hat) == y)/len(y) / 2  # half due to double-counting
eval_metrics = {"acc": acc}

from lambeq import QuantumTrainer, SPSAOptimizer

trainer = QuantumTrainer(
    model,
    loss_function=bce,
    epochs=EPOCHS,
    optimizer=SPSAOptimizer,
    optim_hyperparams={'a': 0.05, 'c': 0.06, 'A':0.001*EPOCHS},
    evaluate_functions=eval_metrics,
    evaluate_on_train=True,
    verbose = 'text',
    log_dir='./john/doe10/',
    seed=0
)
print("Trainer setup complete...\n")

from lambeq import Dataset

train_dataset = Dataset(
            train_circuits,
            train_labels,
            batch_size=BATCH_SIZE)

val_dataset = Dataset(test_circuits, test_labels, shuffle=False)

print("Dataset setup complete...\n")

trainer.fit(train_dataset, val_dataset, early_stopping_interval=10)

print("Training complete...\n")