# Prerequisites
- [jmeter v5.5](https://jmeter.apache.org/download_jmeter.cgi)
- JMeter plugin [Ultimate Thread Group](https://jmeter-plugins.org/wiki/UltimateThreadGroup/) - needed only for scripts modifications

# How to run scripts?

Run scripts/runLoadScript.sh (you may need to adjust parameters).

# Pre-prepared scripts

## JMeter test plans

Five test plans for JMeter were prepared, and they are included in test-plans folder.

For single user, following requests are made:
- list all owners
- add owner
- get owner details
- update owner
- add pet (randomly - add two pets)
- update pet
- list all veterinarians
- add veterinarian visit (randomly - add two visits)

Test plans have different number of parallel users, and differn in how the number of user changes in time. The test schedule for plans can be seen below:

##### Test plan 1:

![image](https://user-images.githubusercontent.com/49311489/174455975-3e5d3d5b-db79-43ba-9150-836d9faee07a.png)

##### Test plan 2:

![image](https://user-images.githubusercontent.com/49311489/174455982-5afebd06-8ad5-4efd-bb87-c6d5a3ea70e4.png)

##### Test plan 3:

![image](https://user-images.githubusercontent.com/49311489/174455997-2949d4f4-becb-4ff4-9fcd-263586ef983d.png)

##### Test plan 4:

![image](https://user-images.githubusercontent.com/49311489/174456008-43aee93e-6fb3-443a-9b03-357a2b197cb9.png)

##### Test plan 5:

![image](https://user-images.githubusercontent.com/49311489/174456020-460681c0-9fd2-4214-94ef-d33eee0dcc1f.png)

# How to modify scripts?

- Run GUI for JMeter
- Open script you want to modify
- To modify load, go to **jp@gc - Ultimate Thred Group**, then adjust load in **Threads Schedule**:

![image](https://user-images.githubusercontent.com/49311489/174456674-d36798ab-36b7-4074-a82c-ccba24e4ca76.png)

