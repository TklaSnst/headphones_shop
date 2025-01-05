async function registration(){
    let username = document.getElementById("login-input").value;
    let password1 = document.getElementById("password1").value;
    let password2 = document.getElementById("password2").value;

    if (password1 != password2){
        return alert("Passwords are not same!");
    } else {
        if (password1.length < 8){
            return alert("Password shud contain 8 characters or more");
        } 
    }

    let user = {
        username: String(username),
        password: String(password1)
    }
    const url = 'http://127.0.0.1:8000/auth/registration/';
    let response = fetch(url, {
        method: 'POST',
        body: JSON.stringify(user),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.status == 401){
            console.log('this username is already taken');
        } else if (response.status < 300 && response.status > 199){
            console.log('successful registration');
        }
    })
}


async function login(){
    let username = document.getElementById("login-input").value;
    let password = document.getElementById("password1").value;

    let user = {
        username: String(username),
        password: String(password)
    }
    var url = 'http://127.0.0.1:8000/auth/login/';
    let response = fetch(url, {
        method: 'POST',
        body: JSON.stringify(user),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        console.log(response.json);
        if (response.status < 300 && response.status > 199){
            console.log('successful login');
        }
    }); 
}


async function get_me(){
    const url = 'http://127.0.0.1:8000/auth/users/me/';
    console.log(document.cookie);
    let response = fetch(url, {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${document.cookie}`
        }
    });
}


function basketAdd(){
    
}