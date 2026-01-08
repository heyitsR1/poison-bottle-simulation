# poison-bottle-simulation

<p>
  This was a riddle given to me by a senior engineer, basically you have to use 10 prisoners to find 1 single poisoned bottle out of 1000 bottles.
</p>
<p>Here's a more common description of the problem: </p>

> <i>The King of a small country invites 1000 senators to his annual party. As a tradition, each senator brings the King a bottle of wine. Soon after, the Queen discovers that one of the senators is trying to assassinate the King by giving him a bottle of poisoned wine. Unfortunately, they do not know which senator, nor which bottle of wine is poisoned, and the poison is completely indiscernible. However, the King has 10 prisoners he plans to execute. He decides to use them as taste testers to determine which bottle of wine contains the poison. The poison when taken has no effect on the prisoner until exactly 24 hours later when the infected prisoner suddenly dies. The King needs to determine which bottle of wine is poisoned by tomorrow so that the festivities can continue as planned. Hence he only has time for one round of testing. How can the King administer the wine to the prisoners to ensure that 24 hours from now he is guaranteed to have found the poisoned wine bottle?</i>

## Program does stuff: 
<div style="text-align: center;">
  <img width="500" height="500" src="https://github.com/user-attachments/assets/811db35e-fe12-475d-8cda-7bdeaa27d3f4"  src="..." alt="image" style="display: block; margin: 0 auto;"
>
</div>

## Try it out with a simple Cntrl + C and Cntrl + V: 

- Use via curl or wget:
```
curl -fsSL https://raw.githubusercontent.com/heyitsR1/poison-bottle-simulation/main/posion-prisoner.py | python3
```
```
wget -qO posion-prisoner.py https://raw.githubusercontent.com/heyitsR1/poison-bottle-simulation/main/posion-prisoner.py && python3 posion-prisoner.py
```
### Flags
```
curl -fsSL https://raw.githubusercontent.com/heyitsR1/poison-bottle-simulation/main/posion-prisoner.py | python3 - --bottles 512 --prisoners 9
```
- Just run python3 poison-prisoner.py || run it with flags
  
   --random , --bottles, --prisoners, --poisoned
  
- bottles defines total number of bottles || default = 1000
- prisoners defines total number of prisoners || default = 10
- poisoned defines the id/number of the poisoned wine bottle || default is random
- random is for random ofc ofc

Example: 
```
python3 poison-prisoner.py
```
or 

```
python3 ./poison-prisoner.py --bottles=1048576  --prisoners=20 --poisoned=69
```



  
