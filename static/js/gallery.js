window.addEventListener('load', function() {

	console.log('{{ embed }}');

	const words = document.getElementsByClassName('new-word');
	const word = document.getElementById('word');
	const prefixDef = document.getElementById('prefix-def');
	const nounDefList = document.getElementById('noun-def-list');
	const gallery = document.getElementById('gallery');
	const progress = document.getElementById('progress');
	const loading = document.getElementById('loading');

	// recursively get text on screen to set timer length
	function getText(element) {
		if (element.textContent) 
			text += element.textContent;
		if (element.children) {
			for (let i = 0; i < element.children.length; i++) {
				getText(element.children[i]);
			}
		}
	}

	window.Gallery = {
		text: '',
		time: 0,
		start: performance.now(),
		timing = false,
		offset = 0,
	};
	
	Gallery.text = getText(gallery);
	Gallery.time = Gallery.text.split(' ').length * 0.3 * 1000;

	Gallery.loadNextWord(reload) {
		progress.style.background = 'transparent';
		loading.style.display = 'block';
			localStorage.setItem('prefix', prefix);
			localStorage.setItem('noun', noun);
		fetch('/random_gallery_word')
			.then(response => { return response.json(); })
			.then(json => {
				console.log(json);
				// const url = `${location.origin}/gallery/word/${json[0]}/${json[1]}`;
				// window.open(url, '_self');
				Gallery.update(json);
			});
	}

	Gallery.update = function(params) {
		const { noun, defs, prefix, prefix_def } = params;
		word.textContent = `${prefix}${noun}`;
		prefixDef.textContent = prefix_def;
		nounDefList.innerHTML = '';
		for (let i = 0; i < defs.length; i++) {
			const li = document.createElement('li');
			li.textContent = defs[i];
			nounDefList.appendChild(li);
		}
		GalleryColor.update();
	};

	const color = document.getElementsByClassName('new-word')[0].style.color;

	var wordInterval = setInterval(function() {
		if (timing) {
			if (performance.now() > start + time) {
				clearInterval(wordInterval);
				loadNextWord(true);
			} else {
				const pct =  100 - (performance.now() - start) / time * 100;
				progress.style.background = `linear-gradient(90deg, ${color} ${pct - 2}%, transparent ${pct + 2}%`;
			}
		}
	}, 1000 / 60);

	
});