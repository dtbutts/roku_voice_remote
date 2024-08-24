This project runs a python script that allows you to wirelessly control your Roku tv through speech recognition.  

I used the Kaldi Speech Recognition Toolkit for speech recognition - https://github.com/kaldi-asr/kaldi and https://kaldi-asr.org/.
You must download a language model from here and plug it into my python script to work. 

To build: 
  update 'model_path' to path of your downloaded language model.
  update 'IP_ADDRESS_OF_TV' to your Roku TV's IP address. This can be found on the TV in Settings => Network => About. 
