# Affiliate Search (backend)

A simple python backend housing three api calls:
* A **list** request that will return all affiliates in the databse
  * Example: http://127.0.0.1:8000/affiliates/
* A **get** request that will return one affiliate by id from the database
  * Example: http://127.0.0.1:8000/affiliates/1
* A **get** request that takes a *affiliate_name* and *page* and returns gym leaderboard statistics
  * Example: http://127.0.0.1:8000/affiliate_leaderboard/?affiliate_name=CrossFit+DC&page=1

---

## Setup Instructions

1. Ensure that you have python 3.7+ installed by running ```python --version```
2. Ensure that you have pip installed by running ```pip --version```
3. Clone the repository
4. Open the parent folder in the command line and run ```pip install -r requirements.txt```
5. Then run the command ```python manage.py runserver```

You should now be able to call all three APIs
