function countdown(){
    let theDate = new Date('Dec 31, 2022 11:00:00').getTime()
    
    let x = setInterval(function () {
        let now = new Date().getTime();

        let distance = theDate - now;

        let days = Math.floor(distance / (1000 * 60 * 60 * 24));
        let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById('countdown').innerHTML = '<h1 class="font-secondary display-4" id="countdown">'+days + ' ngày ' + hours + ' giờ ' + minutes + ' phút'+'</h1>';

        if(distance < 0){
            clearInterval(x);
        }
    }, 1000);
}