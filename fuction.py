import numpy as np
import sounddevice as sd

# Paramètres
sample_rate = 44100  # Fréquence d'échantillonnage (Hz)
duration = 5.0       # Durée du son (secondes)

# Temps
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Fréquence de base (basse)
base_frequency = 50

# Génération du son avec modulation
sound = np.sin(2 * np.pi * base_frequency * t * (1 + 0.5 * np.sin(2 * np.pi * t / duration)))

# Lecture du son
sd.play(sound, sample_rate)
sd.wait()

import numpy as np
import sounddevice as sd

# Paramètres
sample_rate = 44100  # Fréquence d'échantillonnage (Hz)
duration = 5.0       # Durée du son (secondes)

# Temps
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Fréquences de base pour le bruit de slime
base_freq1 = 100
base_freq2 = 220

# Génération du son pour simuler l'écrasement du slime
sound1 = np.sin(2 * np.pi * base_freq1 * t) * np.sin(2 * np.pi * 0.5 * t)
sound2 = np.sin(2 * np.pi * base_freq2 * t) * np.sin(2 * np.pi * 0.7 * t)
sound = sound1 + sound2

# Ajout d'un bruit blanc pour rendre le son plus réaliste
noise = np.random.normal(0, 0.1, sound.shape)
sound += noise

# Lecture du son
sd.play(sound, sample_rate)
sd.wait()
