# Satori GDPR/CCPA Query Tool
## Redshift-specific

Scans for all Satori locations looking for TAGNAME = DB_VALUE
- First: Iterates through all redshift locations using the Satori Data Inventory, skipping over any location which is not tagged with TAGNAME.
- Second: if TAGNAME is found, attempts to actually run a redshift query against this location WHERE TAGNAME = 'DB_VALUE'.
- Each query uses Satori hostnames/endpoints, so any existing security rules and masking are applied.

e.g. 

```python app.py EMAIL "some_email@some_company.com"```

or

```python app.py IDNUM "1234567890"```

or

```python app.py SSN "111-22-3333"```

where EMAIL, IDNUM and SSN are built-in Satori taxonomy names. 

See API call to retrieve full list [here](https://app.satoricyber.com/docs/api#get-/api/v1/taxonomy/satori).

off-label usage :) may include things like:

```python app.py STATE "California"```

or

```python app.py PERSONNAME "Jane"```


___

- Get a Satori service account ID and key/secret from the Satori management console
- Download this repo
- Tested on macOS. We recommend ```pyenv``` e.g.
	- ```pyenv install 3.12.2```
	- ```pyenv virtualenv 3.12.2 redshift-gdpr```
	- ```pyenv global redshift-gdpr```
	- at this point you should have a localized env called 'redshift-gdpr' running python 3.12.2
	- ```pip install -r requirements.txt```
	- at this point you are ready to run the app
- Edit and save **./satori/satori.py** - all values must be filled in.
- Run a search using the above mentioned example syntax.
