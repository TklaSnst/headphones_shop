// let username = document.querySelector("#login-input");
// let password1 = document.querySelector("#password1");
// let password2 = document.querySelector("#password2");
// let submit_button = document.getElementById("submit-button");
// console.log(submit_button);

// submit_button.addEventListener('click', () => {
//     if (password1.value != password2.value){
//         alert("Passwords are not same!");
//     } else {
//         const UserLogin = username.value;
//         const UserPassword = password1.value;
//         console.log(UserLogin, UserPassword);
//     }
// })
    

async function registration(){
    let username = document.getElementById("login-input").value;
    let password1 = document.getElementById("password1").value;
    let password2 = document.getElementById("password2").value;

    if (password1 != password2){
        return alert("Passwords are not same!");
    } else {
        if (password1.length < 8){
            return alert("Password shud contain 8 chars or more");
        } 
    }

    var url = 'http://127.0.0.1:8000/auth/registration/';
    let response = await fetch(url, );
}