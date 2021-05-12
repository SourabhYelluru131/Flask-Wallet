# Flask-Wallet
Flask API for a Wallet

This is an API for a wallet. It can be used to create a new wallet, login to an account, check balance in the wallet of the user, credit and debit the wallet and check credit and debit logs.

Authentication can be done through a POST request with the ID and password sent through a form. Error code 401 indicates that the request can be done only after authentication.

A UI for Sign up and login is also provided.

PUT Request for Creating a new Wallet user
This PUT request creates a new user for the Wallet. The URL must consist of the ID, which if clashes with an already existing user, aborts the creation of a new wallet. The form along with the PUT request must consist of

1.Name
2.Phone Number
3.Balance (Must be no less than the minimum balance, failing which the account will not be created)
4.Password for login <br>
BODY raw<br>
{
    "name":"XYZ",
    "PhNo" : 3010101010,
    "balance": 100,
    "password": "xyzxyz"
}

<img width="837" alt="Screenshot 2021-05-13 at 1 30 53 AM" src="https://user-images.githubusercontent.com/42965936/118037151-1808fb80-b38b-11eb-965f-91de630b8a43.png">


POST Request for Logging into a  wallet
This POST request is to login to a particular account. The form sent should contain -

1.ID
2.Password
3.remember = True
BODY formdata <br>
ID 1 <br>
password admin <br>
remember True <br>

<img width="835" alt="Screenshot 2021-05-13 at 1 31 03 AM" src="https://user-images.githubusercontent.com/42965936/118037322-50103e80-b38b-11eb-82f9-6b071e1c6eb9.png">



GET Request to check Balance
This GET request requests for the balance of any user The URL must contain the ID of the user whose wallet balance must be checked


<img width="838" alt="Screenshot 2021-05-13 at 1 31 13 AM" src="https://user-images.githubusercontent.com/42965936/118037353-5b636a00-b38b-11eb-8237-91bbd6d5c1f9.png">


PATCH Request for Debiting Wallet
This PATCH request debits the wallet of the logged in user with a certain amount of money. The form must contain the amount to be debited. If the balance of the user wallet goes below the minimum balance, the amount will not be debited.

BODY raw
{
    "amount":20
}


<img width="837" alt="Screenshot 2021-05-13 at 1 31 32 AM" src="https://user-images.githubusercontent.com/42965936/118037767-eb091880-b38b-11eb-8b0a-76f7eb815111.png">


PATCH Request for Crediting Wallet
This PATCH request credits the wallet of the logged in user with a certain amount of money. The form must contain the amount to be credited.

BODY raw
{
    "amount":10
}


<img width="833" alt="Screenshot 2021-05-13 at 1 31 43 AM" src="https://user-images.githubusercontent.com/42965936/118037923-17bd3000-b38c-11eb-9b48-385065219a22.png">



GET Request to get Credit/Debit Logs
This GET request gets all the credit and debit logs made by the logged in user.
<img width="838" alt="Screenshot 2021-05-13 at 1 31 13 AM" src="https://user-images.githubusercontent.com/42965936/118037942-1e4ba780-b38c-11eb-8613-15dd2e912af7.png">

