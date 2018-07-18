from subprocess import Popen, PIPE
from shlex import split

class UnsupportedProtocol(Exception):
    pass

class AVStream(object):
    def __init__(self,
            protocol,
            destination,
            video_device='/dev/video0',
            audio_device='alsa://',
            add_timestamp=True,
            sout=None):
        self.protocol = protocol
        self.destination = destination
        self.video_device = video_device
        self.audio_device = audio_device
        self.add_timestamp = add_timestamp
        self.sout = sout

    def __sout(self, timestamp):
        if self.sout is not None:
            return self.sout
        # remove rtp://
        if self.protocol == 'rtp':
            destination = self.destination.replace('rtp://','')
            return "'#transcode{{vcodec=h264v,venc=x264{{preset=ultrafast,tune=zerolatency,intra-refresh,lookahead=0,keyint=15}},acodec=aac,width=1280,height=720,vb=800,ab=128,deinterlace{timestamp}}}:rtp{{mux=ts,dst={destination}}}'".format(timestamp=timestamp, destination=destination),
        # add rtmp://
        if self.protocol == 'rtmp':
            destination = self.destination
            if not self.destination.startswith('rtmp://'):
                destination = 'rtmp://{destination}'.format(destination=destination)
            return "'#transcode{{vcodec=h264,venc=x264{{preset=ultrafast,tune=zerolatency,intra-refresh,lookahead=0,keyint=15}},scale=auto,width=1280,height=720,acodec=aac,ab=128,channels=2,samplerate=44100{timestamp}}}:std{{access=rtmp,mux=ffmpeg{{mux=flv}},dst={destination}}}'".format(timestamp=timestamp, destination=self.destination)
        return ''

    def __stream_command(self):
        if self.audio_device:
            audio_device = ':input-slave={audio_device}'.format(
                    audio_device=self.audio_device)
        else:
            audio_device = ''

        timestamp=''
        if self.add_timestamp:
            timestamp = ',sfilter=marq{marquee="%Y-%m-%d_%H:%M:%S",position=6}'

        sout = self.__sout(timestamp)
        if not sout:
            raise UnsupportedProtocol(self.protocol)

        command = "vlc v4l2://{video_device} {audio_device} --sout {sout}".format(
                video_device=self.video_device,
                audio_device=audio_device,
                sout=sout)
        print(command)
        command = split(command)
        return command

    def stream(self):
        try:
            command = self.__stream_command()
        except UnsupportedProtocol:
            exit('Unsupported audio-video streaming protocol: {}'.format(self.protocol))
        try:
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            for line in iter(process.stderr.readline, b''):
                print(line)
        except:
            process.kill()

if __name__ == '__main__':
    avstream = AVStream(
        protocol = 'rtmp',
        destination='rtmp://127.0.0.1/live',
        video_device = '/dev/video0',
        audio_device = 'alsa://',
        add_timestamp = True)
    avstream.stream()
