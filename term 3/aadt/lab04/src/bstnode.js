export class Node {
	constructor(val, x, y) {
		this.value = val;
		this.left = null;
		this.right = null;
		this.parent = null;
		this.x = x;
		this.y = y;
		this.level;
	}

	addNode(n) {
		n.level++;
		if (n.value < this.value) {
			if (this.left === null) {
				this.left = n;
				this.left.parent = this;
			} else {
				this.left.addNode(n);
			}
		} else if (n.value > this.value) {
			if (this.right === null) {
				this.right = n;
				this.right.parent = this;
			} else {
				this.right.addNode(n);
			}
		}
	}

	setCoordinates() {
		if (this.left) {
			this.left.x = this.x - 500 / 2 ** this.level;
			this.left.y = this.y + 20 * this.level;
			this.left.parent = this;
			this.left.setCoordinates();
		}

		if (this.right) {
			this.right.x = this.x + 500 / 2 ** this.level;
			this.right.y = this.y + 20 * this.level;
			this.right.parent = this;
			this.right.setCoordinates();
		}

	}

	findMinNode(n) {
		if (n.left === null) {
			return n;
		}

		return this.findMinNode(n.left);
	}

	getPoints(points) {
		if (this.left != null) {
			this.left.getPoints(points);
		}

		points.push({
			x: this.x,
			y: this.y,
			parent: this.parent,
			value: this.value,
		});

		if (this.right != null) {
			this.right.getPoints(points);
		}
	}

	inorder(output) {
		if (this.left != null) {
			this.left.inorder(output);
		}
		output.textContent += `${this.value} `;
		
		if (this.right != null) {
			this.right.inorder(output);
		}
	}

	preorder(output) {
		output.textContent += `${this.value} `;
		if (this.left != null) {
			this.left.preorder(output);
		}
		if (this.right != null) {
			this.right.preorder(output);
		}
	}

	postorder(output) {
		if (this.left != null) {
			this.left.postorder(output);
		}
		if (this.right != null) {
			this.right.postorder(output);
		}
		output.textContent += `${this.value} `;
	}

	breadth(output, queue) {
		if (this.left) {
			queue.push(this.left);
		}
		if (this.right) {
			queue.push(this.right);
		}

		output.textContent += `${this.value} `;
		if (queue.length != 0) {
			queue.shift().breadth(output, queue);
		}
	}

	search(val) {
		if (this.value == val) {
			return this;
		}

		if (val < this.value && this.left != null) {
			return this.left.search(val);
		}

		if (val > this.value && this.right != null) {
			return this.right.search(val);
		}

		return null;
	}
}
