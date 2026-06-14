import tensorflow as tf

from filterflow.resampling.standard.base import StandardResamplerBase


@tf.function
def _systematic_spacings(n_particles, batch_size, seed=None):
    """ Generate non decreasing numbers x_i between [0, 1]

    :param n_particles: int
        number of particles
    :param batch_size: int
        batch size
    :return: spacings
    :rtype: tf.Tensor
    """
    dtype = tf.float64
    float_n_particles = tf.cast(n_particles, dtype)
    if seed is None:
        z = tf.random.uniform((batch_size, 1), dtype=dtype)
    else:
        z = tf.random.stateless_uniform((batch_size, 1), seed=seed, dtype=dtype)
    z = z + tf.reshape(tf.linspace(tf.constant(0., dtype=dtype), float_n_particles - 1., n_particles), [1, -1])
    return z / tf.cast(n_particles, dtype)


class SystematicResampler(StandardResamplerBase):
    def __init__(self, on_log=True, name='StandardResamplerBase'):
        super(SystematicResampler, self).__init__(name, on_log)

    @staticmethod
    def _get_spacings(n_particles, batch_size, seed):
        return _systematic_spacings(n_particles, batch_size, seed)
