import p5 from 'p5'

let clr
let hexRadius = 20
let rollSpeed = 40.0
let invRadius = 20
let step = 720 * 0.5

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

const rollApply = document
  .querySelector('#roll-apply')
  .addEventListener('click', () => {
    rollSpeed = 1 / document.querySelector('#roll-speed').value
  })

const involuteRadiusApply = document
  .querySelector('#invRad-apply')
  .addEventListener('click', () => {
    invRadius = document.querySelector('#involute-radius').value
  })

const stepApply = document
  .querySelector('#step-apply')
  .addEventListener('click', () => {
    step = 720 * document.querySelector('#step').value
  })

new p5((p5) => {
  let i = 0
  let trajectory = []
  p5.setup = () => {
    p5.createCanvas(1000, 1000)
  }

  p5.draw = () => {
    p5.background(250)
    let invPoints = involute(invRadius, step)
    drawLines(invPoints, 51)
    p5.push()
    p5.translate(invPoints[i].x, invPoints[i].y)
    p5.rotate(p5.frameCount / rollSpeed)
    polygon(0, 0, hexRadius || 20, 6, clr || 51)
    trajectory.push({
      x: (hexRadius - 5) * p5.cos(p5.frameCount / rollSpeed) + invPoints[i].x,
      y: (hexRadius - 5) * p5.sin(p5.frameCount / rollSpeed) + invPoints[i].y,
    })
    p5.pop()

    p5.beginShape()
    p5.stroke(255, 0, 0)
    for (let j = 1; j < trajectory.length; j++) {
      p5.line(
        trajectory[j].x,
        trajectory[j].y,
        trajectory[j - 1].x,
        trajectory[j - 1].y
      )
    }
    p5.endShape()

    i++

    if (i === invPoints.length) {
      i = 0
      trajectory = []
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

  function drawLines(involutePoints, color) {
    p5.stroke(color)
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
