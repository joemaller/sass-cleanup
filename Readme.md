This works but is not quite ready for release. It's up here because I needed access to the files remotely and wanted to test Package Control from multiple systems.

If you're seeing this, [I have a few questions](http://www.sublimetext.com/forum/viewtopic.php?f=6&t=12636&p=49386)

## Sassify or SassBeautifier or Sass and CSS Cleanup
I haven't decided on a name yet.

### What about CSS?

There are a couple options. First, since Sass's SCSS syntax is a strict super-set of css, all normal CSS files can be beautified just like SCSS. 

But, since we're already using Sass, we do CSS one better.

### Main Use
The main function of this package is to clean up SCSS code. Author however sloppily you'd like, then clean up your code automatically at the end. 
### Other uses

Several other options are available:

1. **Convert SCSS to CSS in place**  
    Converts an SCSS snippet to CSS in place. This is nice if you're working a quick CSS patch or mockup and have forgotten how to -- or refuse to --  write vanilla CSS.

    The source SCSS block can preserved in a CSS comment for further tweaking. (not working yet)

2. **Compress or expand CSS rules**  
    CSS Rules can be expanded or compressed in addition to standard beautification.
    
### Requirements
* **[Ruby](http://www.ruby-lang.org/)**  
The Sass Gem is included, but you'll need to have Ruby installed somewhere for this to work. This package works well with [RubyInstaller](http://rubyinstaller.org) on Windows.
* **[Sass Gem](http://sass-lang.com/)** (Windows only)  
Windows users will also need to install the Sass gem. Mac and Linux users will install a local copy of Sass if one isn't found. 

### What about Sass Syntax?
Sass uses a strict whitespace syntax that uses indentation to define blocks and functionality. Since it won't work without proper formatting, there's not much need for a beautifier. 
