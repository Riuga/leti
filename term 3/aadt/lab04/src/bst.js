import { Node } from "./bstnode.js";

export class Tree {
	constructor() {
		this.root = null;
	}

	isEmpty() {
		return this.root ? false : true;
	}

	addValue(val) {
		const n = new Node(val);
		n.level = 1;

		if (this.isEmpty()) {
			this.root = n;
			this.root.x = 1000 / 2;
			this.root.y = 16;
		} else {
			this.root.addNode(n);
		}
	}

	getMin() {
		if (this.isEmpty()) {
			return;
		}

		let min = this.root;

		while (min.left) {
			min = min.left;
		}

		return min.value;
	}

	getMax() {
		if (this.isEmpty()) {
			return;
		}

		let max = this.root;

		while (max.right) {
			max = max.right;
		}

		return max.value;
	}

	getElement(val) {
		return this.root.search(val);
	}

	removeElement(val) {
		if (this.getElement(val) === null) {
			return;
		}

		this.root.removeNode(this.getElement(val));
	}

	remove(value) {
		this.root = this.removeNode(this.root, value);
	}

	removeNode(current, value) {
		if (current === null) return current;

		if (value === current.value) {
			if (current.left === null && current.right === null) {
				return null;
			} else if (current.left === null) {
				return current.right;
			} else if (current.right === null) {
				return current.left;
			} else {
				let tempNode = this.getMin(current.right);
				current.value = tempNode.value;
				current.right = this.removeNode(current.right, tempNode.value);

				return current;
			}
		} else if (value < current.value) {
			current.left = this.removeNode(current.left, value);

			return current;
		} else {
			current.right = this.removeNode(current.right, value);

			return current;
		}
	}

	inorderTraverse(output) {
		this.root.inorder(output, []);
	}

	preorderTraverse(output) {
		this.root.preorder(output);
	}

	postorderTraverse(output) {
		this.root.postorder(output);
	}

	breadthTraverse(output) {
		this.root.breadth(output, []);
	}

	getPoints() {
		this.root.setCoordinates();
		const points = [];
		this.root.getPoints(points);
		return points;
	}
}
