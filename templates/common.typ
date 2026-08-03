// Shared styling for both resumes
#let resume-doc(title: "", body) = {
  set document(title: title)
  set page(
    paper: "a4",
    margin: (top: 1.4cm, bottom: 1.4cm, left: 1.6cm, right: 1.6cm),
  )
  set text(font: ("Noto Sans CJK SC", "Helvetica Neue"), size: 9.5pt, lang: "zh")
  set par(leading: 0.55em, justify: true)
  show heading.where(level: 1): it => {
    v(0.6em)
    block(fill: rgb("#1f3a5f"), inset: (x: 8pt, y: 4pt), width: 100%,
      text(fill: white, weight: "bold", size: 11pt, it.body))
    v(0.2em)
  }
  show heading.where(level: 2): it => {
    v(0.4em)
    block[
      #text(weight: "bold", size: 10pt, fill: rgb("#1f3a5f"), it.body)
      #v(-0.3em)
      #line(length: 100%, stroke: 0.5pt + rgb("#1f3a5f"))
    ]
  }
  show heading.where(level: 3): it => {
    v(0.2em)
    text(weight: "bold", size: 9.8pt, it.body)
  }
  show link: it => text(fill: rgb("#1f3a5f"), underline(it))
  body
}

#let name-header(name-cn, name-en, tagline, contacts) = {
  block[
    #text(size: 20pt, weight: "bold", fill: rgb("#1f3a5f"))[#name-cn #name-en]
    #v(-0.2em)
    #text(size: 10.5pt, fill: rgb("#1f3a5f"), tagline)
    #v(-0.1em)
    #text(size: 8.8pt, contacts)
  ]
}
