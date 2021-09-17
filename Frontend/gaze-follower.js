const eye1 = document.querySelector('.eyes');
// const eye2 = document.querySelector('.eye-right')
window.addEventListener('mousemove', (evt) => {
    const x = (evt.pageX - (window.innerWidth / 2)) / 110;
    const y = 50 + (evt.pageY - (window.innerHeight / 2)) / 35;
    console.log(y);
    eye1.style.top = `${y}%`
    eye1.style.left = `${x}%`;
    // eye2.style.transform = `translateY(${y}px) translateX(${x}px)`;
});