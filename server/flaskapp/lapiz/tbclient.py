import tensorflow as tf


tf_summary_writers = {}


# def get_summary_writer(runname):
def get_summary_writer(runname, run_folder):
    if runname in tf_summary_writers:
        return tf_summary_writers[runname]

    writer = tf.summary.FileWriter(run_folder, flush_secs=1)
    tf_summary_writers[runname] = writer
    return writer


def write_summaries(runname, run_folder, json_payload):
    writer = get_summary_writer(runname, run_folder)

    wall_time = json_payload.get('wall_time')
    step = json_payload.get('step')

    summaries = []
    for jsum in json_payload['summaries']:
        if jsum.get('type') == 'scalar':
            s = tf.Summary.Value(tag=jsum['tag'], simple_value=jsum['value'])
        elif jsum.get('type') == 'histogram':
            s = tf.Summary.Value(tag=jsum['tag'], histo=jsum['histo'])
        summaries.append(s)

    summary = tf.Summary(value=summaries)
    event = tf.Event(wall_time=wall_time, step=step, summary=summary)
    writer.add_event(event)
    writer.flush()

    return True
