# Computer vision hand-controller

This is a side-project I created as a result of me wanting to control Blender by waving my hands in front of the 
screen instead of using keyboard and mouse. Turned out to be loads of fun along the way!

# Quick run

To try it out, just run the main function and have fun. When camera starts, put both hands in front of the screen.

## Gestures
### Left hand

- `Cursor mode` (or rather, hand operated cursor) - make a fist, and then open your hand fully (for a greater 
cool effect do it like you're throwing sand in someone's face, whoosh!). Your monitor will be represented in smaller 
scale on the screen, and you can move hand within those bounds to control the mouse.

- `Thumb + Index` touch - left mouse click (as long as you hold them together, click is active)
- `Thumb + Middle` touch - middle mouse click with a moving gesture. To put it in a human-readable terms, this will enable 
you to move camera around a point in Blender. The farthest you move your touching fingers from where you originally 
connected them, the faster the rotation. When you release and touch again, you set a new origin.

### Right hand

- ``Grab`` (make a fist) - keyboard Shift

- ``Thumb + Index`` - keyboard G (Blender move)
- ``Thumb + Middle`` - keyboard R (Blender rotate)
- ``Thumb + Ring`` - keyboard S (Blender scale)
- ``Thumb + Pinky`` - keyboard E (Blender extrude)

- ``Pointing one`` (index finger up) - keyboard X (isolate X axis)
- ``Pointing two`` (index and middle finger up) - keyboard Y (isolate Y axis)
- ``Pointing three`` (index and middle finger up, thumb pointing out) - keyboard Z (isolate Z axis)

# Concepts and project structure

We start in the `main` function where events and listeners are registered in a following way:

```python
Event: [ 
    Listener,
    Listener2
]
```

Events are representing gestures (indicating something _has happened_), and listeners represent what is to be executed 
after event has happened (indicating to _do something_). I.e. thumb and index finger touched (event), now execute a 
mouse click (listener).

Code has a concept of inverse events which are simply event opposites to be able to trigger an action when opposite happens.
I.e. thumb and index touch is an event, opposite event is thumb and index release. We would, for example, trigger mouse 
click on touch, keep it clicked until release when we'd execute a mouse click release. 

```python
Event: InverseEvent
```

```
root
├── Events
│   └── ...
└── Listeners
    └── ...
```

Next we extract hands (using [MediaPipe](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)) and 
create ``Hand`` objects from them, making sure we separate left and right hand. Each `Hand` has many `Fingers`.

```
root
└── Models
    ├── Fingers
    ├── Hand
    └── MpHands
```

Lastly, we load the gestures. Loading of gestures happens in a way that events are dispatched under certain condition.
So when you see ``Event.when(something happens).dispatch()``, it means (given that this is triggering each frame) that
as long as condition is satisfied, this event will keep on triggering. 

If you registered a reverse event, you don't need to specifically call ``InverseEvent.when(opposite happens).dispatch()``,
it will happen behind the scenes.

One thing to mention is that although events will keep on firing each and every frame the condition is satisfied, 
listeners will fire either:
- each and every frame 
- once

The determining factor is what I call a ``flip_flop`` mode on `Listener` object. If turned on, it will make sure to flip
the listener only once per satisfied event. Only when inverse event is triggered will that state return to false enabling
it to be fired next time the condition is satisfied. ``flip_flop`` is false by default, meaning it is operating in "stream"
mode. 

Some examples when this makes sense:
- ``flip_flop`` - mouse click. You want to execute a click once per gesture satisfied, otherwise you'd get X amount of 
clicks.
- ``stream`` - mouse move. You want each frame to read new coordinates and move mouse as long as condition is satisfied,
otherwise you'd get a single mouse nudge and that would be it.

# Contributing

I welcome all to join the project and contribute! 

Also, feel free to reach out with any suggestions, bug reports or objections, those are valuable contributions as well,
and are inspiring me to continue.

Using [Black formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) for code formatting,
but set with 119 line length within `pyproject.toml` file.

Some of TODOs and ideas:
- Stabilize and smoothen the mouse movement (having a hand in front of the camera perfectly still is rather hard)
- Fill out the rest of the gestures still unassigned (probably also test out with Blender what makes the most sense)
- Introduce blocking events (i.e. when cursor mode is active, and you enter camera move, 
disable cursor mode until you release the camera)
- Introduce new point left, right, up, down gestures to enable Blender camera view front, back, up, down
- Introduce complex modes (i.e. have one set of gestures when cursor mode is active, and other set when inactive)
- Introduce dynamic sensitivity for cursor mode (i.e. when cursor mode is active, do some gesture with right hand to make
drawn canvas bigger or smaller for finer or faster mouse movements)
- Flip hands through config
- Improve UX by dynamically changing points on hands which are currently active, and other which can be activated 
within that mode
- Prevent detecting random movements as gestures (i.e. drinking coffee in front of the screen would trigger events)
- (continuous) Measure the time of the functions and make sure that all actions are smooth and non-blocking 


