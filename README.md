#PORTFOLIO GENERATOR

A portfolio generator for non-coders.
Developed using Flask.

### First Time Setup

```
virtualenv env
cd portfolio_generator
flask initdb
```

### How to use
```
flask run
``` 
Then open your browser at `127.0.0.1:5000` to add and edit your portfolio.  
When you're done, `Ctrl+C` to stop the server.
```
flask compile
``` 
to compile your data to static files in the folder `/output`.  
Now you can use static file server such as Dropbox, Github Page, or probably your school's server to host your portfolio!  


### What if I want to edit?
Do the same thing again!
```
flask run
```
Then open your browser and edit
```
flask compile
```
Will delete old files and generate new ones.  
