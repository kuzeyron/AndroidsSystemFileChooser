from android import activity, mActivity
from jnius import autoclass
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.properties import BooleanProperty, ListProperty, StringProperty

__all__ = ('SystemFileChooser', )

Intent = autoclass('android.content.Intent')
REQUEST_CODE_OPEN_DOCUMENT = 1


class SystemFileChooser(EventDispatcher):
    '''Class to be used as a object or subclassed.'''

    mime_type = StringProperty('*/*')
    '''Mime type to be used with SystemFileChooser.'''

    multiple = BooleanProperty(False)
    '''Multiple selection with SystemFileChooser.'''

    uris = ListProperty()
    '''Collection of URI's coming from System's own FileChooser.'''

    def trigger(self):
        '''Triggers the System's own FileChooser.'''
        activity.bind(on_activity_result=self._chooser_results)
        intent = Intent(Intent.ACTION_GET_CONTENT)
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, self.multiple)
        intent.setType(self.mime_type)
        mActivity.startActivityForResult(intent, REQUEST_CODE_OPEN_DOCUMENT)

    def _chooser_results(self, requestcode, resultcode, intent):
        '''Activity results triggered by the trigger itself.'''
        activity.unbind(on_activity_result=self._chooser_results)

        if resultcode != -1 or intent is None:
            return  # return nothing because no files selected

        uris = []

        if requestcode == REQUEST_CODE_OPEN_DOCUMENT and resultcode == -1:
            try:
                if (clip_data := intent.getClipData()) is not None:
                    for i in range(clip_data.getItemCount()):
                        uris.append(clip_data.getItemAt(i).getUri())

                elif (clip_data := intent.getData()) is not None:
                    uris.append(clip_data)

                self.uris.extend(uris)

            except Exception as e:
                Logger.error('Error getting file/s: %s', e)
