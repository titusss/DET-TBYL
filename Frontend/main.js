
var emotion = 'neutral';
const body = document.body;
const pupils = document.getElementById('pupils');

// Set eye blinking.
// window.addEventListener('mousemove', (evt) => {
//     const x = (evt.pageX - (window.innerWidth / 2)) / 110;
//     const y = 50 + (evt.pageY - (window.innerHeight / 2)) / 35;
//     pupils.style.top = `${y}%`
//     pupils.style.left = `${x}%`;

//     console.log(x,"     ",y)
// });

// Function for adding and removing CSS classes for setting emotion.
function updateCssClass(targetID, newCssClass) {
    const element = document.getElementById(targetID);
    element.className = ''; //remove all css styles
    if(newCssClass) {
        element.classList.add(newCssClass)
    }
}

function setEmotion() {
    // Main program for deciding which emotion to set.
    const message = emotion.split(";");
    const message_x = message[0]
    const message_y = message[1]
    const message_emotion = message[2]
    const x = -(message_x-0.5)*20
    const y = (message_y-0.5)*20 + 50;
    console.log(x,"     ",y)

    pupils.style.top = `${y}%`
    pupils.style.left = `${x}%`;

    emotion = message_emotion

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
// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:5678');

// Connection opened
socket.addEventListener('open', function (event) {
    socket.send('Hello Server!');
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
    emotion = event.data;
    setEmotion();
});