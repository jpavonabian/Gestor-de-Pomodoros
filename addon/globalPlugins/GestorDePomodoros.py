# -*- coding: utf-8 -*-
# Complemento para NVDA que ayuda a seguir ciclos Pomodoro
# Copyright (C) 2024 Jesús Pavón Abián <galorasd@gmail.com>
# This file is covered by the GNU General Public License.
# Agradecimientos a Sukil Etxenike <sukiletxe@yahoo.es> por ponerme en el camino correcto cuando por falta de experiencia en el desarrollo de complementos no sabía por dónde tirar.
# Agradecimientos a Ángel Alcántar <rayoalcantar@gmail.com> por echarle un ojo al código.
# Agradecimientos a Noelia Ruiz Martínez <nrm1977@gmail.com> por el Feedback que está dando con respecto al código y por aguantar tantísima duda de novato.

import globalPluginHandler
import scriptHandler
from threading import Thread, Event
import ui
import addonHandler
import time
import tones
import globalVars
from speech.priorities import SpeechPriority

addonHandler.initTranslation()

#DURACION_POMODORO = 25
#DURACION_DESCANSO = 5
#DURACION_DESCANSO_LARGO = 10

DURACION_POMODORO = 25 * 60
DURACION_DESCANSO = 5 * 60
DURACION_DESCANSO_LARGO = 15 * 60
FRECUENCIA_TONO_INICIO = 400
FRECUENCIA_TONO_DESCANSO = 600
DURACION_TONO = 600

class PomodoroThread(Thread):
    def __init__(self):
        super(PomodoroThread, self).__init__()
        self.stop_event = Event()
        self.paused = True
        self.daemon = true
        self.reset()

    def reset(self):
        self.paused = True
        self.pomodoro_active = False
        self.start_time = time.monotonic()
        self.in_break = False
        self.cycles_completed = 0
        self.long_break = False

    def run(self):
        while not self.stop_event.is_set():
            if not self.paused and self.pomodoro_active:
                self.check_time()
            time.sleep(0.5)

    def check_time(self):
        current_time = time.monotonic()
        elapsed_time = current_time - self.start_time
        if not self.in_break and elapsed_time >= DURACION_POMODORO:
            self.start_break()
        elif self.in_break and elapsed_time >= (DURACION_DESCANSO if not self.long_break else DURACION_DESCANSO_LARGO):
            self.end_break()

    def start_break(self):
        self.in_break = True
        self.start_time = time.monotonic()
        self.cycles_completed += 1
        if self.cycles_completed % 4 == 0:
            self.long_break = True
            # Translators: A long break begins.
            wx.CallAfter(ui.message, _("Ciclo completado. Iniciando descanso largo."),SpeechPriority.NOW)
            tones.beep(FRECUENCIA_TONO_DESCANSO, DURACION_TONO)
        else:
            self.long_break = False
            # Translators: A break begins.
            wx.CallAfter(ui.message, _("Ciclo completado. Iniciando descanso."),SpeechPriority.NOW)
            tones.beep(FRECUENCIA_TONO_DESCANSO, DURACION_TONO)

    def end_break(self):
        self.in_break = False
        self.start_time = time.monotonic()
        if self.long_break:
            # Translators: A long break ends.
            wx.CallAfter(ui.message, _("Descanso largo finalizado. Iniciando nuevo ciclo."),SpeechPriority.NOW)
            self.long_break = False
        else:
            # Translators: A break ends.
            wx.CallAfter(ui.message, _("Descanso finalizado. Iniciando nuevo ciclo."),SpeechPriority.NOW)
        tones.beep(FRECUENCIA_TONO_INICIO, DURACION_TONO)

    def report_status(self):
        if not self.pomodoro_active:
            # Translators: Pomodoro is not active.
            wx.CallAfter(ui.message, _("El pomodoro no está activo."),SpeechPriority.NOW)
            return
        current_time = time.monotonic()
        if self.paused:
            # Translators: Pomodoro is paused.
            wx.CallAfter(ui.message, _("El pomodoro está pausado."),SpeechPriority.NOW)
            return
        elapsed_time = current_time - self.start_time
        if self.in_break:
            remaining_time = DURACION_DESCANSO_LARGO - elapsed_time if self.long_break else DURACION_DESCANSO - elapsed_time
            # Translators: Break in progres.
            wx.CallAfter(ui.message, _("Descanso en progreso. Tiempo restante: {minutes} minutos y {seconds} segundos.").format(minutes=int(remaining_time // 60), seconds=int(remaining_time % 60)),SpeechPriority.NOW)
        else:
            remaining_time = DURACION_POMODORO - elapsed_time
            # Translators: Pomodoro in progress.
            wx.CallAfter(ui.message, _("Ciclo en progreso. Tiempo restante: {minutes} minutos y {seconds} segundos.").format(minutes=int(remaining_time // 60), seconds=int(remaining_time % 60)),SpeechPriority.NOW)

    def stop(self):
        self.stop_event.set()

# Decorador para deshabilitar en modo seguro
def disableInSecureMode(decoratedCls):
    if globalVars.appArgs.secure:
        return globalPluginHandler.GlobalPlugin
    return decoratedCls

@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.pomodoro_thread = PomodoroThread()
        self.pomodoro_thread.start()

    def terminate(self):
        if self.pomodoro_thread.is_alive():
            self.pomodoro_thread.stop()
            self.pomodoro_thread.join()

    @scriptHandler.script(description=_("Inicia o pausa el Pomodoro"), gesture=None, category=_("Gestor de pomodoros"))
    def script_togglePomodoro(self, gesture):
        if not self.pomodoro_thread.pomodoro_active:
            self.pomodoro_thread.reset()
            self.pomodoro_thread.pomodoro_active = True
            self.pomodoro_thread.paused = False
            self.pomodoro_thread.in_break = False
            self.pomodoro_thread.start_time = time.monotonic()
            # Translators: Message announced when the Pomodoro is started.
            ui.message(_("Pomodoro iniciado."))
        elif self.pomodoro_thread.paused:
            self.pomodoro_thread.paused = False
            # Translators: Message announced when the Pomodoro is resumed.
            ui.message(_("Pomodoro reanudado."))
        else:
            self.pomodoro_thread.paused = True
            # Translators: Message announced when the Pomodoro is paused.
            ui.message(_("Pomodoro pausado."))

    @scriptHandler.script(description=_("Reporta el estado del Pomodoro"), gesture=None, category=_("Gestor de pomodoros"))
    def script_reportPomodoroStatus(self, gesture):
        self.pomodoro_thread.report_status()

    @scriptHandler.script(description=_("Detiene el Pomodoro"), gesture=None, category=_("Gestor de pomodoros"))
    def script_stopPomodoro(self, gesture):
        if self.pomodoro_thread.pomodoro_active:
            self.pomodoro_thread.reset()
            # Translators: Message announced when the Pomodoro is stopped.
            ui.message(_("Pomodoro detenido."))
        else:
            # Translators: Message announced when the Pomodoro is not stopped.
            ui.message(_("No hay ningún pomodoro activo."))
            