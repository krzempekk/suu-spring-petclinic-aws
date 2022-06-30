wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.5.tgz
tar -xf apache-jmeter-5.5.tgz
export PATH=$(pwd)/apache-jmeter-5.5/bin:$PATH
wget https://jmeter-plugins.org/files/packages/jpgc-casutg-2.10.zip
unzip jpgc-casutg-2.10.zip -d apache-jmeter-5.5
sudo apt update
sudo apt install openjdk-17-jdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

