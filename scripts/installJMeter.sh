wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.5.tgz
tar -xf apache-jmeter-5.5.tgz
export PATH=$(pwd)/apache-jmeter-5.5/bin:$PATH
sudo apt update
sudo apt install openjdk-17-jdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

