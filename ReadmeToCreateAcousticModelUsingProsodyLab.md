---------Prosodylab-Aligner Installation on Ubuntu--------

Follow below steps:
1. Install Python3 and pip on ubuntu machine.
2. Install htk by downloading toolkit from this website(http://htk.eng.cam.ac.uk/download.shtml).
3. Unzip the toolkit and run below commands in the ubuntu terminal;

>cd htk
>export CPPFLAGS=-UPHNALG
>sudo apt-get install libx11-dev
>sudo apt-get install g++-multilib
>./configure --disable-hlmtools --disable-hslab
>sudo apt install ruby
>ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
>eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
>brew install gcc
>brew install python3
>sudo apt-get install sox

Install the Prosodylab-Aligner to create own acoustic model:
>git clone http://github.com/prosodylab/Prosodylab-Aligner
>cd Prosodylab-Aligner
>pip3 install -r requirements.txt

Keep all your data audio (.wav) files and transcripts ).lab) files in the data directory and run below command.
>python3 -m aligner -c eng.yaml -d eng.dict -e 10 -t newDirectory/ -w lang-mod.zip

The lang-mod.zip acoustic model will be created and this model can be used with our web application for languages other than English.

