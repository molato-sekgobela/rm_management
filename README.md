# rm_management
Tech Assignment (FutureForex)


1. clone the repo to local machine

2. set up a virtual environment and install all the project dependencies found in requirements.txt file
    pip install -r requirements.txt

3. run the python app 
    python manage.py runserver

3. Use the following credetials for RM login on the application
    username: molato10
    password: 948025466Mp@

4. Initially there will be no client linked to the RM logged in. 
    - Add a client using the following details
        client name: cisco networks
        email address: cisconetworks@techwithmolato.co.za ## Please note i have setup these accounts already for demonstration
    - click on add client
        This will send an email to the client (cisconetworks@techwithmolato.co.za) to verify their email address
        only after they have successfully verified their email will the RM be able to send Document Requests
    

RM email access:
    url: https://joseph.happychappy.com/roundcube/?_task=login&_err=session
    username: rm@techwithmolato.co.za
    password: 948025466Mp@

Client email access:
    url: https://joseph.happychappy.com/roundcube/?_task=login&_err=session
    username: cisconetworks@techwithmolato.co.za
    password: 948025466Mp@



Alternatively you can replace the client email  and also  create a new superuser (using django functionality) with different emails

Happy Testing :-) .....



Author Molato Paul Sekgobela