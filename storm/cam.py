import gobject
import pygst
pygst.require('0.10')
import gst

class VidServer:
    def __init__(self, config):
        log = config.get('log_facility')
        src = gst.element_factory_make("v4l2src")
        src.set_property("device", "/dev/video6")

        enc = gst.element_factory_make("TIVidenc1")
        enc.set_property("codecName", "mpeg4enc")
        enc.set_property("engineName", "codecServer")

        pay = gst.element_factory_make("rtpmp4vpay")

        sink = gst.element_factory_make("udpsink")
        host = config.get('video', 'bind_host')
        port = config.getint('video', 'bind_port')
        sink.set_property("host", host)
        sink.set_property("port", port)
        log.info("udpsink pointed at %s:%d" % (host, port))

        pipeline = gst.Pipeline("pipeline")
        pipeline.add(src, enc, pay, sink)
            
        src.link(enc)
        enc.link(pay)
        pay.link(sink)

        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        log.info("Initialized video streaming server.")

        self.pipeline = pipeline
        self.log = log
        self.config = config

    def on_message(self, bus, message):
        if message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            self.log.warn("Error: %s" % err, debug)
            self.pipeline.set_state(gst.STATE_NULL)
               
    def play(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def pause(self):
        self.pipeline.set_state(gst.STATE_PAUSED)

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)

