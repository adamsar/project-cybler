class Photo
  
  constructor: (@src, preload, onLoad) ->
    if preload
      @image = $("<img />")[0].src = @src
      if onLoad
        @image.onload = onLoad

class Slideshow
  
  constructor: (imgSelector) ->
    self = @
    @container = $(imgSelector)
    imageCandidates = ($(img).data("src") for img in $("#{imgSelector} div"))
    @photos = [new Photo(imageCandidates[0], true, (event) ->
      self.render()
      )]
    @photos.concat (new Photo img, true, false for img in imageCandidates[1..])
    @renderContainer()

  renderContainer: ->
    height = Math.floor (window.screen.width / 1.33) 
    @container.css {
      width: "device-width"
      height: height
      }