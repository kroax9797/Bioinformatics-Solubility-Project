import numpy as np 
import pandas as pd 
import pickle 
from PIL import Image 
from rdkit import Chem 
from rdkit.Chem import Descriptors

def AromaticProportion(m):
  aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
  aa_count = []
  for i in aromatic_atoms:
    if i==True:
      aa_count.append(1)
  AromaticAtom = sum(aa_count)
  HeavyAtom = Descriptors.HeavyAtomCount(m)
  AR = AromaticAtom/(HeavyAtom+0.00000000000000000001)
  return AR

def generate(smiles, verbose=False):

    moldata= []
    for elem in smiles:
        mol=Chem.MolFromSmiles(elem)
        moldata.append(mol)

    baseData= np.arange(1,1)
    i=0
    for mol in moldata:

        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
        desc_AromaticProportion = AromaticProportion(mol)

        row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds,
                        desc_AromaticProportion])

        if(i==0):
            baseData=row
        else:
            baseData=np.vstack([baseData, row])
        i=i+1

    columnNames=["MolLogP","MolWt","NumRotatableBonds","AromaticProportion"]
    descriptors = pd.DataFrame(data=baseData,columns=columnNames)

    return descriptors

import streamlit as st

left , right =st.columns(2)
with left : 
    image = Image.open('molecular-solubility-predictor-logo-zip-file\png\logo-black.png')
    st.image(image  , width = 200)
with right : 
    st.header("Molecular Solubility Prediction App")

st.write("This app predicts the **Solubility(logS)** values . ")
st.write('Data obtained from the John S. Delaney. [ESOL:  Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x). ***J. Chem. Inf. Comput. Sci.*** 2004, 44, 3, 1000-1005.')

smiles_input = "CCCC"
smiles= st.text_area("Smiles Input" , smiles_input)
smiles = "C\n" + smiles 
smiles = smiles.split('\n')

st.header('Input Smiles : ')
st.write(smiles[1:])

st.header('Computed Molecular Descriptors')
x = generate(smiles)
st.write(x[1:])

load_model = pickle.load(open('solubility_model.pkl' , 'rb'))
prediction = load_model.predict(x)

st.header('Predicted LogS values :')
for i in range(1 , len(smiles)):
    st.write(smiles[i] , prediction[i-1])



