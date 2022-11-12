var backgrounds = [
    "url(/static/accounts/images/backgrounds/bg1.jpg) 50% no-repeat",
    "url(/static/accounts/images/backgrounds/bg2.jpg) 50% no-repeat",
    "url(/static/accounts/images/backgrounds/bg3.webp) 50% no-repeat",
    "url(/static/accounts/images/backgrounds/bg4.jpg) 50% no-repeat",
    "url(/static/accounts/images/backgrounds/bg5.jpg) 50% no-repeat",
    "url(/static/accounts/images/backgrounds/bg7.jpg) 50% no-repeat",
    "url(/static/accounts/images/backgrounds/bg9.jpg) 50% no-repeat",
];
var regContainer = document.querySelector('.reg-container')
regContainer.style.background = backgrounds[Math.floor(Math.random() * (backgrounds.length))];
regContainer.style.backgroundSize = 'cover'