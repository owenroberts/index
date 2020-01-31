Array.from(document.getElementsByClassName('new-word')).forEach(element => {
	element.style.color = `hsla(${ getRandomInt(30,300) }, ${getRandomInt(60, 90)}%, ${getRandomInt(50, 80)}%, 1)`;
});