Android's SystemFileChooser with Kivy
=====================================

*A tool that uses Android's SystemFileChooser to process materials with the set of tools from Kivy.*


### Buildozer
To include these tools with Buildozer just include `androidssystemfilechooser` in the requirements.


### API
For now it's better if you just read the source/code.
`JavaStream(input_stream)`
`SystemFileChooser(mime_type, multiple)`
`uri_to_extension(uri)`
`uri_to_filename(uri)`
`uri_to_stream(uri)`
`uri_image_to_texture(uri)`


### Permissions and Runtime-permissions
You don't have to state anything.


### Example code of use
```
from androidssystemfilechooser import (SystemFileChooser,
                                       uri_image_to_texture,
                                       uri_to_extension,
                                       uri_to_stream)
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.image import Image

KV = '''
BoxLayout:
    orientation: 'vertical'

    MyTriggerButton:
        multiple: True
        text: 'Choose and execute results!'
        on_release: self.trigger()
'''


class MyTriggerButton(SystemFileChooser, Button):
    mime_type = StringProperty('image/*')

    def on_uris(self, instance, uris):
        for nr, uri in enumerate(uris):
            if nr % 2 == 0:
                with uri_to_stream(uri) as stream:
                    image = CoreImage(stream, ext=uri_to_extension(uri))
                texture = image.texture
            else:
                texture = uri_image_to_texture(uri)
            instance.parent.add_widget(Image(texture=texture))
        self.uris = []


class MyApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    MyApp().run()
```


### License
MIT-Licensed.