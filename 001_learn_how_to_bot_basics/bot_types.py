class ContentType:
    AUDIO = 'audio'
    PHOTO = 'photo'
    VOICE = 'voice'
    VIDEO = 'video'
    DOCUMENT = 'document'
    TEXT = 'text'
    LOCATION = 'location'
    CONTACT = 'contact'
    STICKER = 'sticker'

class MIMEType:
    APP_FORM = "application/x-www-form-urlencoded"
    APP_JSON = "application/json"
    APP_ZIP = "application/zip"
    APP_PDF = "application/pdf"
    AUDIO_MPEG = "audio/mpeg"
    AUDIO_OGG = "audio/ogg"
    VIDEO_MPEG = "video/mp4"
    TEXT_HTML = "text/html"
    IMG_JPG = "image/jpeg"
    IMG_GIF = "image/gif"
    MULTI_FORM_DATA = "multipart/form-data"

class ParseMode:
    HTML = "HTML"  # https://core.telegram.org/bots/api#html-style
    MD_V2 = "MarkdownV2"  # https://core.telegram.org/bots/api#markdownv2-style
    MD = "Markdown"  # legacy mode https://core.telegram.org/bots/api#markdown-style




