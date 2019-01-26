#!/usr/bin/python

import torch, json, pickle 
from src import seq2seq, langModel

print('Loading saved resources...')
encoder = torch.load('src/models/encoder_2019_1_11.pt')
decoder = torch.load('src/models/decoder_2019_1_11.pt')
with open('src/models/source.p', 'rb') as testFile:
    testLang = pickle.load(testFile)
with open('src/models/target.p', 'rb') as targetFile:
    targetLang = pickle.load(targetFile)
print('Resources loaded.') 

if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
print(f"Using device {device}")

def evaluate(rawString):
    with torch.no_grad():
        maxWords = decoder.maxLength
        layers = encoder.numLayers
        inputSentence, rareWords = langModel.tensorFromSentence(testLang, rawString, maxWords)
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
