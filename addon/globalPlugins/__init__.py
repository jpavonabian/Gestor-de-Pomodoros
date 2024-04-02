import globalPluginHandler
import scriptHandler
from threading import Thread, Event
import ui
import addonHandler
import time
import tones

addonHandler.initTranslation()

DURACION_POMODORO = 25 * 60
DURACION_DESCANSO = 5 * 60
DURACION_DESCANSO_LARGO = 15 * 60
FRECUENCIA_TONO_INICIO = 440
FRECUENCIA_TONO_DESCANSO = 550
DURACION_TONO = 200

class PomodoroThread(Thread):
    def __init__(self):
        super(PomodoroThread, self).__init__()
        self.stop_event = Event()
        self.paused = True
        self.reset()

    def reset(self):
        self.paused = True
        self.pomodoro_active = False
        self.start_time = None
        self.in_break = False
        self.cycles_completed = 0
        self.long_break = False

    def run(self):
        while not self.stop_event.is_set():
            if not self.paused and self.pomodoro_active:
                self.check_time()
            time.sleep(1)

    def check_time(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if not self.in_break and elapsed_time >= DURACION_POMODORO:
            self.start_break()
        elif self.in_break and elapsed_time >= (DURACION_DESCANSO if not self.long_break else DURACION_DESCANSO_LARGO):
            self.end_break()

    def start_break(self):
        self.in_break = True
        self.start_time = time.time()
        if self.cycles_completed % 4 == 0:
            self.long_break = True
            ui.message("Ciclo completado. Iniciando descanso largo.")
            tones.beep(FRECUENCIA_TONO_DESCANSO, DURACION_TONO, 2)
        else:
            self.long_break = False
            ui.message("Ciclo completado. Iniciando descanso.")
            tones.beep(FRECUENCIA_TONO_DESCANSO, DURACION_TONO)

    def end_break(self):
        self.cycles_completed += 1
        self.in_break = False
        self.start_time = time.time()
        if self.long_break:
            ui.message("Descanso largo finalizado. Iniciando nuevo ciclo.")
            self.long_break = False
        else:
            ui.message("Descanso finalizado. Iniciando nuevo ciclo.")
        tones.beep(FRECUENCIA_TONO_INICIO, DURACION_TONO)

    def report_status(self):
        if not self.pomodoro_active:
            ui.message("El Pomodoro no está activo.")
            return
        current_time = time.time()
        if self.paused:
            ui.message("El Pomodoro está pausado.")
            return
        elapsed_time = current_time - self.start_time
        if self.in_break:
            remaining_time = DURACION_DESCANSO_LARGO - elapsed_time if self.long_break else DURACION_DESCANSO - elapsed_time
            ui.message(f"Descanso en progreso. Tiempo restante: {int(remaining_time // 60)} minutos y {int(remaining_time % 60)} segundos.")
        else:
            remaining_time = DURACION_POMODORO - elapsed_time
            ui.message(f"Ciclo en progreso. Tiempo restante: {int(remaining_time // 60)} minutos y {int(remaining_time % 60)} segundos.")

    def stop(self):
        self.stop_event.set()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.pomodoro_thread = PomodoroThread()
        self.pomodoro_thread.start()
        self.lastKeyPressTime = 0
        self.keyPressCount = 0

    def __del__(self):
        if self.pomodoro_thread.is_alive():
            self.pomodoro_thread.stop()
            self.pomodoro_thread.join()

    @scriptHandler.script(description="Gestiona el Pomodoro (iniciar/reportar/pausar)", gesture="kb:NVDA+SHIFT+P")
    def script_managePomodoro(self, gesture):
        currentTime = time.time()
        if currentTime - self.lastKeyPressTime < 0.5:
            self.keyPressCount += 1
        else:
            self.keyPressCount = 1

        if self.keyPressCount == 1:
            if not self.pomodoro_thread.pomodoro_active:
                self.pomodoro_thread.reset()
                self.pomodoro_thread.pomodoro_active = True
                self.pomodoro_thread.paused = False
                self.pomodoro_thread.in_break = False
                self.pomodoro_thread.start_time = time.time()
                ui.message("Pomodoro iniciado.")
            elif self.pomodoro_thread.paused:
                self.pomodoro_thread.paused = False
                ui.message("Pomodoro reanudado.")
            else:
                self.pomodoro_thread.report_status()
        elif self.keyPressCount >= 2:
            if self.pomodoro_thread.pomodoro_active and not self.pomodoro_thread.paused:
                self.pomodoro_thread.paused = True
                ui.message("Pomodoro pausado.")
            elif self.pomodoro_thread.paused:
                self.pomodoro_thread.paused = False
                ui.message("Pomodoro reanudado.")
            else:
                ui.message("No hay un Pomodoro activo para pausar o reanudar.")
        self.lastKeyPressTime = currentTime

    @scriptHandler.script(description="Detiene el Pomodoro", gesture="kb:NVDA+CTRL+SHIFT+P")
    def script_stopPomodoro(self, gesture):
        if self.pomodoro_thread.pomodoro_active:
            self.pomodoro_thread.reset()
            ui.message("Pomodoro detenido.")
