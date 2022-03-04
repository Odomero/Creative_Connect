var password = document.getElementById("pass");
    var password2 = document.getElementById("pass2");
    var form = document.getElementById("forms");
    var pattern1 = /[A-Z]/
    var pattern2 = /\d+/
    var error1 = ""
    var error2 = ""


    form.addEventListener('submit', function(e){

        var message1 = document.getElementById("message1");

        if (pattern1.test(password.value) == false) {
            var error1 = "Password must contain Uppercase";
            message1.innerHTML = error1
            e.preventDefault()
            
        } else if (pattern2.test(password.value) == false){
            var error1 = "Password must contain a digit";
            e.preventDefault()
            message1.innerHTML = error1

        } else if (password.value != password2.value) {
            var error2 = "Password does not match";
            e.preventDefault()
            var message2 = document.getElementById("message2");
            message2.innerHTML = error2
        } 

    })