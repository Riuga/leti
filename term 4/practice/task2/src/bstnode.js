export class Node {
  constructor(val, color, x, y) {
    this.value = val
    this.left = null
    this.right = null
    this.parent = null
    this.color = color
    this.x = x
    this.y = y
    this.level
  }

  addNode(n) {
    n.level++
    if (n.color === 51) {
      if (this.left === null) {
        this.left = n
        this.left.parent = this
      } else {
        this.left.addNode(n)
      }
    } else if (n.color === 255) {
      if (this.right === null) {
        this.right = n
        this.right.parent = this
      } else {
        this.left.addNode(n)
      }
    }
  }

  setCoordinates() {
    if (this.left) {
      this.left.x = this.x - 500 / 2 ** this.level
      this.left.y = this.y + 100 * this.level
      this.left.parent = this
      this.left.setCoordinates()
    }

    if (this.right) {
      this.right.x = this.x + 500 / 2 ** this.level
      this.right.y = this.y + 20 * this.level
      this.right.parent = this
      this.right.setCoordinates()
    }
  }

  getPoints(points) {
    if (this.left != null) {
      this.left.getPoints(points)
    }

    points.push({
      x: this.x,
      y: this.y,
      parent: this.parent,
      value: this.value,
    })

    if (this.right != null) {
      this.right.getPoints(points)
    }
  }
}
