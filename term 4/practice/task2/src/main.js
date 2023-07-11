import { Tree } from './bst.js'
import p5 from 'p5'

// Формирование последовательного изображения фракталов (G шагов генерации) с отображением формирующихся уровней на дереве
// Клетки на основе креста
// Фрактал и дерево в разных окнах

new p5((p5) => {
  const width = 1000
  let fractalWidth = width / 2
  let fractals = []
  const tree = new Tree()
  let points
  let blackSquares
  let whiteSquares

  p5.setup = () => {
    p5.createCanvas(1600, 1600)
    blackSquares = p5.createGraphics(500, 500)
    whiteSquares = p5.createGraphics(500, 500)
    blackSquares.background(51)
    tree.addValue(blackSquares.get(), 51)
    blackSquares.background(200)

    const fr = new Fractal(0, 0, fractalWidth, 51)
    fractals.push(fr)
  }

  p5.mousePressed = () => {
    let next = []
    for (let i = 0; i < fractals.length; i++) {
      let fr = fractals[i]
      let newFractals = fr.generate()
      next = next.concat(newFractals)
    }
    fractals = next
    updateTree()
  }

  p5.draw = () => {
    p5.background(200)
    for (let i = 0; i < fractals.length; i++) {
      fractals[i].show(p5)
    }
    let pts = points
    if (pts) {
      pts.forEach((point) => {
        p5.push()
        p5.translate(point.x, point.y)
        p5.image(point.value, 0, 0, 100, 100)
        p5.pop()
        if (point.parent) {
          p5.stroke(51)
          p5.line(point.x, point.y + 10, point.parent.x, point.parent.y + 10)
        }
      })
    }
  }

  function updateTree() {
    for (let i = 0; i < fractals.length; i++) {
      if (fractals[i].color === 255) {
        fractals[i].show(whiteSquares)
      } else {
        fractals[i].show(blackSquares)
      }
    }
    tree.addValue(whiteSquares.get(), 255)
    tree.addValue(blackSquares.get(), 51)
    blackSquares.background(200)
    points = tree.getPoints()
  }

  function Fractal(x, y, r_, clr) {
    this.pos = p5.createVector(x, y)
    this.r = r_
    this.color = clr

    this.generate = () => {
      const squares = []
      for (let x = -1; x < 2; x++) {
        for (let y = -1; y < 2; y++) {
          if (this.color === 51) {
            let newR = this.r / 3
            if (x != 0 && y != 0) {
              squares.push(
                new Fractal(
                  this.pos.x + (x + 1) * newR,
                  this.pos.y + (y + 1) * newR,
                  newR,
                  51
                )
              )
            } else {
              squares.push(
                new Fractal(
                  this.pos.x + (x + 1) * newR,
                  this.pos.y + (y + 1) * newR,
                  newR,
                  255
                )
              )
            }
          } else {
            squares.push(this)
          }
        }
      }

      return squares
    }

    this.show = (canvas) => {
      canvas.push()
      canvas.fill(this.color)
      canvas.translate(this.pos.x, this.pos.y)
      canvas.rect(0, 0, this.r, this.r)
      canvas.pop()
    }
  }
})
