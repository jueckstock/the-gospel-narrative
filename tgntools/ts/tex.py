"""True typsetting with plain TeX output.

Notes:
------

* use \leftskip <fixed amount> and \rightskip <flex glue amount} to place verse text at mid-page with ragged right edges (no rivers)
    * https://www.overleaf.com/learn/latex/Articles/How_to_change_paragraph_spacing_in_LaTeX#The_fundamentals:_parameter_commands_and_examples
* use \llap{\hbox ...} to place reference information to the left of verse paragraphs
    * see pages 30-31 of `TeX for the Impatient` (available via OpenLibrary at archive.org)
* TODO: figure out how to make the book/chapter numbers conditional
    * some refs are non-conditional (e.g., non-contiguous refs that must always be visible)
    * some are conditional and should show up only if they are the first ref on a given page
"""

