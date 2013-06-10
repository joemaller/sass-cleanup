# Sassify or SassBeautifier or Sass and CSS Cleanup
A collection of Sass-based CSS and SCSS tools for Sublime Text 3
I haven't decided on a name yet.

### Main Use
The main function of this package is to clean up CSS and (Sass) SCSS code. Be as sloppy as you'd like while hashing out your styles, then use this package to clean up your code at the end. 

Because Sass's SCSS syntax is a strict super-set of CSS, all normal CSS files can be beautified just like SCSS. 

### Other uses
Several other options are available:

1. **Expand Selection to CSS Rule**  
    This command will expand a selection out to include the current CSS or SCSS rule. For SCSS files, subsequent calls will climb nesting levels, selecting containing parent rules.

1. **SCSS Compile in place**  
    Converts an SCSS snippet to CSS in place. This is nice if you're working a quick CSS patch or mockup and have forgotten how to -- or refuse to --  write vanilla CSS.

    Source SCSS blocks can be preserved in a CSS comment by setting `preserve_scss_in_comment` to true in settings.

2. **Compact or expand CSS rules**  
    CSS Rules can be expanded or compressed in addition to standard beautification. This is smarter than just using Sublime Text's `join_lines` command; multiple rules will compact to individual lines and spacing around rules and brackets will be consistent. 

### Requirements
* **[Ruby](http://www.ruby-lang.org/)**  
The Sass Gem is included, but you'll need to have Ruby installed somewhere for this to work. This package works well with [RubyInstaller](http://rubyinstaller.org) on Windows.
* **[Sass Gem](http://sass-lang.com/)** (Windows only)  
Windows users will also need to install the Sass gem. Mac and Linux users will install a local copy of Sass if one isn't found. 

Including the Gem seems to be working really well, but [I do have a few questions](http://www.sublimetext.com/forum/viewtopic.php?f=6&t=12636&p=49386) about this.


### What about Sass Syntax?
Sass uses a strict whitespace syntax that uses indentation to define blocks and functionality. Since it won't work without proper formatting, there's not much need for a beautifier. 

### What about Sublime Text 2
I don't currently have plans to back-port this to Sublime Text 2, but I'm open to the possibility.