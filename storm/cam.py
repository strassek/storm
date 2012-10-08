
import gobject
import pygst
pygst.require('0.10')
import gst

class Vid_Server:
    def __init__(self):
        src = gst.element_factory_make("v4l2src")
	src.set_property("device", "/dev/video6")

        enc = gst.element_factory_make("TIVidenc1")
        enc.set_property("codecName", "mpeg4enc")
        enc.set_property("engineName", "codecServer")

        pay = gst.element_factory_make("rtpmp4vpay")

        sink = gst.element_factory_make("udpsink")
        sink.set_property("host", "192.168.2.3")
        sink.set_property("port", 4000)

        pipeline = gst.Pipeline("pipeline")
        pipeline.add(src, enc, pay, sink)
            
        src.link(enc)
        enc.link(pay)
        pay.link(sink)

        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        self.pipeline = pipeline

    def on_message(self, bus, message):
        if message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.pipeline.set_state(gst.STATE_NULL)
               
    def play(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def pause(self):
        self.pipeline.set_state(gst.STATE_PAUSE)

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)

    def main(self):
        self.pipeline.set_state(gst.STATE_PLAYING)
        loop = gobject.MainLoop()
        loop.run()
        
if __name__ == "__main__":
    srv = Vid_Server()
    srv.main()
