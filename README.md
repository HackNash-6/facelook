
Tied for 2nd place at Hack Nashville 6
========
##CelebriME :Find celebrities that most look like you

Team Members
* Chris Graffagnino (nashguitar1@gmail.com)
* Jack Malpasuto (jackmalpo@gmail.com)
* Bennet Littlejohn (bennettlittlejohn@gmail.com)
* Tena Percy (tena.percy@gmail.com)
* Marlee Stevensen (master26@gmail.com)
* Stephen Bain (swbain@gmail.com)
* David Gilmore (dagilmore91@gmail.com)
* Mahesh Thundathil (mesh@fastmail.fm)
* Geoffrey Gross (geoffreyrgross@gmail.com)
* Kaili Liu (pybeebee@gmail.com)
* John Liu (guard0g@gmail.com)

Instructions to Install vm:
========
Make sure you have vagrant (https://www.vagrantup.com/downloads.html) and virtualbox  (https://www.virtualbox.org/wiki/Downloads) installed

* Create a directory ~/vagrant
* cd ~/vagrant
* Download Vagrantfile (into this directory)
* Download vm from this link:  https://www.dropbox.com/s/kgrei0t54f0b1g8/hacknash6.box?dl=0
* Start the vm with the command:  vagrant up

To login in and start ipython notebook:
* login using the command:  vagrant ssh
* once in, start the notebook with the script in the home directory:  bash ./ipython_notebook_start.sh
* On your browser, enter the URL: http://localhost:8888

REST server commands:
========
curl -H "Content-Type: application/octet-stream" -X POST host:port/similarity --data-binary @image.jpg
