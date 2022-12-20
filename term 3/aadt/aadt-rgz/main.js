// Реализовать сжатие символьных данных и обратную операцию с помощью алгоритма Хаффмана.
function getDictionary(string) {
	return [...string].reduce(
		(symbol, frequency) =>
			symbol[frequency]
				? ((symbol[frequency] = symbol[frequency] + 1), symbol)
				: ((symbol[frequency] = 1), symbol),
		{}
	);
}

function dictionaryToArray(dictionary) {
	return Object.keys(dictionary).map((frequency) => [
		frequency,
		dictionary[frequency],
	]);
}

function sortByFrequency(array) {
	return array.sort((a, b) => a[1] > b[1]);
}

function tree(sorted) {
	return sorted.length < 2
		? sorted[0]
		: tree(
				sortByFrequency(
					[[sorted.slice(0, 2), sorted[0][1] + sorted[1][1]]].concat(
						sorted.slice(2)
					)
				)
		  );
}

const setCodes = (tree, code = "") =>
	tree[0] instanceof Array
		? Object.assign(
				setCodes(tree[0][0], code + "0"),
				setCodes(tree[0][1], code + "1")
		  )
		: { [tree[0]]: code };

const getCodes = (text) =>
	setCodes(tree(sortByFrequency(dictionaryToArray(getDictionary(text)))));

const codesToArray = (text) => dictionaryToArray(getCodes(text));

function toCodes(text, alphabet) {
	let result = "";
	for (let i = 0; i < text.length; i++) {
		alphabet.forEach((pair) => {
			if (text.charAt(i) == pair[0]) {
				result += pair[1];
			}
		});
	}

	return result;
}

function toText(text, alphabet) {
	let result = "";
	let letter = "";
	for (let i = 0; i < text.length; i++) {
		letter += text.charAt(i);
		alphabet.forEach((pair) => {
			if (letter == pair[1]) {
				result += pair[0];
				letter = "";
			}
		});
	}

	return result;
}

const setupBtn = document.getElementById("setup-btn");
const toTextBtn = document.getElementById("to-text-btn");
const toCodesBtn = document.getElementById("to-codes-btn");
const dictionary = document.getElementById("dictionary");
const toCodesOutput = document.getElementById("to-codes-output");
const toTextOutput = document.getElementById("to-text-output");
let alphabet;

setupBtn.addEventListener("click", () => {
	const setupString = document.getElementById("setup").value;
	dictionary.textContent = JSON.stringify(getCodes(setupString));
	alphabet = codesToArray(setupString);
});

toCodesBtn.addEventListener("click", () => {
	const codesToText = document.getElementById("to-codes").value;
	toCodesOutput.textContent = toCodes(codesToText, alphabet);
	console.log(alphabet);
});

toTextBtn.addEventListener("click", () => {
	const textToCodes = document.getElementById("to-text").value;
	toTextOutput.textContent = toText(textToCodes, alphabet);
});
