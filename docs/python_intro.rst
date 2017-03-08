Python intro
============

If it just so happens that you are interested in Alexa, but don't have much Python experience, don't worry. There isn't that much to know about Python to be able to do an awfull lot.

the 1 minute intro to Python for programmers
--------------------------------------------
Python has variable types such as ints, floats, strings, bytes, lists, dicts and others. Python requires you to use offsets (tabs, or 4-spaces, not mixed though!) for scoping the code.

.. code-block:: pycon

    >>> # this is a comment             # which doesn't get executed
    >>> a = [1, 2, 3]                   # creates a list
    >>> a = a + [4, 5]                  # appends 4 and 5 to the list
    >>> print(a[0])                     # prints the first element of a
    >>> d = {"my_key": "my_value"}      # creates a dict (hash map)
    >>> d["another_key"] = 42           # adds another entry into d
    >>> print(d["my_key"])              # prints "my_value"
    >>> def polite_function(x):         # defines a function returning a string "hi"
    >>>     a = "hi"                    # for a call: polite_function("hello")
    >>>     if x == "hello"             # compares the value of x against "hello"
    >>>         return a                # and if True, greets you back
    >>>     else:
    >>>         return "Pffff!"

Ready for a puzzle?
Try and define a new list "my_list" a new dictionary "my_dict" and new function "my_fun" so that:

.. code-block:: pycon

      >>> print(my_list[2] + " is " + my_dict["what"] + " " + str(my_fun() + 2) + "! :)") # prints "Python is number one! :)"

Now go and change some Alexa skills!

the 15 minute Intro to Python for non-programmers
-------------------------------------------------

One beautiful thing about programming is that it's very reliable! The computer isn't like a puppy, it will always do what you tell it to, not just maybe, and not just sometimes. Now, if that would be true literally, you wouldn't have to read this introduction and you could just have chat with it about what is it you want. Unfortunately, while Alexa is getting smarter, you still have to program your computer to do whatever you want it to do (as of 2017). But in a sense programming is like a chat. You give instructions, and observe what the computer does with them. If you don't like what you see, you modify your instructions, until you are satisfied. These "instructions" are computer code and writing them is what people call "programming". Think of them as cooking recipe that you give the computer. It takes your recipe and provided it understands all the instructions, it executes each instruction in the order you've given it, from start to finish. And that's really it. To start programming in Python you need to know only two things: there are variables (of different types) and there are functions. You can think of "variables" in computer code as the same "variables" you learned about in your mathematics class.

You can give it a try by creating a file (recipe) by creating a file called  "first_script.py" in IDLE.
Now write something like:

.. code-block:: pycon

    >>> a = 1
    >>> print(a)
    >>> a = 2
    >>> print(a)
    >>> b = 3
    >>> a = b
    >>> print(a)

Save the file and execute it in the command line by running:

.. code-block:: console

    $ python first_script.py

What is going on here? We create a variable called "a" and set it to 1. Then we print the value of "a". We can also create a variable "b" and then assign "a" to have the value of "b". So far so good. Right? Now comes a tricky bit:

.. code-block:: pycon

    >>> a = 1
    >>> a = a + 1
    >>> print(a)

Ok. So if you replace the variable "a" with its value in the second line you get "1 = 1 + 1" which does not make much sense. Here is where the difference to "variables" you know from school becomes apparent. In mathematics the equal sign "=" means "is equal", while in programming it means "make it equal". So the first line above reads: "Take the value of "a" and make it equal to 1." and the second line reads: "Take the value of "a" and make it equal to the sum of "a" (which is currently 1, set in the previous line) and 1." Hence we are setting "a" to be equal to 2 and then printing it in the last line.

The last bit you need to understand are functions. Fortunately they are super simple to wrap your head around. Think of them as mini-programs (or mini-cooking recipes). You can put them in whichever place you want and then you can execute them whenever you like. Let's try to think of a recipe for making pancakes. We will be adding ingredients and mixing them together. We will create a "mixing" function that we will call at different times:

.. code-block:: pycon

    >>> def mixing():
    >>>     print("Mixing ingredients now...")
    >>>     print("Now they are well mixed again!")
    >>> a = "flour"
    >>> print("adding " + a)
    >>> b = "milk"
    >>> print("adding " + b)
    >>> mixing()
    >>> c = "eggs"
    >>> print("adding " + c)
    >>> mixing()

See how useful the "mixing" function is? We defined it at the very top and then called it whenever we needed it by running "mixing()". This was a very simple function, it didn't do much other than print the same thing, over and over. Functions are great because we can give them our variables and receive a variable in return. Let's try to do that:

.. code-block:: pycon

    >>> def mixing(a, b, c):
    >>>     return "We've made great pancake dough using: " + a + ", " + b + " and " + c + " :)"
    >>> a = "flour"
    >>> print("adding " + a)
    >>> b = "milk"
    >>> print("adding " + b)
    >>> c = "eggs"
    >>> print("adding " + c)
    >>> result = mixing(a, b, c)
    >>> print(result)

If you have made it this far, you should be very proud! You've just seen what is the essence of writing a program. There is much more to learn but most of that deals with what are the right instructions for getting the computer to do what you want. Once you have truly understood why writing code is like writing recipes, you can always google how to make it do what you want.
If there are bits you are unclear about, just go back and make small modifications to see how the computer reacts.

I guess it's also time to let you in on two secrets:

**Firstly,** this guide was never about Python - that's what "the 1 minute intro to Python" is all about. It was a bit about cooking and recipes but mostly about what really happens between you and the computer when you code.

**And secondly,** now that you've learned how coding works, you should learn what to code. Go and fearlessly explore "the 1 minute intro to Python"!