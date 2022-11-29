// Variant 19
// A=0.53 B=0.61

// f(x) = B(4-x*x): 0 <= x <= 2
//      = A(x+2): -2 < x < 0

// Integrate from https://mathjs.org/examples/advanced/custom_argument_parsing.js.html
function integrate(f, k, start, end, step) {
	let total = 0;
	step = step || 0.01;
	for (let x = start; x < end; x += step) {
		total += f(x + step / 2, k) * step;
	}
	return total;
}

function idzFunc(x, k, a = 0.53, b = 0.61) {
	if (x <= 2 && x >= 0) {
		return b * (4 - x * x);
	} else if (x > -2 && x < 0) {
		return a * (x + 2);
	}

	return 0;
}

function idzFuncSquare(x, k, a = 0.53, b = 0.61) {
	return idzFunc(x, k, (a = 0.53), (b = 0.61)) ** 2;
}

function idzCoeffAFunc(x, k, a = 0.53, b = 0.61) {
	if (x <= 2 && x >= 0) {
		return b * (4 - x * x) * Math.cos((Math.PI * k * x) / 2);
	} else if (x > -2 && x < 0) {
		return a * (x + 2) * Math.cos((Math.PI * k * x) / 2);
	}

	return 0;
}

function idzCoeffBFunc(x, k, a = 0.53, b = 0.61) {
	if (x <= 2 && x >= 0) {
		return b * (4 - x * x) * Math.sin((Math.PI * k * x) / 2);
	} else if (x > -2 && x < 0) {
		return a * (x + 2) * Math.sin((Math.PI * k * x) / 2);
	}

	return 0;
}

function coefficientA(k) {
	const result = [];

	for (let i = 0; i < k; i++) {
		result.push((1 / 2) * integrate(idzCoeffAFunc, k, -2, 2));
	}

	return result;
}

function coefficientB(k) {
	const result = [];

	for (let i = 0; i < k; i++) {
		result.push((1 / 2) * integrate(idzCoeffBFunc, k, -2, 2));
	}

	return result;
}

function particalSum(n, a0, coeffsA, coeffsB) {
	let result = `${a0 / 2} `;

	for (let k = 0; k < n; k++) {
		result += `+ ${coeffsA[k]} * \\cos(${k + 1} * x) + ${
			coeffsB[k]
		} * \\sin(${k + 1} * x)`;
	}

	return result + "\\{-2 < x <= 2\\}";
}

function particalSumSquare(n, a0, coeffsA, coeffsB) {
	let result = a0 ^ (2 / 2);

	for (let k = 0; k < n; k++) {
		result += coeffsA[k] ** 2 + coeffsB[k] ** 2;
	}

	return result;
}

function deviations(n, a0, coeffsA, coeffsB) {
	return Math.sqrt(
		(1 / 2) * integrate(idzFuncSquare, 0, -2, 2) -
			particalSumSquare(n, a0, coeffsA, coeffsB)
	);
}

const coeffsA = coefficientA(20);
const coeffsB = coefficientB(20);
const a0 = integrate(idzFunc, 0, -2, 2) / 2;
const s1 = particalSum(1, a0, coeffsA, coeffsB);
const s5 = particalSum(5, a0, coeffsA, coeffsB);
const s20 = particalSum(20, a0, coeffsA, coeffsB);
const d1 = deviations(1, a0, coeffsA, coeffsB);
const d5 = deviations(5, a0, coeffsA, coeffsB);
const d20 = deviations(20, a0, coeffsA, coeffsB);

// Graphics
const devs = document.getElementById("deviations");
const elt = document.getElementById("calculator");
const calculator = Desmos.GraphingCalculator(elt);

devs.textContent = `D1 = ${d1}; D5 = ${d5}; D20 = ${d20}`;

calculator.setExpression({
	id: "graph1",
	latex: "0.61*(4-x*x)\\{0 <= x <= 2\\}",
	color: Desmos.Colors.BLUE,
});

calculator.setExpression({
	id: "graph2",
	latex: "0.53*(x + 2) \\{-2 < x < 0\\}",
	color: Desmos.Colors.BLUE,
});

calculator.setExpression({
	id: "graph3",
	latex: s1,
	color: Desmos.Colors.RED,
});

calculator.setExpression({
	id: "graph4",
	latex: s5,
	color: Desmos.Colors.GREEN,
});

calculator.setExpression({
	id: "graph5",
	latex: s20,
	color: Desmos.Colors.BLACK,
});
