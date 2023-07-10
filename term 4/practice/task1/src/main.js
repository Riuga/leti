import p5 from 'p5'

let clr
let hexRadius

const clrApply = document
  .querySelector('#color-apply')
  .addEventListener('click', () => {
    clr = document.querySelector('#color').value
  })

const radApply = document
  .querySelector('#radius-apply')
  .addEventListener('click', () => {
    hexRadius = document.querySelector('#radius').value
  })

new p5((p5) => {
  const radius = 20
  const divisions = 1440
  const invPoints = involute(radius, divisions)
  let i = 0

  p5.setup = () => {
    p5.createCanvas(1000, 1000)
  }

  p5.draw = () => {
    p5.background(250)
    p5.push()
    drawInvolute(invPoints)
    p5.pop()

    p5.push()
    polygon(invPoints[i].x, invPoints[i].y, hexRadius || 20, 6, clr || 51)
    p5.pop()
    i++

    if (i === invPoints.length) {
      i = 0
    }
  }

  function involute(radius, divisions) {
    let x
    let y
    let deg
    let points = []
    for (let i = 0; i < 719; i = i + 720 / divisions) {
      deg = p5.radians(i)
      x = radius * (p5.cos(deg) + deg * p5.sin(deg))
      y = radius * (p5.sin(deg) - deg * p5.cos(deg))
      points.push({ x: x + 400, y: y + 400 })
    }

    return points
  }

  function drawInvolute(involutePoints) {
    p5.stroke(51)
    p5.strokeWeight(5)
    for (let i = 1; i < involutePoints.length; i++) {
      p5.line(
        involutePoints[i - 1].x,
        involutePoints[i - 1].y,
        involutePoints[i].x,
        involutePoints[i].y
      )
    }
  }

  function polygon(x, y, radius, npoints, color) {
    let angle = p5.TWO_PI / npoints
    p5.beginShape()
    p5.stroke(color)
    p5.fill(color)
    for (let a = 0; a < p5.TWO_PI; a += angle) {
      let sx = x + p5.cos(a) * radius
      let sy = y + p5.sin(a) * radius
      p5.vertex(sx, sy)
    }
    p5.endShape(p5.CLOSE)
  }
})
