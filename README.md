# Flask-Wallet
Flask API for a Wallet

This is an API for a wallet. It can be used to create a new wallet, login to an account, check balance in the wallet of the user, credit and debit the wallet and check credit and debit logs.

Authentication can be done through a POST request with the ID and password sent through a form. Error code 401 indicates that the request can be done only after authentication.

A UI for Sign up and login is also provided.

###PUT Request for Creating a new Wallet user
This PUT request creates a new user for the Wallet. The URL must consist of the ID, which if clashes with an already existing user, aborts the creation of a new wallet. The form along with the PUT request must consist of

1.Name
2.Phone Number
3.Balance (Must be no less than the minimum balance, failing which the account will not be created)
4.Password for login
BODY raw
{
    "name":"XYZ",
    "PhNo" : 3010101010,
    "balance": 100,
    "password": "xyzxyz"
}


####Example Request                                 				Creating Wallet
curl --location --request PUT 'http://localhost:5000/user/3' \
--data-raw '{
    "name":"XYZ",
    "PhNo" : 3010101010,
    "balance": 100,
    "password": "xyzxyz"
}'

###POSTRequest for Loggin into a  wallet
This POST request is to login to a particular account. The form sent should contain -

1.ID
2.Password
3.remember = True
BODY formdata
ID 1
password admin
remember True


####Example Request										Login Wallet
curl --location --request POST 'http://localhost:5000/login' \
--form 'ID="1"' \
--form 'password="admin"' \
--form 'remember="True"'


###GET Request to check Balance
This GET request requests for the balance of any user The URL must contain the ID of the user whose wallet balance must be checked



####Example Request										Check Balance
curl --location --request GET 'http://localhost:5000/user/1' \
--data-raw ''


###PATCH Request for Debiting Wallet
This PATCH request debits the wallet of the logged in user with a certain amount of money. The form must contain the amount to be debited. If the balance of the user wallet goes below the minimum balance, the amount will not be debited.

BODY raw
{
    "amount":20
}


####Example Request										Debiting Wallet
curl --location --request PATCH 'http://localhost:5000/user/deposit' \
--data-raw '{
    "amount":20
}'


###PATCH Request for Crediting Wallet
This PATCH request credits the wallet of the logged in user with a certain amount of money. The form must contain the amount to be credited.

BODY raw
{
    "amount":10
}


####Example Request										Crediting Wallet
curl --location --request PATCH 'http://localhost:5000/user/withdraw' \
--data-raw '{
    "amount":10
}'


###GET Request to get Credit/Debit Logs
This GET request gets all the credit and debit logs made by the logged in user.



####Example Request										Get Credit/Debit Logs
curl --location --request GET 'http://localhost:5000/user/log'
