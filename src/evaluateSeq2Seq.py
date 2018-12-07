#!/usr/bin/python

import torch, json, pickle 
from src import seq2seq, langModel

with open('src/params.json') as paramsFile:
    params = json.load(paramsFile)
hSize    = params['hSize']
maxWords = params['maxWords']
layers   = params['layers']
length   = params['dataSentenceLength']

if torch.cuda.is_available():
    device = torch.device('cuda')
    cuda = True
else:
    device = torch.device('cpu')
    cuda = False

def evaluate(encoder, decoder, rawString, testLang, targetLang):
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
