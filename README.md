# Robots vs Dinosaurs

In this simulate, it's implementing a service that provides a REST API to support a war between robots and dinosaurs.

The key features are:
These are the features required:
### Backend
- Be able to create an empty simulation space - an empty 10 x 10 grid.
- Be able to create a robot in a certain position.
- Be able to create a dinosaur in a certain position.
- Issue instructions to a robot - a robot can move up, move down, move left, move right and attack.
- A robot attack destroys dinosaurs around it (the attack kills all the dinosaurs in up, left, right or
down cell).
- No need to worry about the dinosaurs - dinosaurs don't move.
- Two or more entities (robots or dinosaurs) cannot occupy the same position.
- Attempting to move a robot outside the simulation space is an invalid operation.
#### Run this command on your terminal
```
    1. git clone https://github.com/mohsensami/robots-vs-dinosaurs.git
    2. cd robots-vs-dinosaurs
```
#### Create virtual enviroment to install required libraries
```
    1. pip install virtualenv 
    2. virtualenv venv
    3. source venv/bin/activate
    4. pip install -r requirements.txt
```
#### Run the project
```
uvicorn main:app --reload
```
### Frontend 
- A menu to create a new simulation (be able to add robots, dinosaurs)
- Display the simulation's current state.
#### Front Project Setup
```
cd frontend
yarn
yarn dev
```


### App Preview :

<table width="100%"> 
<tr>
<td width="50%">      
&nbsp; 
<br>
<p align="center">
  Start Game
</p>
<img src="https://github.com/mohsensami/robots-vs-dinosaurs/blob/main/screenshot/_start.png?raw=true">
</td> 
<td width="50%">
<br>
<p align="center">
  Finish Game
</p>
<img src="https://github.com/mohsensami/robots-vs-dinosaurs/blob/main/screenshot/_end.png?raw=true">  
</td>
</table>