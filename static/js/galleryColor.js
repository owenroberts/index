Array.from(document.getElementsByClassName('new-word')).forEach(element => {
	element.style.color = `hsla(${ getRandomInt(120, 350) }, ${getRandomInt(50, 90)}%, ${getRandomInt(50, 70)}%, 1)`;
});