let viewbtn = document.getElementById('view')
let passwordinput = document.getElementById('password')
let icon = document.getElementById('icon')

//
viewbtn.addEventListener("click",() => {
    if (passwordinput.type === 'password'){
        passwordinput.type = 'text'
        icon.className = "fi fi-rr-eye"
    }
    else{
        passwordinput.type = 'password'
        icon.className = "fi fi-rr-eye-crossed"
    }
});