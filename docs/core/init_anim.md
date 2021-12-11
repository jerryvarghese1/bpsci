## ```init_anim```
Sets up the global animation information such as beginning frame, ending frame, and speed up

```python
anim = bpsc.init_anim(t, speed_up)
```

### Arguments 
```t```: an ```nd.array``` that contains the time information that corresponds with the six degrees of freedom data
<br>```speed_up```: a ```float``` that is the "real time speed up" or the ratio of the duration of the data to the duration of the animation
