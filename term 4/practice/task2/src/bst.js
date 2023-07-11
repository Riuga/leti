import { Node } from './bstnode.js'

export class Tree {
  constructor() {
    this.root = null
  }

  addValue(val, color) {
    const n = new Node(val, color)
    n.level = 1

    if (this.root === null) {
      this.root = n
      this.root.x = 1150
      this.root.y = 16
    } else {
      this.root.addNode(n)
    }
  }

  getPoints() {
    this.root.setCoordinates()
    const points = []
    this.root.getPoints(points)
    return points
  }
}
