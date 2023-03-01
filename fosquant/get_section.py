import numpy as np
from skimage.util import img_as_uint
import javabridge
import bioformats as bf

myloglevel="ERROR"

def get_section_from_vsi(path, dims, chan, series_hires=8)
    javabridge.start_vm(class_path=bf.JARS)

    rootLoggerName = javabridge.get_static_field("org/slf4j/Logger","ROOT_LOGGER_NAME", "Ljava/lang/String;")
    rootLogger = javabridge.static_call("org/slf4j/LoggerFactory","getLogger", "(Ljava/lang/String;)Lorg/slf4j/Logger;", rootLoggerName)
    logLevel = javabridge.get_static_field("ch/qos/logback/classic/Level",myloglevel, "Lch/qos/logback/classic/Level;")
    javabridge.call(rootLogger, "setLevel", "(Lch/qos/logback/classic/Level;)V", logLevel)

    with bf.ImageReader(path) as reader:
        planes = []
        for z in range(3):
            im = reader.read(c=chan, z=z, series_hires=11, XYWH=dims)
            planes.append(im)

    javabridge.kill_vm()

    img = np.dstack(planes)
    img = img_as_uint(img)

    return img

