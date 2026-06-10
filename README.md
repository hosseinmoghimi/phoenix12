# Phoenix12
 
## Version 0.2.2

## install pip packages

```bash
    pip install -r requirements.txt
```


## Copy server config files

```bash
    cp phoenix/sample_settings.py phoenix/server_settings.py
```
```bash
    cp phoenix/sample_urls.py phoenix/server_urls.py
```
```bash
    cp phoenix/sample_apps.py phoenix/server_apps.py
```

 
## Edit server config files

 
replace SECRET_KEY in
```bash
    vi phoenix/server_settings.py
```
list your urls
```bash
    vi phoenix/server_urls.py
```
list your apps in
```bash
    vi phoenix/server_apps.py
```
 

## Copy accounting config files

for accounting app copy this file then edit it if needed
```bash
    cp accounting/sample_settings.py accounting/server_settings.py
```

  ## Authors

- [@Hossein Moghimi](https://dikoo24.ir)

