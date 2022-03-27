+++
url = "2022/03/27/meet_hugo/"
title = "Meet Hugo"
date = "2022-03-27"
tags = ["kendra creates"]
topics = ["coding"]
description = ""
+++

When I first set up Kendra Creates, I went with the lowest barrier-to-entry: GitHub Pages, Jekyll, and a simple Jekyll theme. I made some changes and got everything set up, and quickly realized that I wanted something fuller featured. My husband, [@dpendolino](https://github.com/dpendolino), recommended switching from Jekyll to Hugo to take full advantage of its features including post taxonomies and syntax highlighting. So I embarked on the process of switching to Hugo.

I got hugo installed on my Chromebook and spent a day or so playing with different themes trying to find one I liked as a starting point. I eventually settled on Blackburn - you can see screenshots of the theme's default styling [here](https://themes.gohugo.io/themes/blackburn/). With the base chosen, it was time for me to add my personal touches.

# My Customizations

Here's a brief rundown of the changes I've made.

## Cover Photo

First off the bat, I added the gorgeous cover image you see ^ up there ^. The base theme didn't have any kind of cover photo as part of the template, so I added it to the layouts and added styles to support it. Nearly every other change I've made to the theme is to align it better with the cover photo. I even picked a cute little unicode flower to replace the calendar icon: ✿.

This photo was taken by talented photographer and dear friend [Lara Santaella](https://prints.larasantaella.es/), and I absolutely love it. Every time I see this photo, I feel a sense of peace, and I wanted to share that with you all. 

## Colors

Every color in this theme, from the background and menu bar to the text colors and syntax highlighting, is chosen directly from or inspired by the cover image. Everything in the kendra.css and syntax.css stylesheets is customized with these colors. So far, I only have a light theme, but I plan to add a dark theme and dark theme support soon(ish).

## Fonts

I skimmed a list of web safe fonts trying to find something that I really liked, but came up short. So I checked Google Fonts and found Raleway. Came back to the template and discovered that it was already using Raleway for headings - that's probably part of what drew me to it in the first place! Anyway I wanted to use it basically everywhere, so I set that up.

## Menus

I tweaked the menus, including adding an entry for my [Curriculum Vitae](../cv/). Most of this was basic configuration, like setting up information for my social media accounts. I also customized the section after the copyright to clarify that while this page is built with Hugo and based on the [Blackburn](https://github.com/yoshiharuyamashita/blackburn) theme, it contains my own customizations and again, the lovely work of [Lara Santaella](https://prints.larasantaella.es/).

# My Learning Experiences

Setting up the blog in Jekyll was very easy, as was setting it up in Hugo. But converting from Jekyll to Hugo had its dicey moments. The first of these was that instead of starting from a clean slate, I tried to convert from Jekyll to Hugo in situ. I also skimped on branching (_I know, **I know**_). This, combined with coding too late at night, led to a bit more chaos than I generally like. Luckily [@dpendolino](https://github.com/dpendolino) was able to help me untangle the mess I'd made, and I started over with a clean slate and much more success.
