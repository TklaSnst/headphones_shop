function reg(){
    // if (pass1 != pass2){
    //     console.log('paroli ne sovpadaiut');
    //     return 0;
    //     // 
    // }

    // if (pass1.length < 8){
    //     console.log('parol dolzhen bit' );
    // }

    // var data = fetch(`${url}/page/usr_win/?tgid=${tgid}&usr_bet=${user_bet}&coefficient=2`).then(
    //     (data) => {const d2 = data.json().then((info) => {
    //         document.getElementById("user_balance").textContent = String(info)
    //     })}
    // );

    let form = document.forms.registration_form;
    let login = form.elements.login.value;
    let password1 = form.elements.password1.value;
    let password2 = form.elements.password2.value;

    console.log(login, password1);


}
