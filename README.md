# The onset of collective motion

This repository models the onset of collective motion using a variety of models including the sandpile model.

## Intuition (What are we concerned with?)

Imagine a herd of wilderbeast grazing on the plains. When one wilderbeast no longer finds enough gras to feed on where it is right now, it may start to move slightly. That may then encumber their conspecifics. That may increase the discomfort of that conspecific and it may in turn decide to move slightly or even run off. The same may go when an animal senses some danger (either by spotting a predator or just generally becoming alarmed). 

Or a bit closer to home: Think of the onset of mass panics or how you might get pulled or pushed into a direction you may not want to follow in crowded places even when everyone is enjoying themselves. 

## Reasoning (Why on earth would we want to study that?)

Groups moving together or individuals breaking away is an interesting phenomenon in nature. 

## The models

### Sandpile model

We use a variant of the well established sandpile model. The sandpile model posits that when you drop sand grain by grain onto a pile of sand, eventually you will start to see avalanches of diverse sizes. We use this intuition to model the agitation of the individuals and their neighbours. The addition of grains is the equivalent of the number of neighbours increasing within the perception radius of the agent. When the number of neighbours surpasses a threshold, the agent will move to an adjacent square to try and escape the pressure. This should lead to the typical avalanches.