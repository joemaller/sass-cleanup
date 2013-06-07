This works but is not quite ready for release. It's up here because I needed access to the files remotely and wanted to test Package Control from multiple systems.

If you're seeing this, [I have a few questions](http://www.sublimetext.com/forum/viewtopic.php?f=6&t=12636&p=49386)

## Sassify or SassBeautifier or Sass and CSS Cleanup
I haven't decided on a name yet.

### What about CSS?

There are a couple options. First, since Sass's SCSS syntax is a strict super-set of css, all normal CSS files can be beautified just like SCSS. 

But, since we're already using Sass, we do CSS one better.


### Other uses

Several other options are available:

1. **Convert SCSS to CSS in place**  
    Converts an SCSS snippet to CSS in place. THis is nice if you're working a quick CSS patch or mockup and have forgotten how to or refuse to write vanilla CSS.

    The source SCSS block can even preserved in a CSS comment for further tweaking.

2. **Compress or expand CSS rules**  
    CSS Rules can be expanded or compressed in addition to standard beautification.
    
### What about Sass Syntax?
First off, Sass is a strict whitespace syntax that uses indentation to define blocks and functionality. Since Sass syntax doesn't work without proper formatting, there's not much need for a beatuifier. 
