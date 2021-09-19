
var emotion = 'neutral';
const body = document.body;
const pupils = document.getElementById('pupils');

// Set eye blinking.
window.addEventListener('mousemove', (evt) => {
    const x = (evt.pageX - (window.innerWidth / 2)) / 110;
    const y = 50 + (evt.pageY - (window.innerHeight / 2)) / 35;
    pupils.style.top = `${y}%`
    pupils.style.left = `${x}%`;
});

// Function for adding and removing CSS classes for setting emotion.
function updateCssClass(targetID, newCssClass) {
    const element = document.getElementById(targetID);
    element.className = ''; //remove all css styles
    if(newCssClass) {
        console.log(newCssClass);
        element.classList.add(newCssClass)
    }
}

function setEmotion() {
    // Main program for deciding which emotion to set.
    switch(emotion) {
        case 'happy':
            console.log('Emotion: Happy')
            updateCssClass('pupils', null)
            updateCssClass('eyelid-left', 'eyelid-laughing')
            updateCssClass('eyelid-right', 'eyelid-laughing')
            updateCssClass('mouth','mouth-laughing')
            body.style.setProperty('filter', 'hue-rotate(0deg)');
            break
        case 'sad':
            console.log('Emotion: Sad')
            updateCssClass('pupils', 'show')
            updateCssClass('eyelid-left', 'eyelid-left-sad')
            updateCssClass('eyelid-right', 'eyelid-right-sad')
            updateCssClass('mouth','mouth-sad')
            body.style.setProperty('filter', 'hue-rotate(340deg)');
            break;
        case 'sleepy':
            console.log('Emotion: Sleepy')
            updateCssClass('pupils', 'hide')
            updateCssClass('eyelid-left', 'eyelid-sleepy')
            updateCssClass('eyelid-right', 'eyelid-sleepy')
            updateCssClass('mouth','mouth-neutral')
            body.style.setProperty('filter', 'hue-rotate(40deg)');
            break
        default:
            console.log('Emotion: Default')
            updateCssClass('pupils', null)
            updateCssClass('eyelid-left', null)
            updateCssClass('eyelid-right', null)
            updateCssClass('mouth','mouth-neutral')
            body.style.setProperty('filter', 'hue-rotate(110deg)');
            break
    }
}

setEmotion();
var dgram = require('dgram');
var port = 5005;

socket = dgram.createSocket('udp4');

socket.on('message', function (msg, info){
    emotion = msg.toString();
    console.log(emotion);
    setEmotion();
});

socket.on('listening', function(){
    var address = socket.address();
    console.log("listening on :" + address.address + ":" + address.port);
});

socket.bind(port);
