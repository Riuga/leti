function insertionSort(data) {
	const dataCopy = [...data];
	for (let i = 1; i < data.length; i++) {
		if (dataCopy[i] < dataCopy[i - 1]) {
			let j = i;
			while (dataCopy[j] < dataCopy[j - 1]) {
				let temp = dataCopy[j];
				dataCopy[j] = dataCopy[j - 1];
				dataCopy[j - 1] = temp;
				j--;
			}
		}
	}

	return dataCopy;
}

function selectionSort(data) {
	const dataCopy = [...data];
	let i = data.length - 1;

	while (i > 0) {
		let max = dataCopy[0];
		let maxIndex = 0;

		for (let j = 0; j <= i; j++) {
			if (dataCopy[j] > max) {
				max = dataCopy[j];
				maxIndex = j;
			}
		}

		let temp = dataCopy[i];
		dataCopy[i] = max;
		dataCopy[maxIndex] = temp;

		i--;
	}

	return dataCopy;
}

function bubbleSort(data) {
	const dataCopy = [...data];
	let i = data.length - 1;

	while (i > 1) {
		let isSwapped = false;

		for (let j = 1; j <= i; j++) {
			if (dataCopy[j] < dataCopy[j - 1]) {
				let temp = dataCopy[j];
				dataCopy[j] = dataCopy[j - 1];
				dataCopy[j - 1] = temp;
				isSwapped = true;
			}
		}

		i--;

		if (!isSwapped) {
			break;
		}
	}

	return dataCopy;
}

function merge(left, right) {
	let result = [],
		l = 0,
		r = 0;

	while (l < left.length && r < right.length) {
		if (left[l] < right[r]) {
			result.push(left[l]);
			l++;
		} else {
			result.push(right[r]);
			r++;
		}
	}

	return result.concat(left.slice(l)).concat(right.slice(r));
}

function mergeSort(data) {
	if (data.length <= 1) {
		return data;
	}

	const mid = Math.floor(data.length / 2);

	const left = data.slice(0, mid);
	const right = data.slice(mid);

	return merge(mergeSort(left), mergeSort(right));
}

function shellSort(data) {
	const dataCopy = [...data];
	let size = dataCopy.length;
	for (let gap = Math.floor(size / 2); gap > 0; gap = Math.floor(gap / 2)) {
		for (let i = gap; i < size; i += 1) {
			let temp = dataCopy[i];

			let j;
			for (j = i; j >= gap && dataCopy[j - gap] > temp; j -= gap) {
				dataCopy[j] = dataCopy[j - gap];
			}

			dataCopy[j] = temp;
		}
	}

	return dataCopy;
}

function quickSort(data) {
	let dataCopy = [...data];

	if (dataCopy.length < 2) {
		return dataCopy;
	}

	let min = 1;
	let max = dataCopy.length - 1;
	let rand = Math.floor(min + Math.random() * (max + 1 - min));
	let pivot = dataCopy[rand];

	const left = [];
	const right = [];

	dataCopy.splice(dataCopy.indexOf(pivot), 1);
	dataCopy = [pivot].concat(dataCopy);

	for (let i = 1; i < dataCopy.length; i++) {
		if (pivot > dataCopy[i]) {
			left.push(dataCopy[i]);
		} else {
			right.push(dataCopy[i]);
		}
	}
	return quickSort(left).concat(pivot, quickSort(right));
}

function jsSort(data) {
	const dataCopy = [...data];

	return dataCopy.sort((a, b) => a - b);
}

function generateData(size) {
	const data = [];
	for (let i = 0; i < size; i++) {
		data.push(Math.floor(Math.random() * 1000));
	}

	return data;
}

function getTime(sort, data) {
	const start = new Date().getTime();
	const sorted = sort(data);
	const end = new Date().getTime();
	return end - start;
}

function draw(x, y, clr) {
	const colors = [
		"#fc0303",
		"#f0fc03",
		"#02f702",
		"#02f7f3",
		"#3322ba",
		"#ab22ba",
		"#000000",
	];

	calculator.setExpression({
		type: "table",
		columns: [
			{
				latex: "x",
				values: x,
			},
			{
				latex: "y",
				values: y,
				dragMode: Desmos.DragModes.XY,
				color: colors[clr],
			},
		],
	});
}

function main() {
	const minSize = Number(document.getElementById("min-el").value);
	const maxSize = Number(document.getElementById("max-el").value);
	const step = Number(document.getElementById("step").value);

	const x = [];
	const insertionSortTime = [];
	const selectionSortTime = [];
	const bubbleSortTime = [];
	const mergeSortTime = [];
	const shellSortTime = [];
	const quickSortTime = [];
	const jsSortTime = [];

	for (let i = minSize; i < maxSize; i += step) {
		let data = generateData(i);

		x.push(i);
		insertionSortTime.push(getTime(insertionSort, data));
		selectionSortTime.push(getTime(selectionSort, data));
		bubbleSortTime.push(getTime(bubbleSort, data));
		mergeSortTime.push(getTime(mergeSort, data));
		shellSortTime.push(getTime(shellSort, data));
		quickSortTime.push(getTime(quickSort, data));
		jsSortTime.push(getTime(jsSort, data));
	}

	draw(x, insertionSortTime, 0);
	draw(x, selectionSortTime, 1);
	draw(x, bubbleSortTime, 2);
	draw(x, mergeSortTime, 3);
	draw(x, shellSortTime, 4);
	draw(x, quickSortTime, 5);
	draw(x, jsSortTime, 6);
}

const elt = document.getElementById("calculator");
const calculator = Desmos.GraphingCalculator(elt);
const start = document.getElementById("start");
start.addEventListener("click", main);
