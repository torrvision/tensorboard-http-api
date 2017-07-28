import tensorflow as tf


tf_summary_writers = {}


# def get_summary_writer(runname):
def tb_get_xp_writer(runname, run_folder):
    if runname in tf_summary_writers:
        return tf_summary_writers[runname]

    tb_access_xp(runname)
    writer = tf.summary.FileWriter(run_folder, flush_secs=1)
    tf_summary_writers[runname] = writer
    tb_modified_xp(runname)
    return writer
