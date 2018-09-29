# Service-inspector
  
## In a nutshell  
Simple service to observe healthy of other services.

## How to use  
### How make new checker
You should to create new class inheretaning from `InspectorAbstract` from `utils.common`. Simple example:
```
class GoogleInspector(InspectorAbstract):  
  interval = 60  
  name = "Google Main Page"  
  
  def check(self):  
        return requests.head('https://google.com').ok
```
where required parameters:
* interval - value in seconds for rerun `check` method
* name - name of checker for viewing
* check - main method for running check

### How to add into 

Just put `.py` file with inspectors into `inspectors` folder. Name of file will be name of project. 

## Extra
### More details
Are you want to more details in report? Not a problem - just describe `self.details` in `check` method, like this:
```
    ...
    def check(self):
        response = requests.get('https://google.com')
        self.details = {'status': response.status_code}
        return response.ok
```
### Reusing network connections
For reusing HTTP connection for requests can use `Session` class from `utils.sessions`, like this:
```
session = Session('https://google.com')
...
return session.head('https://google.com').ok
```
### Using telegram bot
You can using telegram bot for reporting of services status. For this set parameters:
* TELEGRAM_TOKEN - token of bot
* TELEGRAM_CHANNEL - number of channel for reporting
### Main Page example
![](https://image.ibb.co/iyczj9/Screen_Shot_2018_09_29_at_11_19_54.png)