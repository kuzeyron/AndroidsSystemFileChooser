from io import RawIOBase

from android import mActivity
from jnius import autoclass
from kivy.graphics.texture import Texture

__all__ = ('JavaStream',
           'uri_to_extension',
           'uri_to_filename',
           'uri_to_stream',
           'uri_image_to_texture')

BitmapFactory = autoclass('android.graphics.BitmapFactory')
BitmapFactoryOptions = autoclass('android.graphics.BitmapFactory$Options')
ByteBuffer = autoclass('java.nio.ByteBuffer')
Intent = autoclass('android.content.Intent')
MediaColumns = autoclass('android.provider.MediaStore$MediaColumns')
MimeTypeMap = autoclass('android.webkit.MimeTypeMap')


class JavaStream(RawIOBase):
    '''Making the stream readable.'''

    def __init__(self, input_stream):
        self._stream = input_stream

    def close(self) -> None:
        self._stream.close()
        super().close()

    def readall(self) -> bytes:
        self._checkClosed()
        buffer_size = self._stream.available()
        buffer = bytearray(buffer_size)
        read_bytes = self.readinto(buffer)
        return bytes(buffer[:read_bytes])

    def readinto(self, buffer) -> int | None:
        self._checkClosed()
        read_bytes = self._stream.read(buffer)

        if read_bytes < 0:  # EOF
            return 0

        return read_bytes


def uri_to_extension(uri):
    '''Returns the extension name from the filename using URI.'''
    return MimeTypeMap.getFileExtensionFromUrl(uri_to_filename(uri))


def uri_to_filename(uri):
    '''Returns the filename from URI. On newer versions it doesn't return the
       correct filename. But you will get the correct extension name.'''
    cursor = mActivity.getContentResolver().query(uri, None, None, None, None)

    if cursor is not None and cursor.moveToFirst():
        filename_index = cursor.getColumnIndex(MediaColumns.DISPLAY_NAME)
        filename = cursor.getString(filename_index) if filename_index != -1 else None
        cursor.close()
        return filename

    return uri.getLastPathSegment()


def uri_to_image(uri):
    '''Open bitmap with the use of URI.'''
    context =  mActivity.getApplicationContext()
    resolver = context.getContentResolver()
    stream = resolver.openInputStream(uri) 
    bitmap = BitmapFactory.decodeStream(stream) 

    return bitmap


def uri_to_stream(uri):
    '''Opens by URI the FileInputStream with JavaStream.'''
    resolver = mActivity.getContentResolver()
    stream = resolver.openInputStream(uri)

    return JavaStream(stream)


def uri_image_to_texture(uri):
    '''Using URI to load the selected image and convert 
       the image to pixels. Returns texture and size.'''
    bitmap = uri_to_image(uri)
    bitmap_size = bitmap.getWidth(), bitmap.getHeight()

    buffer = ByteBuffer.allocateDirect(bitmap.getByteCount())
    bitmap.copyPixelsToBuffer(buffer)
    bitmap.recycle()

    texture = Texture.create(bitmap_size, colorfmt='rgba')
    texture.blit_buffer(bytes(buffer.array()),
                        colorfmt='rgba',
                        bufferfmt='ubyte')
    texture.flip_vertical()

    return texture
