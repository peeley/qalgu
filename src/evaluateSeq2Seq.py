#!/usr/bin/python

import torch, json, pickle 
from src import seq2seq, langModel

print('Loading saved resources...')
with open('src/params.json') as paramsFile:
    params = json.load(paramsFile)
hSize    = params['hSize']
maxWords = params['maxWords']
layers   = params['layers']
length   = params['dataSentenceLength']

encoder = torch.load('src/encoder.pt')
decoder = torch.load('src/decoder.pt')
with open('src/eng.p', 'rb') as testFile:
    testLang = pickle.load(testFile)
with open('src/ipq.p', 'rb') as targetFile:
    targetLang = pickle.load(targetFile)
print('Resources loaded.') 

if torch.cuda.is_available():
    device = torch.device('cuda')
    cuda = True
else:
    device = torch.device('cpu')
    cuda = False
print(f"Using device {device}")

def evaluate(rawString):
    with torch.no_grad():
        for item in range(len(rawString)):
            inputString = (rawString[item])
            inputSentence, rareWords = langModel.tensorFromSentence(testLang, inputString, length)
            inputSentence = inputSentence.view(-1,1,1).to(device)

            encoderOutputs, encoderHidden = encoder(inputSentence, None)
            decoderInput = torch.tensor([[targetLang.SOS]]).to(device)
            decoderHidden = encoderHidden[:layers]
            decodedWords = []
            
            for letter in range(maxWords):
                if letter in rareWords.keys():
                    decodedWords.append(rareWords[letter])
                else:
                    decoderOutput, decoderHidden = decoder(decoderInput, decoderHidden, encoderOutputs)
                    decoderOutput = decoderOutput.view(1, -1)
                    topv, topi = decoderOutput.data.topk(1)
                    if topi.item() == testLang.EOS:
                        decodedWords.append('/end/')
                        break
                    else:
                        decodedWords.append(targetLang.idx2word[topi.item()])
                    decoderInput = torch.tensor([topi.squeeze().detach()]).to(device)
    return decodedWords
