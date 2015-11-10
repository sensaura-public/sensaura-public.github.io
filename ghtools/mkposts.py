#!/usr/bin/env python
#----------------------------------------------------------------------------
# Generate a set of sample pages.
#----------------------------------------------------------------------------
from os.path import join, dirname, abspath
from random import choice

# Generated with http://phrasegenerator.com/headlines
TITLES = (
  "20 Dirty Secrets About Needlepoint",
  "12 Naughty Beard Care Tips From Natalie Portman",
  "5 Things Urologists Don't Like To Think About",
  "15 Amazing Secrets Your Electrician Doesn't Know About",
  "10 Sexy Facts That Will Make Your Boyfriend Work Harder",
  "Arnold Schwarzenegger's 6 Windsurfing Secrets",
  "8 Shocking Halo Tips From Martin Scorsese",
  "15 Troubling Truths That Make Plastic Surgeons Feel Ashamed",
  "Agriculture Secretary Thomas J. Vilsack's Top 5 Practical Shopping Tips",
  "The Shocking Truth About Warren Buffet",
  "10 Alarming Things Family Doctors Don't Want You to Know"
  )
  
# Front matter section
FRONT_MATTER = """
---
title: %s
---
"""

CONTENT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam tempus sapien vitae est varius eleifend. Nam ut porttitor orci. Etiam non viverra mi. Mauris consectetur, augue non finibus bibendum, arcu odio porta sapien, et consectetur risus ligula sit amet ante. Mauris consectetur ligula sit amet enim laoreet sagittis. Ut congue mi et nunc luctus aliquet. Maecenas tincidunt imperdiet mauris eget euismod. Ut congue augue pharetra nulla ornare accumsan a at enim.

Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Fusce condimentum sapien bibendum lorem blandit, at gravida nisl eleifend. Quisque aliquet vestibulum ligula, fringilla aliquet elit. Mauris nisl nulla, scelerisque ut nisl nec, condimentum ornare purus. Morbi ac libero id lorem dictum malesuada varius sit amet odio. Integer sed elit in risus porta dictum sit amet non diam. Morbi vitae ante tempus, congue massa eget, tempor eros. Suspendisse ac ex erat. Proin diam magna, iaculis ac semper sed, vulputate at augue. Maecenas venenatis faucibus risus, at lacinia urna fringilla non. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vivamus eleifend lacinia diam, sit amet malesuada dolor bibendum eu. Morbi vulputate vel ligula eget finibus. Nunc euismod et nunc id congue.

Proin nec elementum ex. Phasellus ac purus sed ex pulvinar efficitur congue at lacus. Etiam efficitur, ligula eu ullamcorper pulvinar, massa lorem tincidunt urna, commodo eleifend diam urna non tortor. Sed sit amet lobortis tortor. Ut dignissim malesuada elit vel ullamcorper. Ut sollicitudin mollis felis, vel imperdiet sem. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse placerat lacus eget lectus fringilla, at venenatis enim viverra. Mauris volutpat nec velit eu eleifend. Integer iaculis ante nec luctus euismod. Quisque lacinia risus iaculis tempus mollis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam consectetur blandit neque at pretium. Aliquam dui arcu, efficitur et malesuada vitae, dapibus eget justo.

Vivamus sed enim porta diam blandit pellentesque. Nullam neque est, luctus quis ornare volutpat, maximus id justo. Fusce posuere, nulla a consequat pellentesque, nunc nisi porta risus, vitae maximus turpis neque in risus. Mauris sollicitudin mauris dolor, a venenatis mi sagittis in. Maecenas elementum pellentesque ante imperdiet tempor. Sed volutpat dolor neque, efficitur porta libero aliquam sed. Cras tempus et nibh vel fringilla.

Pellentesque vitae nisi urna. Quisque iaculis orci sed aliquet porta. Fusce consectetur nunc ligula, non lobortis eros varius et. In hac habitasse platea dictumst. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas finibus turpis non nisl consectetur iaculis. Nam in pellentesque justo, eu mollis augue. Etiam sit amet interdum velit, nec elementum ex. Proin venenatis orci accumsan, eleifend leo vestibulum, gravida mi. Aliquam ac convallis augue. Morbi nulla eros, rutrum vel augue non, eleifend sagittis lacus. Aenean imperdiet nisl nisi, in cursus velit lacinia et. Morbi quis nulla non nisi pharetra malesuada vitae sit amet felis. Curabitur ut venenatis arcu. Integer congue quis odio sed posuere.
"""

def generatePost(postdir, num):
  with open(join(postdir, "2012-12-%02d-sample.md" % num), "w") as output:
    output.write(FRONT_MATTER.strip() % choice(TITLES))
    output.write(CONTENT)
    
if __name__ == "__main__":
  posts = join(abspath(join(dirname(__file__), "..")), "_posts")
  for x in range(1, 30):
    generatePost(posts, x)
    