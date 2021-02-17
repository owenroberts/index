window.addEventListener('load', function() {

	window.GalleryColor = {
		update: function() {
			Array.from(document.getElementsByClassName('new-word')).forEach(element => {
				element.style.color = `hsla(${ getRandomInt(120, 350) }, ${getRandomInt(50, 90)}%, ${getRandomInt(50, 70)}%, 1)`;
			});
			const color = document.getElementsByClassName('new-word')[0].style.color;
			document.body.style.setProperty('--ui-color', color);
		}
	};

	GalleryColor.update();
	
});