# Damn Small MIDI Matrix
This program converts MIDI notes to hashmap.
For example you can make animation using only MIDI sequencer.

# Requirements
* python3
* pyrtmidi (see [https://github.com/patrickkidd/pyrtmidi](https://github.com/patrickkidd/pyrtmidi) )


## Mapping
Hashmap is a bitmap with resolution 16x8 chars. 

<table border=1>
<tr>
    <td>Row</td>
    <td>Midi note number</td>
</tr>
<tr>
    <td>0</td>
    <td>0-15</td>
</tr>
<tr>
    <td>1</td>
    <td>16-31</td>
</tr>
<tr>
    <td>2</td>
    <td>32-47</td>
</tr>
<tr>
    <td>3</td>
    <td>48-63</td>
</tr>
<tr>
    <td>4</td>
    <td>64-79</td>
</tr>
<tr>
    <td>5</td>
    <td>80-95</td>
</tr>
<tr>
    <td>6</td>
    <td>96-111</td>
</tr>
<tr>
    <td>7</td>
    <td>112-127</td>
</tr>

</table>

