local plain = require("classes.plain")
local booklet = pl.class(plain)
booklet._name = "booklet"

booklet.defaultFrameset = {
  content = {
    top = "5%ph",
    left = "0.8in",
    right = "width(page) - 0.8in",
    bottom = "93%ph"
  },
  folio = {
    top = "95%ph",
    left = "left(page)",
    right = "right(page)",
    bottom = "97%ph"
  }
}

function booklet:_init(options)
  plain._init(self, options)
  self:loadPackage("counters")
  self:loadPackage("color")
  self:loadPackage("raiselower")
  self:loadPackage("pdf")
  self:loadPackage("tableofcontents")
end


function booklet:registerCommands()
  plain.registerCommands(self)

  self:registerCommand("chapter", function(options, content)
    SILE.typesetter:leaveHmode()
    SILE.call("goodbreak")

    SILE.call("increment-multilevel-counter", { id = "sectioning", level = 1 })
    SILE.call("tocentry", { level = 1, number = self:getMultilevelCounter("sectioning") }, SU.subContent(content))

    SILE.call("par")
    SILE.call("noindent")
    SILE.call("center", nil, function ()
      SILE.call("font", { size = "24pt" }, content)
    end)
    SILE.typesetter:leaveHmode()
    SILE.call("nobreak")
    SILE.call("medskip")
    SILE.call("nobreak")

    SILE.call("noindent")
    SILE.typesetter:inhibitLeading()
  end)

  self:registerCommand("vref", function(options, content)
    return SILE.call("raise", { height = "4pt" }, function()
      SILE.call("color", { color = "#dddddd" }, function()
        SILE.call("font", { size = "8pt" }, content)
      end)
    end)
  end)

  self:registerCommand("gap", function(options, content)
    return SILE.typesetter:typeset("…")
  end)
end

return booklet
