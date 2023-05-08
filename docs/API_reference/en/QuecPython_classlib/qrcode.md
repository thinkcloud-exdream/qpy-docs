# qrcode- Display QR Code

Module feature: generate the corresponding QR code according to what you enter.

## Display QR Code

### `qrcode.show`

```python
qrcode.show(qrcode_str,magnification,start_x,start_y,Background_color,Foreground_color)
```

Displays the QR code on LCD.

**Parameter:**

- `qrcode_str` - String type. Content of QR code;
- `magnification  ` - Integer type. Magnification [1,6];
- `start_x ` - Integer type. The starting x coordinate of the QR code;
- `start_y ` - Integer type. The starting y coordinate of the QR code;
- `Background_color` - Integer type. Foreground color (It is set to 0xffff by default);
- `Foreground_color` - Integer type. Background color (It is set to 0x0000 by default).

**Return Value:**

`0` - Successful execution

`-1` - Failed to generate the QR code

`-2` - Failed to magnify

`-3` - Failed to display

