meSpeak.loadConfig("/static/js/synth/mespeak_config.json");
meSpeak.loadVoice("/static/js/synth/en.json");

let spoken;
//translate
const mappings = [
	{ 'src': /^\s*\//g, 'dest': '' },
	{ 'src': /\/\s*$/g, 'dest': '' },

	{ 'src': /(\.)/g, 'dest': '%' },
	{ 'src': /(\u02c8)/g, 'dest': '\'' },
	{ 'src': /(\u02cc)/g, 'dest': ',' },
	{ 'src': /(\u0251)/g, 'dest': 'A:' },
	{ 'src': /(\u02d0)/g, 'dest': ':' },
	{ 'src': /(\u0251\u02d0)/g, 'dest': 'A' },
	{ 'src': /(\u0251\u0279)/g, 'dest': 'A' },
	{ 'src': /(a\u02d0)/g, 'dest': 'A' },

	// feedback from formantzero via r/linguistics
	{ 'src': /(\u0329)/g, 'dest': 'r' },  
	
	// feedback from scharfes_s via r/linguistics
	{ 'src': /(\u027e)/g, 'dest': 't' },  

	{ 'src': /(\xe6)/g, 'dest': 'a' },
	{ 'src': /(a)/g, 'dest': 'a' },
	{ 'src': /(\u028c)/g, 'dest': 'V' },
	{ 'src': /(\u0252)/g, 'dest': '0' },
	{ 'src': /(\u0254)/g, 'dest': '0' },
	{ 'src': /(a\u028a)/g, 'dest': 'aU' },
	{ 'src': /(\xe6\u0254)/g, 'dest': 'aU' },
	{ 'src': /(\u0259)/g, 'dest': '@' },
	{ 'src': /(\u025a)/g, 'dest': '3' },
	{ 'src': /(\u0259\u02d0)/g, 'dest': '3:' },
	{ 'src': /(a\u026a)/g, 'dest': 'aI' },
	{ 'src': /(\u028c\u026a)/g, 'dest': 'aI' },
	{ 'src': /(\u0251e)/g, 'dest': 'aI' },
	{ 'src': /(b)/g, 'dest': 'b' },
	{ 'src': /(t\u0283)/g, 'dest': 'tS' },
	{ 'src': /(\u02a7)/g, 'dest': 'tS' },
	{ 'src': /(d)/g, 'dest': 'd' },
	{ 'src': /(\xf0)/g, 'dest': 'D' },
	{ 'src': /(\u025b)/g, 'dest': 'E' },
	{ 'src': /(e)/g, 'dest': 'E' },
	{ 'src': /(\u025d)/g, 'dest': '3:' },
	{ 'src': /(\u025c\u02d0)/g, 'dest': '3:' },
	{ 'src': /(\u025b\u0259)/g, 'dest': 'e@' },
	{ 'src': /(e)/g, 'dest': 'E' },
	{ 'src': /(\u025d)/g, 'dest': '3:' },
	{ 'src': /(\u025c\u02d0)/g, 'dest': '3:' },
	{ 'src': /(e\u026a)/g, 'dest': 'eI' },
	{ 'src': /(\xe6\u026a)/g, 'dest': 'eI' },
	{ 'src': /(f)/g, 'dest': 'f' },
	{ 'src': /(\u0261)/g, 'dest': 'g' },
	{ 'src': /(g)/g, 'dest': 'g' },
	{ 'src': /(h)/g, 'dest': 'h' },
	{ 'src': /(\u026a)/g, 'dest': 'I' },
	{ 'src': /(\u0268)/g, 'dest': 'I' },
	{ 'src': /(\u026a\u0259)/g, 'dest': 'i@' },
	{ 'src': /(\u026a\u0279)/g, 'dest': 'i@' },
	{ 'src': /(\u026a\u0279\u0259)/g, 'dest': 'i@3' },
	{ 'src': /(i)/g, 'dest': 'i:' },
	{ 'src': /(i\u02d0)/g, 'dest': 'i:' },
	{ 'src': /(d\u0292)/g, 'dest': 'dZ' },
	{ 'src': /(\u02a4)/g, 'dest': 'dZ' },
	{ 'src': /(k)/g, 'dest': 'k' },
	{ 'src': /(x)/g, 'dest': 'x' },
	{ 'src': /(l)/g, 'dest': 'l' },
	{ 'src': /(d\u026b)/g, 'dest': 'l' }, 
	{ 'src': /(m)/g, 'dest': 'm' },
	{ 'src': /(n)/g, 'dest': 'n' },
	{ 'src': /(\u014b)/g, 'dest': 'N' },
	{ 'src': /(\u0259\u028a)/g, 'dest': 'oU' },
	{ 'src': /(o)/g, 'dest': 'oU' },
	{ 'src': /(o\u028a)/g, 'dest': 'oU' },
	{ 'src': /(\u0259\u0289)/g, 'dest': 'V' },
	{ 'src': /(\u0254\u026a)/g, 'dest': 'OI' },
	{ 'src': /(o\u026a)/g, 'dest': 'OI' },
	{ 'src': /(p)/g, 'dest': 'p' },
	{ 'src': /(\u0279)/g, 'dest': 'r' },
	{ 'src': /(s)/g, 'dest': 's' },
	{ 'src': /(\u0283)/g, 'dest': 'S' },
	{ 'src': /(t)/g, 'dest': 't' },
	{ 'src': /(\u027e)/g, 'dest': 't' },
	{ 'src': /(\u03b8)/g, 'dest': 'T' },
	{ 'src': /(\u028a\u0259)/g, 'dest': 'U@' },
	{ 'src': /(\u028a\u0279)/g, 'dest': 'U@' },
	{ 'src': /(\u028a)/g, 'dest': 'U' },
	{ 'src': /(\u0289\u02d0)/g, 'dest': 'u:' },
	{ 'src': /(u\u02d0)/g, 'dest': 'u:' },
	{ 'src': /(u)/g, 'dest': 'u:' },
	{ 'src': /(\u0254\u02d0)/g, 'dest': 'O:' },
	{ 'src': /(o\u02d0)/g, 'dest': 'O:' },
	{ 'src': /(v)/g, 'dest': 'v' },
	{ 'src': /(w)/g, 'dest': 'w' },
	{ 'src': /(\u028d)/g, 'dest': 'w' },
	{ 'src': /(j)/g, 'dest': 'j' },
	{ 'src': /(z)/g, 'dest': 'z' },
	{ 'src': /(\u0292)/g, 'dest': 'Z' },
	{ 'src': /(\u0294)/g, 'dest': '?' },

	// special edits
	{ 'src': /(k\'a2n)/g, 'dest': 'k\'@n' },
	{ 'src': /(ka2n)/g, 'dest': 'k@n' },
	{ 'src': /(gg)/g, 'dest': 'g' },
	{ 'src': /(@U)/g, 'dest': 'oU' },
	{ 'src': /rr$/g, 'dest': 'r' },
	{ 'src': /3r$/g, 'dest': '3:' },
	{ 'src': /([iU]|([AO]:))@r$/g, 'dest': '$1@' },
	{ 'src': /([^e])@r/g, 'dest': '$1:3' },
	{ 'src': /e@r$/g, 'dest': 'e@' },
	{ 'src': /e@r([bdDfghklmnNprsStTvwjzZ])/g, 'dest': 'e@$1' },

		// edits arising from testing
		{ 'src': /(\'k)+/g, 'dest': 'k\'' },  
		{ 'src': /(\ː)+/g, 'dest': ':' },
		{ 'src': /(\:)+/g, 'dest': ':' },      
		{ 'src': /(ᵻ)/g, 'dest': 'I' },
		{ 'src': /(ɜ)/g, 'dest': '3' },  
		{ 'src': /(ɔ)/g, 'dest': 'O' },  

	// feedback from formantzero via r/linguistics
	{ 'src': /\u0361(.)/g, 'dest': '$1\'' },  
	{ 'src': /3$/g, 'dest': 'R' }
];

const orig = document.getElementById("orig");
const subs = document.getElementById("subs");
let orig_phons = [];


for (let i = 0; i < text.length; i++) {
	for (let j = 0; j < text[i].length; j++) {
		if (orig_phons.indexOf(text[i][j]) == -1) {
			orig_phons.push(text[i][j]);
		}
	}
}

for (let i = 0; i < orig_phons.length; i++) {
	if (!/\s/.test(orig_phons[i])) {
		const phon = document.createElement('div');
		phon.classList.add('orig', orig_phons[i]);
		phon.textContent = orig_phons[i];
		orig.appendChild(phon);
		phon.onmouseover = function() {
			const matches = document.getElementsByClassName(this.classList[1]);
			for (let i = 0; i < matches.length; i++){
				matches[i].classList.add('select');
			}
		};
		phon.onmouseout = function() {
			const matches = document.getElementsByClassName(this.classList[1]);
			for (let i = 0; i < matches.length; i++){
				matches[i].classList.remove('select');
			}
		};

		phon.onclick = function() {
			const matches = document.getElementsByClassName(this.classList[1]);
			process(this.textContent);
			for (let i = 0; i < matches.length; i++){
				if (matches[i] != this)
					matches[i].classList.add('choice');
			}
		};
	}
}


for (let i = 0; i < mappings.length; i++) {
	//console.log(mappings[i].src.toString());
	//console.log(String.fromCharCode(mappings[i].src.toString().substring(4,8)));
	let ch = '';
	let c = mappings[i].src.toString().split('(')[1];
	if (c) {
		c = c.split(')')[0];
		if (c.includes('\\')) {
			c = c.split('\\');
			//console.log(c);
			if (c[0].length == 1) {
				makePhonChoice(c[0]);
			}
			for (let j = 1; j < c.length; j++) {
				if (c[j].includes('u0')) {
					makePhonChoice(String.fromCharCode(c[j].replace('u0','')));
				} else if (c[j].includes('x')){
					makePhonChoice(String.fromCharCode('0' + c[j]));
				} else {
					console.log(c[j])
				}
			}
		} else {
			makePhonChoice(c);
		}
	}
}

function makePhonChoice(ch) {
	const phon = document.createElement('div');
	phon.classList.add('subs');
	phon.textContent = ch;
	subs.appendChild(phon);
	phon.onclick = function() {
		const matches = document.getElementsByClassName('choice');
		process(this.textContent);
		for (let i = 0; i < matches.length; i++){
			const original = matches[i].textContent;
			const replace = this.textContent
			matches[i].textContent = replace;
			matches[i].parentNode.dataset.sentence = matches[i].parentNode.dataset.sentence.replace(new RegExp(original,'g'), replace);
		}
	}
}

function process(uipa) {
	// nothing to process      
	if (uipa == null || uipa.length == 0) {
		return;
	}

	for (var i = 0; i < mappings.length; i++) {
		uipa = uipa.replace(mappings[i].src, mappings[i].dest);
		//console.log(mappings[i].src)
		//console.log(uipa);
		//console.log(mappings[i].src + uipa);
	}
	console.log(uipa);
	spoken = meSpeak.speak('[['+uipa+']]', { 'rawdata': 'mime', 'speed': 75, 'variant': "f3" });
	if (spoken == null) {
		alert("An error occurred: speaking failed.");
	}
	meSpeak.play(spoken);
}



var words = document.getElementsByClassName("phon_word");
for (let i = 0; i < words.length; i++) {
	words[i].addEventListener("click", function() {
		process(this.dataset.word);
	});
}

var playButtons = document.getElementsByClassName('play');
for (let i = 0; i < playButtons.length; i++) {
	playButtons[i].addEventListener("click", function() {
		var sentence = this.parentNode.dataset.sentence;
		process(sentence);
	});
}