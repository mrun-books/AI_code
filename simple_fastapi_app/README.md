## README

How to use this.

1. Once you clone the directory ; you need to install all the apps in requirements.txt file using
   pip install -r requiremnts.txt

2. Create .env at the root level directory which holds all API keys.

- To Run uvicorn server :

---

uvicorn backend.main:app --reload

You should receive message Application startup Complete . Then only it is successfully running the fastapi backend server

- To run streamlit applciation

---

streamlit run .\streamlit_with_fastapi.py
