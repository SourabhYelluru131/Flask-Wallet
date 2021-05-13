# Flask-Wallet
Flask API for a Wallet
This is an API for a wallet. It can be used to create a new wallet, login to an account, check balance in the wallet of the user, credit and debit the wallet and check credit and debit logs.
Authentication can be done through a POST request with the ID and password sent through a form. Error code 401 indicates that the request can be done only after authentication.
An optional UI for Sign up and login is also provided.
To set it up locally, install all the dependencies from requirements.txt
Run app.py using python app.py 
Using postman, requests can be sent to the API to register, login, check balance, deposit, withdraw or check balance in a wallet. <br>
POSTMAN COLLECTION => https://www.getpostman.com/collections/a15f3dea4bce61962ab7 <br>
POSTMAN DOCUMENTATION => https://documenter.getpostman.com/view/15749577/TzRUC7y3 <br>

Each kind of request is explained below


## Creating a wallet
PUT Request for Creating a new Wallet user.
This PUT request creates a new user for the Wallet.The form along with the PUT request must consist of<br>
1.Name <br>
2.Phone Number <br>
3.Balance (Must be no less than the minimum balance, failing which the account will not be created)<br> 
4.Password for login <br>
BODY raw <br>
{ "name":"XYZ", <br>
"PhNo" : 3010101010, <br>
"balance": 100, <br>
"password": "xyzxyz" }
 <br>

<img width="699" alt="Screenshot 2021-05-13 at 11 20 58 AM" src="https://user-images.githubusercontent.com/42965936/118083925-6ba43500-b3dd-11eb-91c0-54fb303a92ac.png">


## Log in to wallet
This POST request is to login to a particular account. The form sent should contain - <br>

1.Phone Number <br>
2.Password <br>
3.remember = True <br>
BODY formdata <br>
Phone Number 1234567890 <br>
password admin <br>
remember True <br>

<img width="697" alt="Screenshot 2021-05-13 at 11 21 08 AM" src="https://user-images.githubusercontent.com/42965936/118083918-66df8100-b3dd-11eb-895e-dfc6e8ded3e8.png">


## Check balance
This GET request requests for the balance of any user The URL must contain the ID of the user whose wallet balance must be checked


<img width="838" alt="Screenshot 2021-05-13 at 1 31 13 AM" src="https://user-images.githubusercontent.com/42965936/118037353-5b636a00-b38b-11eb-8237-91bbd6d5c1f9.png">


## Debit from  Wallet 
This PATCH request debits the wallet of the logged in user with a certain amount of money. The form must contain the amount to be debited. If the balance of the user wallet goes below the minimum balance, the amount will not be debited. <br>
```Race condition is handled by flask SQLAlchemy itself``` <br>
BODY raw <br>
{ <br>
    "amount":20 <br>
} <br>


<img width="837" alt="Screenshot 2021-05-13 at 1 31 32 AM" src="https://user-images.githubusercontent.com/42965936/118037767-eb091880-b38b-11eb-8b0a-76f7eb815111.png">


## Credit to Wallet
This PATCH request credits the wallet of the logged in user with a certain amount of money. The form must contain the amount to be credited.

BODY raw <br>
{ <br>
    "amount":10 <br>
} <br>


<img width="833" alt="Screenshot 2021-05-13 at 1 31 43 AM" src="https://user-images.githubusercontent.com/42965936/118037923-17bd3000-b38c-11eb-9b48-385065219a22.png">



## Credit/Debit Logs
This GET request gets all the credit and debit logs made by the logged in user.
<img width="838" alt="Screenshot 2021-05-13 at 1 31 13 AM" src="https://user-images.githubusercontent.com/42965936/118037942-1e4ba780-b38c-11eb-8613-15dd2e912af7.png">

