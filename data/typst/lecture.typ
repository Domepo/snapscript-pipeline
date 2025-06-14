
#import "@preview/arkheion:0.1.0": arkheion, arkheion-appendices
#let first_person = json(bytes(sys.inputs.first_person))
#let heading = json(bytes(sys.inputs.heading))
#let sections = json(bytes(sys.inputs.sections))


#let first_author_name = first_person.name
#let first_author_uni = first_person.uni
#let first_author_email = first_person.email
#let first_author_phone = first_person.phone

#let title = heading.title
#let abstract = heading.abstract
#let keywords = heading.keywords
#let date = heading.date

#show: arkheion.with(
  title: title,
  authors: (
    (name: first_author_name, email: first_author_email, affiliation: first_author_uni),
  ),
  abstract: abstract,
  keywords: keywords,
  date: date,
)


#for section in sections {
  [= #section.name]
  // #c.content
  for content in section.content {
    if content.type == "image" {
      [#figure(image(content.path,width: content.width * 100%), caption: [#section.name])]
    }
    if content.type == "text" {
      [#content.value]
    }
  }
}
TEST
// #figure(image("/data/cropped/crop_0_camera-4.jpg"), caption: [Schematische Darstellung der Livestream-Ebenen])


