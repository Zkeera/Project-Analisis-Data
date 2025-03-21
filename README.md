## Setup Environment - Python
```
python -m venv main-ds
main-ds\Scripts\activate
pip install -r requirements.txt
```
## Install Dependencies
---

pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade certifi
import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

---

## Run steamlit app
```
streamlit run dashboard.py
```
